import pytest
from django.urls import resolve

# TODO (mdtro): determine where these are loading in at?


PATHS_TO_ROUTE_NAMES = [
    ("/associate/complete/backend", "socialauth_associate_complete", False),
    ("/associate/backend", "socialauth_associate", False),
]


@pytest.mark.url_resolve
@pytest.mark.skip(reason="Need to determine where these urls are included")
@pytest.mark.parametrize("path,expected_route_name,is_endpoint", PATHS_TO_ROUTE_NAMES)
def test_expected_route_match_without_trailing_slash(
    path: str, expected_route_name, is_endpoint: bool
):
    if is_endpoint:
        match = resolve(f"{path}")
        assert (
            match.url_name == expected_route_name
        ), f"{match.url_name} != {expected_route_name} | matched on route {match.route} | matched function: {match._func_path}"
    else:
        path = path.rstrip("/")  # removing any trailing slash, we want to test without it
        match = resolve(f"{path}")
        assert (
            match.url_name == expected_route_name
        ), f"{match.url_name} != {expected_route_name} | matched on route {match.route} | matched function: {match._func_path}"


@pytest.mark.url_resolve
@pytest.mark.skip(reason="Need to determine where these urls are included")
@pytest.mark.parametrize("path,expected_route_name,is_endpoint", PATHS_TO_ROUTE_NAMES)
def test_expected_route_match_with_trailing_slash(
    path: str, expected_route_name, is_endpoint: bool
):
    if is_endpoint:
        match = resolve(f"{path}")
        assert (
            match.url_name == expected_route_name
        ), f"{match.url_name} != {expected_route_name} | matched on route {match.route} | matched function: {match._func_path}"
    else:
        path = path.rstrip("/")  # removing any trailing slash (so we don't end up with `//`)
        match = resolve(f"{path}/")
        assert (
            match.url_name == expected_route_name
        ), f"{match.url_name} != {expected_route_name} | matched on route {match.route} | matched function: {match._func_path}"
