import pytest
from django.urls import resolve

# this file tests src/sentry/django_admin.py
# specifically this import:
# `urlpatterns = [re_path("^admin/?$", include(site.urls[:2]))]`


PATHS_TO_ROUTE_NAMES = [
    ("/admin", "index"),  # `index` is the name of the route within django.contrib.admin.sites
    # ("/admin/login", "login"),
    # ("/admin/logout", "logout"),
    # ("/admin/password_change", "password_change"),
    # ("/admin/password_change/done", "password_change_done"),
    # ("/admin/jsi18n", "jsi18n")
]


@pytest.mark.url_resolve
@pytest.mark.parametrize("path,expected_route_name", PATHS_TO_ROUTE_NAMES)
def test_expected_route_match_without_trailing_slash(path: str, expected_route_name):
    path = path.rstrip("/")  # removing any trailing slash, we want to test without it
    match = resolve(f"{path}")
    assert (
        match.url_name == expected_route_name
    ), f"{match.url_name} != {expected_route_name} | matched on route {match.route} | matched function: {match._func_path}"


@pytest.mark.url_resolve
@pytest.mark.parametrize("path,expected_route_name", PATHS_TO_ROUTE_NAMES)
def test_expected_route_match_with_trailing_slash(path: str, expected_route_name):
    path = path.rstrip("/")  # removing any trailing slash (so we don't end up with `//`)
    match = resolve(f"{path}/")
    assert (
        match.url_name == expected_route_name
    ), f"{match.url_name} != {expected_route_name} | matched on route {match.route} | matched function: {match._func_path}"
