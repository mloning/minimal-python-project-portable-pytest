#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

from base_package.utils.testing import configure_pytest_generate_tests, BaseEstimatorTestCollection, ForecasterTestCollection

# Configure pytest test collection.
# We parametrise tests with estimator classes and objects.
pytest_generate_tests = configure_pytest_generate_tests(estimator_types="forecaster")


class TestForecaster(ForecasterTestCollection, BaseEstimatorTestCollection):
    # Test class discovered during pytest test collection.
    # All methods are run during testing.
    # We inherit common API tests from the base package.

    def test_estimator_class_collection(self, estimator_class):
        assert estimator_class.__name__ == "MyForecaster"

    def test_estimator_instance_collection(self, estimator_instance):
        assert estimator_instance.__class__.__name__ == "MyForecaster"
