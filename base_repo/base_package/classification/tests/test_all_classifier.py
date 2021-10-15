#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

from base_package.utils.testing import configure_pytest_generate_tests, BaseEstimatorChecks, ClassifierChecks

pytest_generate_tests = configure_pytest_generate_tests(estimator_types="classifier")


class TestClassifier(BaseEstimatorChecks, ClassifierChecks):

    def test_estimator_class_collection(self, estimator_class):
        assert estimator_class.__name__ == "MyClassifier"

    def test_estimator_instance_collection(self, estimator_instance):
        assert estimator_instance.__class__.__name__ == "MyClassifier"
