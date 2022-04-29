import importlib
import pkgutil

import pytest

"""
What's happening below?

We're using pytest to generate tests for integrations that contain a `urls.py` file.

From there, we import `urlpatterns` (the common Django pattern for declaring URLs) and
then iterate over each of the URLPattern's to make sure they have a `name` attribute.

Having the `name` attribute will help with unit testing route matching and using the
Django `reverse` function when needed.
"""


def pytest_generate_tests(metafunc):
    integrations_module = importlib.import_module("sentry.integrations")

    integrations_with_urls = set()
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        integrations_module.__path__, integrations_module.__name__ + "."
    ):
        if str(module_name).endswith("urls"):
            integrations_with_urls.add(module_name)

    if "test_urls" in metafunc.fixturenames:
        metafunc.parametrize("test_urls", integrations_with_urls)


@pytest.mark.url_resolve
def test_urlpatterns_have_names(test_urls):
    integration = importlib.import_module(test_urls)
    url_patterns = getattr(integration, "urlpatterns")

    for pattern in url_patterns:
        assert pattern.name, f"Missing `name` attribute on route {str(pattern.pattern)}"
