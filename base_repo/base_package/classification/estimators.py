#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

from sktime.classification.base import BaseClassifier
import pandas as pd
import numpy as np


class MyClassifier(BaseClassifier):

    def _fit(self, y, X=None, fh=None):
        pass

    def _predict(self, fh, X=None, return_pred_int=False, alpha=0.95):
        return pd.Series(np.ones(len(fh)))

    @classmethod
    def create_test_instance(cls):
        return cls()
