#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

from sktime.forecasting.base import BaseForecaster


class MyCustomForecaster(BaseForecaster):

    def _fit(self, y, X=None, fh=None):
        return self

    @classmethod
    def create_test_instance(cls):
        return cls()
