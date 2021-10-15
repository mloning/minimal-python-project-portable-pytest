#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

from base_package.registry import configure_all_estimators
from pathlib import Path


all_estimators = configure_all_estimators(
    root_dir=str(Path(__file__).parent),
    package_name="companion_package",
    ignore_modules=None,
)
