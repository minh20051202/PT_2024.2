#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test helper functions and assertion utilities for the invoice management system.

This module provides custom assertion helpers that make tests more readable
and maintainable by encapsulating common test patterns.
"""

from typing import Dict, Any
from models import Product


class TestAssertions:
    """Custom assertion helpers for testing."""

    @staticmethod
    def assert_product_equal(actual: Product, expected: Dict[str, Any]):
        """Assert that a Product object matches expected data."""
        assert actual.product_id == expected['product_id']
        assert actual.name == expected['name']
        assert actual.unit_price == expected['unit_price']
        assert actual.calculation_unit == expected.get('calculation_unit', 'đơn vị')
        assert actual.category == expected.get('category', 'General')
