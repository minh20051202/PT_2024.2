#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for validation functions.
"""

import pytest
import sys
import os
from datetime import datetime

# Add src to path for imports
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
    """Tests for validate_positive_number function."""

    def test_valid_positive_numbers(self):
        """Test with valid positive numbers."""
        test_cases = [
            (1, "Test field"),
            (10.5, "Price"),
            (0.01, "Small amount"),
            (1000000, "Large amount"),
            ("123.45", "String number")  # Should convert to float
        ]

        for value, field_name in test_cases:
            valid, error = validate_positive_number(value, field_name)
            assert valid, f"Expected {value} to be valid"
            assert error == "", f"Expected no error for {value}"

    def test_invalid_numbers(self):
        """Test with invalid numbers."""
        test_cases = [
            (-1, "Negative number"),
            (-10.5, "Negative decimal"),
            (0, "Zero"),
            (-0.01, "Small negative")
        ]

        for value, description in test_cases:
            valid, error = validate_positive_number(value, "Test field")
            assert not valid, f"Expected {value} ({description}) to be invalid"
            assert "phải lớn hơn 0" in error

    def test_non_numeric_values(self):
        """Test with non-numeric values."""
        test_cases = [
            ("abc", "Non-numeric string"),
            (None, "None value"),
            ([], "List"),
            ({}, "Dictionary")
        ]

        for value, description in test_cases:
            valid, error = validate_positive_number(value, "Test field")
            assert not valid, f"Expected {value} ({description}) to be invalid"
            assert "phải là một số" in error


class TestValidateRequiredField:
    """Tests for validate_required_field function."""

    def test_valid_values(self):
        """Test with valid non-empty values."""
        test_cases = [
            ("Test string", "String"),
            (123, "Number"),
            ([1, 2, 3], "List"),
            ({"key": "value"}, "Dictionary"),
            (0, "Zero number"),  # Zero is considered valid
            (False, "Boolean False")  # False is considered valid
        ]

        for value, description in test_cases:
            valid, error = validate_required_field(value, "Test field")
            assert valid, f"Expected {value} ({description}) to be valid"
            assert error == ""

    def test_invalid_values(self):
        """Test with invalid empty values."""
        test_cases = [
            ("", "Empty string"),
            ("   ", "Whitespace only"),
            (None, "None value")
        ]

        for value, description in test_cases:
            valid, error = validate_required_field(value, "Test field")
            assert not valid, f"Expected {value} ({description}) to be invalid"
            assert "bắt buộc" in error


class TestValidateStringLength:
    """Tests for validate_string_length function."""

    def test_valid_lengths(self):
        """Test strings with valid lengths."""
        test_cases = [
            ("Hello", 3, 10),
            ("Test", 4, 4),  # Exact length
            ("A" * 50, 1, 100),
            ("", 0, 5)  # Empty string with min_length 0
        ]

        for value, min_len, max_len in test_cases:
            valid, error = validate_string_length(value, "Test field", min_len, max_len)
            assert valid, f"Expected '{value}' to be valid (min={min_len}, max={max_len})"
            assert error == ""

    def test_invalid_lengths(self):
        """Test strings with invalid lengths."""
        # Too short
        valid, error = validate_string_length("Hi", "Test field", 5, 10)
        assert not valid
        assert "ít nhất 5 ký tự" in error

        # Too long
        valid, error = validate_string_length("Very long string", "Test field", 1, 5)
        assert not valid
        assert "không được vượt quá 5 ký tự" in error

    def test_non_string_values(self):
        """Test with non-string values."""
        test_cases = [123, None, [], {}]

        for value in test_cases:
            valid, error = validate_string_length(value, "Test field", 1, 10)
            assert not valid
            assert "phải là chuỗi" in error


class TestValidateDateFormat:
    """Tests for validate_date_format function."""

    def test_valid_dates(self):
        """Test with valid date formats."""
        test_cases = [
            ("2023-12-25", "%Y-%m-%d"),
            ("25/12/2023", "%d/%m/%Y"),
            ("2023-12-25 14:30:00", "%Y-%m-%d %H:%M:%S")
        ]

        for date_str, format_str in test_cases:
            valid, error = validate_date_format(date_str, "Test field", format_str)
            assert valid, f"Expected '{date_str}' to be valid with format '{format_str}'"
            assert error == ""

    def test_invalid_dates(self):
        """Test with invalid date formats."""
        test_cases = [
            ("2023-13-25", "%Y-%m-%d"),  # Invalid month
            ("25-12-2023", "%Y-%m-%d"),  # Wrong format
            ("not-a-date", "%Y-%m-%d"),
            ("", "%Y-%m-%d")
        ]

        for date_str, format_str in test_cases:
            valid, error = validate_date_format(date_str, "Test field", format_str)
            assert not valid, f"Expected '{date_str}' to be invalid"
            assert format_str in error


class TestValidateEmail:
    """Tests for validate_email function."""

    def test_valid_emails(self):
        """Test with valid email addresses."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com",
            "a@b.co"
        ]

        for email in valid_emails:
            valid, error = validate_email(email)
            assert valid, f"Expected '{email}' to be valid"
            assert error == ""

    def test_invalid_emails(self):
        """Test with invalid email addresses."""
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
            assert not valid, f"Expected '{email}' to be invalid"
            assert "không hợp lệ" in error


class TestValidatePhoneNumber:
    """Tests for validate_phone_number function."""

    def test_valid_phone_numbers(self):
        """Test with valid Vietnamese phone numbers."""
        valid_phones = [
            "0912345678",
            "0987654321",
            "0356789012",
            "0798765432"
        ]

        for phone in valid_phones:
            valid, error = validate_phone_number(phone)
            assert valid, f"Expected '{phone}' to be valid"
            assert error == ""

    def test_invalid_phone_numbers(self):
        """Test with invalid phone numbers."""
        invalid_phones = [
            "123456789",  # Too short
            "01234567890",  # Too long
            "0123456789",  # Invalid prefix
            "abc1234567",  # Contains letters
            "",
            "84912345678"  # International format
        ]

        for phone in invalid_phones:
            valid, error = validate_phone_number(phone)
            assert not valid, f"Expected '{phone}' to be invalid"
            assert "không hợp lệ" in error


class TestValidateProductId:
    """Tests for validate_product_id function."""

    def test_valid_product_ids(self):
        """Test with valid product IDs."""
        valid_ids = [
            "P001",
            "PROD123",
            "ABC123",
            "TEST01"
        ]

        for product_id in valid_ids:
            valid, error = validate_product_id(product_id)
            assert valid, f"Expected '{product_id}' to be valid"
            assert error == ""

    def test_invalid_product_ids(self):
        """Test with invalid product IDs."""
        invalid_ids = [
            "",  # Empty
            "P1",  # Too short
            "VERYLONGPRODUCTID",  # Too long
            "p001",  # Lowercase
            "P-001",  # Contains hyphen
            "P 001"  # Contains space
        ]

        for product_id in invalid_ids:
            valid, error = validate_product_id(product_id)
            assert not valid, f"Expected '{product_id}' to be invalid"
            assert error != ""


class TestValidateQuantity:
    """Tests for validate_quantity function."""

    def test_valid_quantities(self):
        """Test with valid quantities."""
        valid_quantities = [1, 5, 100, 999, "10", "500"]

        for quantity in valid_quantities:
            valid, error = validate_quantity(quantity)
            assert valid, f"Expected '{quantity}' to be valid"
            assert error == ""

    def test_invalid_quantities(self):
        """Test with invalid quantities."""
        invalid_quantities = [
            0,  # Zero
            -1,  # Negative
            1001,  # Too large
            "abc",  # Non-numeric
            None,  # None
            # Note: 3.5 might be valid depending on implementation
        ]

        for quantity in invalid_quantities:
            valid, error = validate_quantity(quantity)
            assert not valid, f"Expected '{quantity}' to be invalid"
            assert error != ""