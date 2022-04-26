import pytest
from django.urls import resolve

PATHS_TO_ROUTE_NAMES = [
    ("/extensions/slack/action", "sentry-integration-slack-action"),
    ("/extensions/slack/commands", "sentry-integration-slack-commands"),
    ("/extensions/slack/event", "sentry-integration-slack-event"),
    ("/extensions/slack/link-identity/signedparams123", "sentry-integration-slack-link-identity"),
    (
        "/extensions/slack/unlink-identity/signedparams123",
        "sentry-integration-slack-unlink-identity",
    ),
    ("/extensions/slack/link-team/signedparams123", "sentry-integration-slack-link-team"),
    ("/extensions/slack/unlink-team/signedparams123", "sentry-integration-slack-unlink-team"),
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
