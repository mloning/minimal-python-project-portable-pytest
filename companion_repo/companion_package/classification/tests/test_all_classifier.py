#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

from companion_package.utils.testing import configure_pytest_generate_tests
from base_package.utils.testing import BaseEstimatorTestCollection, ClassifierTestCollection

pytest_generate_tests = configure_pytest_generate_tests(estimator_types="classifier")


class TestClassifier(BaseEstimatorTestCollection, ClassifierTestCollection):

    def test_estimator_class_collection(self, estimator_class):
        assert estimator_class.__name__ == "MyCustomClassifier"

    def test_estimator_instance_collection(self, estimator_instance):
        assert estimator_instance.__class__.__name__ == "MyCustomClassifier"
