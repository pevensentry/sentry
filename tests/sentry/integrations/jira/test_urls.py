import pytest
from django.urls import resolve

PATHS_TO_ROUTE_NAMES = [
    ("/extensions/jira/ui-hook", "sentry-extensions-jira-uihook"),
    ("/extensions/jira/descriptor", "sentry-extensions-jira-descriptor"),
    ("/extensions/jira/installed", "sentry-extensions-jira-installed"),
    ("/extensions/jira/uninstalled", "sentry-extensions-jira-uninstalled"),
    ("/extensions/jira/issue-updated", "sentry-extensions-jira-issue-updated"),
    ("/extensions/jira/search/orgslug/123456", "sentry-extensions-jira-search"),
    ("/extensions/jira/configure", "sentry-extensions-jira-configure"),
    ("/extensions/jira/issue/APP-123", "sentry-extensions-jira-issue-hook"),
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
