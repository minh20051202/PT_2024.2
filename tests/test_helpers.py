#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hàm trợ giúp test và tiện ích assertion cho hệ thống quản lý hóa đơn.

Module này cung cấp các helper assertion tùy chỉnh giúp tests dễ đọc hơn
và dễ bảo trì bằng cách đóng gói các pattern test phổ biến.

Các lớp hỗ trợ:
- TestAssertions: Chứa các phương thức assertion tùy chỉnh
  cho việc so sánh và kiểm tra các đối tượng trong hệ thống

Sử dụng trong các test để thực hiện kiểm tra phức tạp một cách rõ ràng.
"""

from typing import Dict, Any
from models import Product


class TestAssertions:
    """Helper assertion tùy chỉnh cho testing."""

    @staticmethod
    def assert_product_equal(actual: Product, expected: Dict[str, Any]):
        """Kiểm tra rằng một đối tượng Product khớp với dữ liệu mong đợi."""
        assert actual.product_id == expected['product_id']
        assert actual.name == expected['name']
        assert actual.unit_price == expected['unit_price']
        assert actual.calculation_unit == expected.get('calculation_unit', 'đơn vị')
        assert actual.category == expected.get('category', 'General')
