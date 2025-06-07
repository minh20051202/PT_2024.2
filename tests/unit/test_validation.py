#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm tra toàn diện cho các hàm validation.
"""

import pytest
import sys
import os
from datetime import datetime

# Thêm src vào path để import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from utils.validation import (
    validate_positive_number,
    validate_required_field,
    validate_string_length,
    validate_date_format,
    validate_email,
    validate_phone_number,
    validate_product_id,
    validate_quantity
)

class TestValidatePositiveNumber:
    """Kiểm tra cho hàm validate_positive_number."""

    def test_valid_positive_numbers(self):
        """Kiểm tra với các số dương hợp lệ."""
        test_cases = [
            (1, "Test field"),
            (10.5, "Price"),
            (0.01, "Small amount"),
            (1000000, "Large amount"),
            ("123.45", "String number")  # Nên chuyển đổi thành float
        ]

        for value, field_name in test_cases:
            valid, error = validate_positive_number(value, field_name)
            assert valid, f"Mong đợi {value} hợp lệ"
            assert error == "", f"Mong đợi không có lỗi cho {value}"

    def test_invalid_numbers(self):
        """Kiểm tra với các số không hợp lệ."""
        test_cases = [
            (-1, "Số âm"),
            (-10.5, "Số thập phân âm"),
            (0, "Số không"),
            (-0.01, "Số âm nhỏ")
        ]

        for value, description in test_cases:
            valid, error = validate_positive_number(value, "Test field")
            assert not valid, f"Mong đợi {value} ({description}) không hợp lệ"
            assert "phải lớn hơn 0" in error

    def test_non_numeric_values(self):
        """Kiểm tra với các giá trị không phải số."""
        test_cases = [
            ("abc", "Chuỗi không phải số"),
            (None, "Giá trị None"),
            ([], "Danh sách"),
            ({}, "Từ điển")
        ]

        for value, description in test_cases:
            valid, error = validate_positive_number(value, "Test field")
            assert not valid, f"Mong đợi {value} ({description}) không hợp lệ"
            assert "phải là một số" in error


class TestValidateRequiredField:
    """Kiểm tra cho hàm validate_required_field."""

    def test_valid_values(self):
        """Kiểm tra với các giá trị hợp lệ không rỗng."""
        test_cases = [
            ("Test string", "Chuỗi"),
            (123, "Số"),
            ([1, 2, 3], "Danh sách"),
            ({"key": "value"}, "Từ điển"),
            (0, "Số không"),  # Số không được coi là hợp lệ
            (False, "Boolean False")  # False được coi là hợp lệ
        ]

        for value, description in test_cases:
            valid, error = validate_required_field(value, "Test field")
            assert valid, f"Mong đợi {value} ({description}) hợp lệ"
            assert error == ""

    def test_invalid_values(self):
        """Kiểm tra với các giá trị rỗng không hợp lệ."""
        test_cases = [
            ("", "Chuỗi rỗng"),
            ("   ", "Chỉ có khoảng trắng"),
            (None, "Giá trị None")
        ]

        for value, description in test_cases:
            valid, error = validate_required_field(value, "Test field")
            assert not valid, f"Mong đợi {value} ({description}) không hợp lệ"
            assert "bắt buộc" in error


class TestValidateStringLength:
    """Kiểm tra cho hàm validate_string_length."""

    def test_valid_lengths(self):
        """Kiểm tra chuỗi với độ dài hợp lệ."""
        test_cases = [
            ("Hello", 3, 10),
            ("Test", 4, 4),  # Độ dài chính xác
            ("A" * 50, 1, 100),
            ("", 0, 5)  # Chuỗi rỗng với min_length 0
        ]

        for value, min_len, max_len in test_cases:
            valid, error = validate_string_length(value, "Test field", min_len, max_len)
            assert valid, f"Mong đợi '{value}' hợp lệ (min={min_len}, max={max_len})"
            assert error == ""

    def test_invalid_lengths(self):
        """Kiểm tra chuỗi với độ dài không hợp lệ."""
        # Quá ngắn
        valid, error = validate_string_length("Hi", "Test field", 5, 10)
        assert not valid
        assert "ít nhất 5 ký tự" in error

        # Quá dài
        valid, error = validate_string_length("Very long string", "Test field", 1, 5)
        assert not valid
        assert "không được vượt quá 5 ký tự" in error

    def test_whitespace_handling(self):
        """Kiểm tra xử lý khoảng trắng trong validation."""
        # Test string with leading/trailing whitespace
        valid, error = validate_string_length("  hello  ", "Test", 5, 10)
        assert valid, "Mong đợi chuỗi có whitespace được trim hợp lệ"
        
        # Test string that becomes too short after trimming
        valid, error = validate_string_length("  a  ", "Test", 3, 10)
        assert not valid, "Mong đợi chuỗi quá ngắn sau trim không hợp lệ"
        assert "ít nhất 3 ký tự" in error
        
        # Test string with only whitespace
        valid, error = validate_string_length("   ", "Test", 1, 10)
        assert not valid, "Mong đợi chuỗi chỉ có whitespace không hợp lệ"
        assert "ít nhất 1 ký tự" in error

    def test_non_string_values(self):
        """Kiểm tra với các giá trị không phải chuỗi."""
        test_cases = [123, None, [], {}]

        for value in test_cases:
            valid, error = validate_string_length(value, "Test field", 1, 10)
            assert not valid
            assert "phải là chuỗi" in error
            
    def test_exact_boundary_lengths(self):
        """Kiểm tra các giá trị boundary chính xác cho độ dài."""
        # Test string with exact minimum length
        valid, error = validate_string_length("ab", "Test", 2, 5)
        assert valid, "Mong đợi chuỗi độ dài chính xác tối thiểu hợp lệ"
        
        # Test string with exact maximum length
        valid, error = validate_string_length("abcde", "Test", 2, 5)
        assert valid, "Mong đợi chuỗi độ dài chính xác tối đa hợp lệ"
        
        # Test one character under minimum
        valid, error = validate_string_length("a", "Test", 2, 5)
        assert not valid, "Mong đợi chuỗi ngắn hơn tối thiểu không hợp lệ"
        assert "ít nhất 2 ký tự" in error
        
        # Test one character over maximum
        valid, error = validate_string_length("abcdef", "Test", 2, 5)
        assert not valid, "Mong đợi chuỗi dài hơn tối đa không hợp lệ"
        assert "không được vượt quá 5 ký tự" in error


class TestValidateDateFormat:
    """Kiểm tra cho hàm validate_date_format."""

    def test_valid_dates(self):
        """Kiểm tra với các định dạng ngày hợp lệ."""
        test_cases = [
            ("2023-12-25", "%Y-%m-%d"),
            ("25/12/2023", "%d/%m/%Y"),
            ("2023-12-25 14:30:00", "%Y-%m-%d %H:%M:%S")
        ]

        for date_str, format_str in test_cases:
            valid, error = validate_date_format(date_str, "Test field", format_str)
            assert valid, f"Mong đợi '{date_str}' hợp lệ với định dạng '{format_str}'"
            assert error == ""

    def test_invalid_dates(self):
        """Kiểm tra với các định dạng ngày không hợp lệ."""
        test_cases = [
            ("2023-13-25", "%Y-%m-%d"),  # Tháng không hợp lệ
            ("25-12-2023", "%Y-%m-%d"),  # Định dạng sai
            ("not-a-date", "%Y-%m-%d"),
            ("", "%Y-%m-%d")
        ]

        for date_str, format_str in test_cases:
            valid, error = validate_date_format(date_str, "Test field", format_str)
            assert not valid, f"Mong đợi '{date_str}' không hợp lệ"
            assert format_str in error


class TestValidateEmail:
    """Kiểm tra cho hàm validate_email."""

    def test_valid_emails(self):
        """Kiểm tra với các địa chỉ email hợp lệ."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com",
            "a@b.co"
        ]

        for email in valid_emails:
            valid, error = validate_email(email)
            assert valid, f"Mong đợi '{email}' hợp lệ"
            assert error == ""

    def test_invalid_emails(self):
        """Kiểm tra với các địa chỉ email không hợp lệ."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test.example.com",
            "test@.com",
            "",
            "test@example"
        ]

        for email in invalid_emails:
            valid, error = validate_email(email)
            assert not valid, f"Mong đợi '{email}' không hợp lệ"
            assert "không hợp lệ" in error


class TestValidatePhoneNumber:
    """Kiểm tra cho hàm validate_phone_number."""

    def test_valid_phone_numbers(self):
        """Kiểm tra với các số điện thoại Việt Nam hợp lệ."""
        valid_phones = [
            "0912345678",
            "0987654321",
            "0356789012",
            "0798765432"
        ]

        for phone in valid_phones:
            valid, error = validate_phone_number(phone)
            assert valid, f"Mong đợi '{phone}' hợp lệ"
            assert error == ""

    def test_invalid_phone_numbers(self):
        """Kiểm tra với các số điện thoại không hợp lệ."""
        invalid_phones = [
            "123456789",  # Quá ngắn
            "01234567890",  # Quá dài
            "0123456789",  # Tiền tố không hợp lệ
            "abc1234567",  # Chứa chữ cái
            "",
            "84912345678"  # Định dạng quốc tế
        ]

        for phone in invalid_phones:
            valid, error = validate_phone_number(phone)
            assert not valid, f"Mong đợi '{phone}' không hợp lệ"
            assert "không hợp lệ" in error


class TestValidateProductId:
    """Kiểm tra cho hàm validate_product_id."""

    def test_valid_product_ids(self):
        """Kiểm tra với các ID sản phẩm hợp lệ."""
        valid_ids = [
            "P001",
            "PROD123",
            "ABC123",
            "TEST01"
        ]

        for product_id in valid_ids:
            valid, error = validate_product_id(product_id)
            assert valid, f"Mong đợi '{product_id}' hợp lệ"
            assert error == ""

    def test_invalid_product_ids(self):
        """Kiểm tra với các ID sản phẩm không hợp lệ."""
        invalid_ids = [
            "",  # Rỗng
            "P1",  # Quá ngắn
            "VERYLONGPRODUCTID",  # Quá dài
            "p001",  # Chữ thường
            "P-001",  # Chứa dấu gạch ngang
            "P 001"  # Chứa khoảng trắng
        ]

        for product_id in invalid_ids:
            valid, error = validate_product_id(product_id)
            assert not valid, f"Mong đợi '{product_id}' không hợp lệ"
            assert error != ""


class TestValidateQuantity:
    """Kiểm tra cho hàm validate_quantity."""

    def test_valid_quantities(self):
        """Kiểm tra với các số lượng hợp lệ."""
        valid_quantities = [1, 5, 100, 999, "10", "500"]

        for quantity in valid_quantities:
            valid, error = validate_quantity(quantity)
            assert valid, f"Mong đợi '{quantity}' hợp lệ"
            assert error == ""

    def test_invalid_quantities(self):
        """Kiểm tra với các số lượng không hợp lệ."""
        invalid_quantities = [
            0,  # Số không
            -1,  # Số âm
            1001,  # Quá lớn
            "abc",  # Không phải số
            None,  # None
            # Lưu ý: 3.5 có thể hợp lệ tùy thuộc vào implementation
        ]

        for quantity in invalid_quantities:
            valid, error = validate_quantity(quantity)
            assert not valid, f"Mong đợi '{quantity}' không hợp lệ"
            assert error != ""
    
    def test_boundary_values_detailed(self):
        """Kiểm tra chi tiết các giá trị boundary cụ thể."""
        # Test exact boundary for quantity limit (1000)
        valid, error = validate_quantity(1000)
        assert valid, "Mong đợi 1000 (giá trị giới hạn trên) hợp lệ"
        assert error == ""
        
        # Test just over the limit
        valid, error = validate_quantity(1001)
        assert not valid, "Mong đợi 1001 (vượt quá giới hạn) không hợp lệ"
        assert "không được vượt quá 1000" in error
        
        # Test exact minimum boundary (1)
        valid, error = validate_quantity(1)
        assert valid, "Mong đợi 1 (giá trị tối thiểu) hợp lệ"
        assert error == ""
        
        # Test just under minimum (0)
        valid, error = validate_quantity(0)
        assert not valid, "Mong đợi 0 (dưới giá trị tối thiểu) không hợp lệ"
        assert "phải lớn hơn 0" in error
        
    def test_edge_cases_extreme_values(self):
        """Kiểm tra các trường hợp biên với giá trị cực đại/cực tiểu."""
        import sys
        
        # Test very large integer
        valid, error = validate_quantity(sys.maxsize)
        assert not valid, "Mong đợi số nguyên rất lớn không hợp lệ"
        assert "không được vượt quá 1000" in error
        
        # Test negative very large number
        valid, error = validate_quantity(-sys.maxsize)
        assert not valid, "Mong đợi số âm rất lớn không hợp lệ"
        assert "phải lớn hơn 0" in error
