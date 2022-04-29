import pytest
from django.test import override_settings
from django.urls import resolve

# format of the tuple below:
#   ( route-to-test, expected-matching-route-name, is-route-an-endpoint (ex. index.html) )
PATHS_TO_ROUTE_NAMES = [
    # src/sentry/web/debug_urls.py
    ("/debug/mail/alert", "sentry-frontend-debug-mail-alert", False),
    ("/debug/mail/note", "sentry-frontend-debug-mail-note", False),
    ("/debug/mail/new-release", "sentry-frontend-debug-mail-new-release", False),
    ("/debug/mail/new-user-feedback", "sentry-frontend-debug-mail-new-user-feedback", False),
    ("/debug/mail/assigned", "sentry-frontend-debug-mail-assigned", False),
    ("/debug/mail/assigned/self", "sentry-frontend-debug-mail-assigned-self", False),
    ("/debug/mail/assigned/team", "sentry-frontend-debug-mail-assigned-team", False),
    (
        "/debug/mail/codeowners_auto_sync_failure",
        "sentry-frontend-debug-mail-codeowners-sync-fail",
        False,
    ),
    ("/debug/mail/digest", "sentry-frontend-debug-mail-digest", False),
    ("/debug/mail/report", "sentry-frontend-debug-mail-report", False),
    ("/debug/mail/regression", "sentry-frontend-debug-mail-regression", False),
    ("/debug/mail/regression/release", "sentry-frontend-debug-mail-regression-release", False),
    ("/debug/mail/resolved", "sentry-frontend-debug-mail-resolved", False),
    ("/debug/mail/resolved-in-release", "sentry-frontend-debug-mail-resolved-in-release", False),
    (
        "/debug/mail/resolved-in-release/upcoming",
        "sentry-frontend-debug-mail-resolved-in-release-upcoming",
        False,
    ),
    ("/debug/mail/request-access", "sentry-frontend-debug-mail-request-access", False),
    (
        "/debug/mail/request-access-for-another-member",
        "sentry-frontend-debug-mail-request-access-another-member",
        False,
    ),
    ("/debug/mail/join-request", "sentry-frontend-debug-mail-join-request", False),
    ("/debug/mail/invite-request", "sentry-frontend-debug-mail-invite-request", False),
    ("/debug/mail/access-approved", "sentry-frontend-debug-mail-access-approved", False),
    ("/debug/mail/invitation", "sentry-frontend-debug-mail-invitation", False),
    ("/debug/mail/invalid-identity", "sentry-frontend-debug-mail-invalid-identity", False),
    ("/debug/mail/codeowners-request", "sentry-frontend-debug-mail-codeowners-request", False),
    ("/debug/mail/confirm-email", "sentry-frontend-debug-mail-confirm-email", False),
    ("/debug/mail/recover-account", "sentry-frontend-debug-mail-recover-account", False),
    (
        "/debug/mail/unable-to-delete-repo",
        "sentry-frontend-debug-mail-unable-to-delete-repo",
        False,
    ),
    (
        "/debug/mail/unable-to-fetch-commits",
        "sentry-frontend-debug-mail-unable-to-fetch-commits",
        False,
    ),
    ("/debug/mail/unassigned", "sentry-frontend-debug-mail-unassigned", False),
    ("/debug/mail/org-delete-confirm", "sentry-frontend-debug-mail-org-delete-confirm", False),
    ("/debug/mail/mfa-removed", "sentry-frontend-debug-mail-mfa-removed", False),
    ("/debug/mail/mfa-added", "sentry-frontend-debug-mail-mfa-added", False),
    (
        "/debug/mail/recovery-codes-regenerated",
        "sentry-frontend-debug-mail-recovery-codes-regenerated",
        False,
    ),
    ("/debug/mail/password-changed", "sentry-frontend-debug-mail-password-changed", False),
    (
        "/debug/mail/new-processing-issues",
        "sentry-frontend-debug-mail-new-processing-issues",
        False,
    ),
    (
        "/debug/mail/new-processing-issues-no-reprocessing",
        "sentry-frontend-debug-mail-new-processing-issues-no-reprocessing",
        False,
    ),
    ("/debug/mail/sso-linked", "sentry-frontend-debug-mail-sso-linked", False),
    ("/debug/mail/sso-unlinked", "sentry-frontend-debug-mail-sso-unlinked", False),
    (
        "/debug/mail/sso-unlinked/no-password",
        "sentry-frontend-debug-mail-sso-unlinked-no-password",
        False,
    ),
    ("/debug/mail/incident-activity", "sentry-frontend-debug-mail-incident-activity", False),
    ("/debug/mail/incident-trigger", "sentry-frontend-debug-mail-incident-trigger", False),
    ("/debug/mail/setup-2fa", "sentry-frontend-debug-mail-setup-2fa", False),
    ("/debug/embed/error-page", "sentry-frontend-debug-embed-error-page", False),
    ("/debug/trigger-error", "sentry-frontend-debug-trigger-error", False),
    ("/debug/auth-confirm-identity", "sentry-frontend-debug-auth-confirm-identity", False),
    ("/debug/auth-confirm-link", "sentry-frontend-debug-auth-confirm-link", False),
    ("/debug/sudo", "sentry-frontend-debug-sudo", False),
    ("/debug/oauth/authorize", "sentry-frontend-debug-oauth-authorize", False),
    ("/debug/oauth/authorize/error", "sentry-frontend-debug-oauth-authorize-error", False),
    ("/debug/chart-renderer", "sentry-frontend-debug-chart-renderer", False),
    # TODO(mdtro): These two are failing even in 2.2.24.
    # ("_static/something/something/images/favicon.ico", "sentry-dev-favicon", True),
    # ("_static/something/something/images/favicon.png", "sentry-dev-favicon", True),
    # src/sentry/web/urls.py
    # We don't test any route with an `include` here. Those are tested in their specific app/module.
    ("/api/project-id_1234/crossdomain.xml", "sentry-api-crossdomain-xml", True),
    ("/api/client-config", "sentry-api-client-config", False),
    ("/_static/dist/somemodule/somepathmedia.js", "sentry-frontend-app-media", True),
    # testing three variants here since the `version` can either be a 10 digit timestamp,
    # sha1, or md5
    ("/_static/1234567890/somemodule/somepathmedia.js", "sentry-media", True),
    ("/_static/2080520c2ce6ea7336e784f2698534f2/somemodule/somepathmedia.js", "sentry-media", True),
    (
        "/_static/9d53e21c4d3770329ee56b66a0ca63ae3571344a/somemodule/somepathmedia.js",
        "sentry-media",
        True,
    ),
    ("/js-sdk-loader/SomePublicKey.min.js", "sentry-js-sdk-loader", True),
    ("/api/hooks/mailgun/inbound", "sentry-mailgun-inbound-hook", False),
    ("/api/hooks/release/pluginid/projectid/signature", "sentry-release-hook", False),
    ("/api/embed/error-page", "sentry-error-page-embed", False),
    # OAuth
    ("/oauth/authorize", "sentry-auth-oauth-authorize", False),
    ("/oauth/token", "sentry-auth-oauth-token", False),
    # SAML
    ("/saml/acs/orgslug", "sentry-auth-organization-saml-acs", False),
    ("/saml/sls/orgslug", "sentry-auth-organization-saml-sls", False),
    ("/saml/metadata/orgslug", "sentry-auth-organization-saml-metadata", False),
    # Auth
    ("/auth/login", "sentry-login", False),
    ("/auth/login/orgslug", "sentry-auth-organization", False),
    ("/auth/link/orgslug", "sentry-auth-link-identity", False),
    ("/auth/2fa", "sentry-2fa-dialog", False),
    ("/auth/2fa/u2fappid.json", "sentry-u2f-app-id", True),
    ("/auth/sso", "sentry-auth-sso", False),
    ("/auth/logout", "sentry-logout", False),
    ("/auth/reactivate", "sentry-reactivate-account", False),
    ("/auth/register", "sentry-register", False),
    ("/auth/close", "sentry-auth-close", False),
    ("/login-redirect", "sentry-login-redirect", False),
    # Account
    ("/account/sudo", "sentry-sudo", False),
    ("/account/confirm-email", "sentry-account-confirm-email-send", False),
    ("/account/authorizations", "sentry-account-settings-authorizations-redirect", False),
    (
        "/account/confirm-email/123456/15f69e7693e3ff20be170fa680fd725e",
        "sentry-account-confirm-email",
        False,
    ),
    ("/account/user-confirm/somekey", "sentry-idp-email-verification", False),
    ("/account/recover", "sentry-account-recover", False),
    (
        "/account/recover/confirm/123456/15f69e7693e3ff20be170fa680fd725e",
        "sentry-account-recover-confirm",
        False,
    ),
    (
        "/account/password/confirm/123456/15f69e7693e3ff20be170fa680fd725e",
        "sentry-account-set-password-confirm",
        False,
    ),
    ("/account/settings", "sentry-account-settings-redirect", False),
    ("/account/settings/2fa", "sentry-account-settings-2fa-security-redirect", False),
    ("/account/settings/avatar", "sentry-account-settings-avatar-redirect", False),
    ("/account/settings/appearance", "sentry-account-settings-appearance-redirect", False),
    ("/account/settings/identities", "sentry-account-settings-identities-redirect", False),
    ("/account/settings/subscriptions", "sentry-account-settings-subscriptions-redirect", False),
    (
        "/account/settings/identities/associate/orgslug/providerkey/externalid",
        "sentry-account-associate-identity",
        False,
    ),
    ("/account/settings/security", "sentry-account-settings-security-redirect", False),
    ("/account/settings/emails", "sentry-account-settings-emails-redirect", False),
    (
        "/account/settings/wizard/15f69e7693e3ff20be170fa680fd725e",
        "sentry-project-wizard-fetch",
        False,
    ),
    (
        "/account/settings/notifications/unsubscribe/123456",
        "sentry-account-settings-compatibility-notifications-unsubscribe",
        False,
    ),
    ("/account/settings/notifications", "sentry-account-settings-notifications-redirect", False),
    (
        "/account/notifications/unsubscribe/123456",
        "sentry-account-email-unsubscribe-project",
        False,
    ),
    (
        "/account/notifications/unsubscribe/issue/123456",
        "sentry-account-email-unsubscribe-issue",
        False,
    ),
    (
        "/account/notifications/unsubscribe/incident/123456",
        "sentry-account-email-unsubscribe-incident",
        False,
    ),
    ("/account/remove", "sentry-remove-account-redirect", False),
    ("/onboarding", "sentry-onboarding", False),
    ("/manage", "sentry-admin-overview", False),
    ("/docs", "sentry-docs-redirect", False),
    ("/docs/api", "sentry-api-docs-redirect", False),
    ("/api", "sentry-api-redirect", False),
    ("/api/applications", "sentry-api-applications-redirect", False),
    ("/api/new-token", "sentry-api-new-auth-token-redirect", False),
    # ("/api/anythingbut0", "sentry-api-not-0-redirect", False),
    ("/out", "sentry-out", False),
    ("/accept-transfer", "sentry-accept-project-transfer", False),
    ("/accept/123456/sometoken123456", "sentry-accept-invite", False),
    ("/settings/account", "sentry-account-settings", False),
    ("/settings/account/authorizations", "sentry-account-settings-authorizations", False),
    ("/settings/account/security", "sentry-account-settings-security", False),
    ("/settings/account/avatar", "sentry-account-settings-avatar", False),
    ("/settings/account/identities", "sentry-account-settings-identities", False),
    ("/settings/account/subscriptions", "sentry-account-settings-subscriptions", False),
    ("/settings/account/notifications", "sentry-account-settings-notifications", False),
    ("/settings/account/emails", "sentry-account-settings-emails", False),
    ("/settings/account/api/applications", "sentry-api-applications", False),
    ("/settings/account/api/auth-tokens/new-token", "sentry-api-new-auth-token", False),
    ("/settings/account/api", "sentry-api", False),
    ("/settings/account/close-account", "sentry-remove-account", False),
    ("/settings/orgslug", "sentry-organization-settings", False),
    ("/settings/orgslug/teams", "sentry-organization-teams", False),
    ("/settings/orgslug/members", "sentry-organization-members", False),
    ("/settings/orgslug/members/12345", "sentry-organization-member-settings", False),
    ("/settings/orgslug/auth", "sentry-organization-auth-settings", False),
    ("/settings/orgslug/random_words-catchall", "sentry-organization-catchall", False),
    # ("/settings", "sentry-settings-catchall", False),
    ("/extensions/external-install/providerid/installationid", "integration-installation", False),
    ("/orgslug", "sentry-organization-home", False),
    # Organizations
    ("/organizations/new", "sentry-organization-new", False),
    ("/organizations/org-slug_with_underscore", "sentry-organization-index", False),
    ("/organizations/orgslug/issues", "sentry-organization-issue-list", False),
    ("/organizations/orgslug/issues/123456", "sentry-organization-issue", False),
    # skipping this test for now, the above route conflicts and will always take precedence
    # ("/organizations/orgslug/issues/123456", "sentry-organization-issue-detail", False),
    (
        "/organizations/orgslug/issues/123456/events/event-id-or-latest",
        "sentry-organization-event-detail",
        False,
    ),
    ("/organizations/orgslug/data-export/123456", "sentry-data-export-details", False),
    (
        "/organizations/orgslug/issues/123456/events/event-id-or-latest/json",
        "sentry-group-event-json",
        False,
    ),
    (
        "/organizations/orgslug/projects/project_slug/events/client-event-id",
        "sentry-project-event-redirect",
        False,
    ),
    ("/organizations/orgslug/api-keys", "sentry-organization-api-keys", False),
    (
        "/organizations/orgslug/api-keys/example_key-id",
        "sentry-organization-api-key-settings",
        False,
    ),
    ("/organizations/orgslug/auth/configure", "sentry-organization-auth-provider-settings", False),
    (
        "/organizations/orgslug/integrations/provider_id/setup",
        "sentry-organization-integrations-setup",
        False,
    ),
    ("/organizations/orgslug/members", "sentry-organization-members-old", False),
    ("/organizations/orgslug/members/123456", "sentry-organization-member-settings-old", False),
    ("/organizations/orgslug/stats", "sentry-organization-stats", False),
    ("/organizations/orgslug/restore", "sentry-restore-organization", False),
    ("/organizations/orgslug/disabled-member", "sentry-organization-disabled-member", False),
    ("/organizations/orgslug/something_random-for-catchall", "sentry-organization-catchall", False),
    # Settings - Projects
    ("/orgslug/projectslug/settings", "sentry-manage-project-redirect", False),
    # TODO (mdtro): this will never match as the `/settings` (`sentry-settings-catchall`) route above will always match.
    #  Since it is using a top-level route with includes.
    # ("/settings/orgslug/projects/projectslug", "sentry-manage-project", False),
    ("/avatar/avatarid", "sentry-user-avatar-url", False),
    ("/organization-avatar/avatarid", "sentry-organization-avatar-url", False),
    ("/project-avatar/avatarid", "sentry-project-avatar-url", False),
    ("/team-avatar/avatarid", "sentry-team-avatar-url", False),
    ("/sentry-app-avatar/avatarid", "sentry-app-avatar-url", False),
    ("/doc-integration-avatar/avatarid", "sentry-doc-integration-avatar-url", False),
    ("/_chartcuterie-config.js", "sentry-chartcuterie-config", True),
    ("/", "sentry", True),  # TODO: should this be is_endpoint = True?
    ("/robots.txt", "sentry-api-robots-txt", True),
    ("/favicon.ico", "sentry-favicon-404", True),
    ("/crossdomain.xml", "sentry-crossdomain-404", True),
    ("/extensions/provider_id/setup", "sentry-extension-setup", False),
    ("/share/group/share_id-123", "sentry-group-shared", False),
    ("/share/issue/share_id-123", "sentry-group-shared", False),
    ("/join-request/orslug", "sentry-join-request", False),
    ("/orgslug/issues/short_id-123", "sentry-short-id", False),
    ("/orgslug/project_id-123/issues/123456", "sentry-group", False),
    ("/orgslug/project_slug-123/issues/123456/events/event_id-123", "sentry-group-event", False),
    ("/orgslug/project_id-123", "sentry-stream", False),
    ("/organizations/orgslug/alerts/123456", "sentry-metric-alert", False),
    # TODO (mdtro): this will never match as the `/settings` (`sentry-settings-catchall`) route above will always match.
    #  Since it is using a top-level route with includes.
    # ("/settings/orgslug/projects/project_slug-1234/alerts/metric-rules/123456", "sentry-alert-rule", False),
    (
        "/orgslug/project_slug-1234/issues/123456/tags/somekey/export",
        "sentry-group-tag-export",
        False,
    ),
    (
        "/orgslug/project_slug-1234/issues/123456/actions/some-slug",
        "sentry-group-plugin-action",
        False,
    ),
    ("/orgslug/project-slug/events/client_123-event-id", "sentry-project-event-redirect", False),
    # TODO (mdtro): this route may never match as the `sentry` route above will
    # ("/", "sentry-catchall", False)
]


@pytest.mark.url_resolve
@pytest.mark.parametrize("path,expected_route_name,is_endpoint", PATHS_TO_ROUTE_NAMES)
@override_settings(DEBUG=True)
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
@pytest.mark.parametrize("path,expected_route_name,is_endpoint", PATHS_TO_ROUTE_NAMES)
@override_settings(DEBUG=True)
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
