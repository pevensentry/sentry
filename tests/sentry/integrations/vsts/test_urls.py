import pytest
from django.urls import resolve

PATHS_TO_ROUTE_NAMES = [
    ("/extensions/vsts/issue-updated", "sentry-extensions-vsts-issue-updated"),
    ("/extensions/vsts/search/orgslug/123456", "sentry-extensions-vsts-search"),
    ("/extensions/vsts/configure", "vsts-extension-configuration"),
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
