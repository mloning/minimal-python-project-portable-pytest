#!/usr/bin/env python3 -u
# coding: utf-8

__author__ = ["mloning"]
__all__ = []

import inspect
import pkgutil
from importlib import import_module
from operator import itemgetter

from pathlib import Path

from sktime.registry._lookup import VALID_ESTIMATOR_TYPES
from sktime.registry._lookup import _check_estimator_types


def configure_all_estimators(root_dir, package_name, ignore_modules=None):

    ignore_modules = [] if ignore_modules is None else ignore_modules

    def get_estimators(
        estimator_types=None,
        exclude_estimators=None,
        return_names=True,
    ):
        """Get a list of all estimators from sktime.

        This function crawls the module and gets all classes that inherit
        from sktime's and sklearn's base_package classes.

        Not included are: the base_package classes themselves, classes defined in test
        modules.

        Parameters
        ----------
        estimator_types: string, list of string, optional (default=None)
            Which kind of estimators should be returned.
            - If None, no filter is applied and all estimators are returned.
            - Possible values are 'classifier', 'regressor', 'transformer' and
            'forecaster' to get estimators only of these specific types, or a list of
            these to get the estimators that fit at least one of the types.
        return_names: bool, optional (default=True)
            If True, return estimators as list of (name, estimator class) tuples.
            If False, return list of estimators classes.
        exclude_estimators: str, list of str, optional (default=None)
            Names of estimators to exclude.

        Returns
        -------
        estimators: list of class, if return_names=False,
                or list of tuples (str, class), if return_names=True
            if list of estimators:
                entries are estimator classes matching the query,
                in alphabetical order of class name
            if list of tuples:
                list of (name, class) matching the query,
                in alphabetical order of class name, where
                ``name`` is the estimator class name as string
                ``class`` is the actual class

        References
        ----------
        Modified version from scikit-learn's `all_estimators()`.
        """
        import warnings

        all_estimators = []

        def _is_abstract(klass):
            if not (hasattr(klass, "__abstractmethods__")):
                return False
            if not len(klass.__abstractmethods__):
                return False
            return True

        def _is_private_module(module):
            return "._" in module

        def _is_ignored_module(module):
            module_parts = module.split(".")
            return any(part in ignore_modules for part in module_parts)

        def _is_base_class(name):
            return name.startswith("_") or name.startswith("Base")

        def _is_estimator(name, klass):
            # Check if klass is subclass of base_package estimators, not an base_package class itself and
            # not an abstract class
            return (
                issubclass(klass, VALID_ESTIMATOR_TYPES)
                and klass not in VALID_ESTIMATOR_TYPES
                and not _is_abstract(klass)
                and not _is_base_class(name)
            )

        # Ignore deprecation warnings triggered at import time and from walking
        # packages
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            warnings.simplefilter("module", category=ImportWarning)
            for _, module_name, _ in pkgutil.walk_packages(path=[root_dir], prefix=f"{package_name}."):

                # Filter modules
                if _is_ignored_module(module_name) or _is_private_module(module_name):
                    continue

                try:
                    module = import_module(module_name)
                    classes = inspect.getmembers(module, inspect.isclass)

                    # Filter classes
                    estimators = [
                        (name, klass)
                        for name, klass in classes
                        if _is_estimator(name, klass)
                    ]
                    all_estimators.extend(estimators)
                except ModuleNotFoundError as e:
                    # Skip missing soft dependencies
                    if "soft dependency" not in str(e):
                        raise e
                    warnings.warn(str(e), ImportWarning)

        # Drop duplicates
        all_estimators = set(all_estimators)

        # Filter based on given estimator types
        def _is_in_estimator_types(estimator, estimator_types):
            return any(
                [
                    issubclass(estimator, estimator_type)
                    for estimator_type in estimator_types
                ]
            )

        if estimator_types is not None:
            estimator_types = _check_estimator_types(estimator_types)
            all_estimators = [
                (name, estimator)
                for name, estimator in all_estimators
                if _is_in_estimator_types(estimator, estimator_types)
            ]

        # Filter based on given exclude list
        if exclude_estimators is not None:
            if not isinstance(exclude_estimators, list):
                exclude_estimators = [exclude_estimators]  # make iterable
            if not all([isinstance(estimator, str) for estimator in exclude_estimators]):
                raise ValueError(
                    "Please specify `exclude_estimators` as a list of strings."
                )
            all_estimators = [
                (name, estimator)
                for name, estimator in all_estimators
                if name not in exclude_estimators
            ]

        # Drop duplicates, sort for reproducibility
        # itemgetter is used to ensure the sort does not extend to the 2nd item of
        # the tuple
        all_estimators = sorted(all_estimators, key=itemgetter(0))

        # remove names if return_names=False
        if not return_names:
            all_estimators = [estimator for (name, estimator) in all_estimators]

        return all_estimators

    return get_estimators


all_estimators = configure_all_estimators(
    root_dir=str(Path(__file__).parent),
    package_name="base_package",
    ignore_modules=None,
)
