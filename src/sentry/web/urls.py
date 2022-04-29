import re

from django.conf import settings
from django.http import HttpResponse
from django.urls import include, re_path
from django.views.generic import RedirectView

from sentry.auth.providers.saml2.provider import SAML2AcceptACSView, SAML2MetadataView, SAML2SLSView
from sentry.charts.endpoints import serve_chartcuterie_config
from sentry.web import api
from sentry.web.frontend import accounts, generic
from sentry.web.frontend.account_identity import AccountIdentityAssociateView
from sentry.web.frontend.auth_close import AuthCloseView
from sentry.web.frontend.auth_login import AuthLoginView
from sentry.web.frontend.auth_logout import AuthLogoutView
from sentry.web.frontend.auth_organization_login import AuthOrganizationLoginView
from sentry.web.frontend.auth_provider_login import AuthProviderLoginView
from sentry.web.frontend.disabled_member_view import DisabledMemberView
from sentry.web.frontend.doc_integration_avatar import DocIntegrationAvatarPhotoView
from sentry.web.frontend.error_page_embed import ErrorPageEmbedView
from sentry.web.frontend.group_event_json import GroupEventJsonView
from sentry.web.frontend.group_plugin_action import GroupPluginActionView
from sentry.web.frontend.group_tag_export import GroupTagExportView
from sentry.web.frontend.home import HomeView
from sentry.web.frontend.idp_email_verification import AccountConfirmationView
from sentry.web.frontend.js_sdk_loader import JavaScriptSdkLoader
from sentry.web.frontend.mailgun_inbound_webhook import MailgunInboundWebhookView
from sentry.web.frontend.oauth_authorize import OAuthAuthorizeView
from sentry.web.frontend.oauth_token import OAuthTokenView
from sentry.web.frontend.organization_auth_settings import OrganizationAuthSettingsView
from sentry.web.frontend.organization_avatar import OrganizationAvatarPhotoView
from sentry.web.frontend.organization_integration_setup import OrganizationIntegrationSetupView
from sentry.web.frontend.out import OutView
from sentry.web.frontend.pipeline_advancer import PipelineAdvancerView
from sentry.web.frontend.project_avatar import ProjectAvatarPhotoView
from sentry.web.frontend.project_event import ProjectEventRedirect
from sentry.web.frontend.react_page import GenericReactPageView, ReactPageView
from sentry.web.frontend.reactivate_account import ReactivateAccountView
from sentry.web.frontend.release_webhook import ReleaseWebhookView
from sentry.web.frontend.restore_organization import RestoreOrganizationView
from sentry.web.frontend.sentryapp_avatar import SentryAppAvatarPhotoView
from sentry.web.frontend.setup_wizard import SetupWizardView
from sentry.web.frontend.sudo import SudoView
from sentry.web.frontend.team_avatar import TeamAvatarPhotoView
from sentry.web.frontend.twofactor import TwoFactorAuthView, u2f_appid
from sentry.web.frontend.unsubscribe_incident_notifications import (
    UnsubscribeIncidentNotificationsView,
)
from sentry.web.frontend.unsubscribe_issue_notifications import UnsubscribeIssueNotificationsView
from sentry.web.frontend.user_avatar import UserAvatarPhotoView

__all__ = ("urlpatterns",)


# Only create one instance of the ReactPageView since it's duplicated everywhere
generic_react_page_view = GenericReactPageView.as_view()
react_page_view = ReactPageView.as_view()

urlpatterns = []

if getattr(settings, "DEBUG_VIEWS", settings.DEBUG):
    from sentry.web.debug_urls import urlpatterns as debug_urls

    urlpatterns += debug_urls

if getattr(settings, "SERVE_UPLOADED_FILES", settings.DEBUG):
    from django.views.static import serve

    # Serve FileSystemStorage files in development. In production this
    # would typically be handled by some static server.
    urlpatterns += [
        re_path(
            fr"^{re.escape(settings.MEDIA_URL)}(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
            name="sentry-serve-media",
        )
    ]

if settings.DEBUG:
    # Special favicon in debug mode
    urlpatterns += [
        re_path(
            r"^_static/[^/]+/[^/]+/images/favicon\.(ico|png)$",
            generic.dev_favicon,
            name="sentry-dev-favicon",
        ),
    ]

urlpatterns += [
    re_path(
        r"^api/(?P<project_id>[\w_-]+)/crossdomain\.xml$",
        api.crossdomain_xml,
        name="sentry-api-crossdomain-xml",
    ),
    # Frontend client config
    re_path(
        r"^api/client-config/?$", api.ClientConfigView.as_view(), name="sentry-api-client-config"
    ),
    # We do not want to have webpack assets served under a versioned URL, as these assets have
    # a filecontent-based hash in its filenames so that it can be cached long term
    re_path(
        r"^_static/dist/(?P<module>[^/]+)/(?P<path>.*)$",
        generic.frontend_app_static_media,
        name="sentry-frontend-app-media",
    ),
    # The static version is either a 10 digit timestamp, a sha1, or md5 hash
    re_path(
        r"^_static/(?:(?P<version>\d{10}|[a-f0-9]{32,40})/)?(?P<module>[^/]+)/(?P<path>.*)$",
        generic.static_media,
        name="sentry-media",
    ),
    # Javascript SDK Loader
    re_path(
        r"^js-sdk-loader/(?P<public_key>[^/\.]+)(?:(?P<minified>\.min))?\.js$",
        JavaScriptSdkLoader.as_view(),
        name="sentry-js-sdk-loader",
    ),
    # Versioned API
    re_path(r"^api/0/", include("sentry.api.urls")),
    # Legacy unversioned endpoints
    re_path(
        r"^api/hooks/mailgun/inbound/?$",
        MailgunInboundWebhookView.as_view(),
        name="sentry-mailgun-inbound-hook",
    ),
    re_path(
        r"^api/hooks/release/(?P<plugin_id>[^/]+)/(?P<project_id>[^/]+)/(?P<signature>[^/]+)/?$",
        ReleaseWebhookView.as_view(),
        name="sentry-release-hook",
    ),
    re_path(
        r"^api/embed/error-page/?$", ErrorPageEmbedView.as_view(), name="sentry-error-page-embed"
    ),
    # OAuth
    re_path(
        r"^oauth/",
        include(
            [
                re_path(
                    r"^authorize/?$",
                    OAuthAuthorizeView.as_view(),
                    name="sentry-auth-oauth-authorize",
                ),
                re_path(r"^token/?$", OAuthTokenView.as_view(), name="sentry-auth-oauth-token"),
            ]
        ),
    ),
    # SAML
    re_path(
        r"^saml/",
        include(
            [
                re_path(
                    r"^acs/(?P<organization_slug>[^/]+)/?$",
                    SAML2AcceptACSView.as_view(),
                    name="sentry-auth-organization-saml-acs",
                ),
                re_path(
                    r"^sls/(?P<organization_slug>[^/]+)/?$",
                    SAML2SLSView.as_view(),
                    name="sentry-auth-organization-saml-sls",
                ),
                re_path(
                    r"^metadata/(?P<organization_slug>[^/]+)/?$",
                    SAML2MetadataView.as_view(),
                    name="sentry-auth-organization-saml-metadata",
                ),
            ]
        ),
    ),
    # Auth
    re_path(
        r"^auth/",
        include(
            [
                re_path(r"^login/?$", AuthLoginView.as_view(), name="sentry-login"),
                re_path(
                    r"^login/(?P<organization_slug>[^/]+)/?$",
                    AuthOrganizationLoginView.as_view(),
                    name="sentry-auth-organization",
                ),
                re_path(
                    r"^link/(?P<organization_slug>[^/]+)/?$",
                    AuthOrganizationLoginView.as_view(),
                    name="sentry-auth-link-identity",
                ),
                re_path(r"^2fa/?$", TwoFactorAuthView.as_view(), name="sentry-2fa-dialog"),
                re_path(r"^2fa/u2fappid\.json$", u2f_appid, name="sentry-u2f-app-id"),
                re_path(r"^sso/?$", AuthProviderLoginView.as_view(), name="sentry-auth-sso"),
                re_path(r"^logout/?$", AuthLogoutView.as_view(), name="sentry-logout"),
                re_path(
                    r"^reactivate/?$",
                    ReactivateAccountView.as_view(),
                    name="sentry-reactivate-account",
                ),
                re_path(r"^register/?$", AuthLoginView.as_view(), name="sentry-register"),
                re_path(r"^close/?$", AuthCloseView.as_view(), name="sentry-auth-close"),
            ]
        ),
    ),
    re_path(r"^login-redirect/?$", accounts.login_redirect, name="sentry-login-redirect"),
    # Account
    re_path(
        r"^account/",
        include(
            [
                re_path(r"^sudo/?$", SudoView.as_view(), name="sentry-sudo"),
                re_path(
                    r"^confirm-email/?$",
                    accounts.start_confirm_email,
                    name="sentry-account-confirm-email-send",
                ),
                re_path(
                    r"^authorizations/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-authorizations", permanent=False
                    ),
                    name="sentry-account-settings-authorizations-redirect",
                ),
                re_path(
                    r"^confirm-email/(?P<user_id>[\d]+)/(?P<hash>[0-9a-zA-Z]+)/?$",
                    accounts.confirm_email,
                    name="sentry-account-confirm-email",
                ),
                re_path(
                    r"^user-confirm/(?P<key>[^\/]+)/?$",
                    AccountConfirmationView.as_view(),
                    name="sentry-idp-email-verification",
                ),
                re_path(r"^recover/?$", accounts.recover, name="sentry-account-recover"),
                re_path(
                    r"^recover/confirm/(?P<user_id>[\d]+)/(?P<hash>[0-9a-zA-Z]+)/?$",
                    accounts.recover_confirm,
                    name="sentry-account-recover-confirm",
                ),
                re_path(
                    r"^password/confirm/(?P<user_id>[\d]+)/(?P<hash>[0-9a-zA-Z]+)/?$",
                    accounts.set_password_confirm,
                    name="sentry-account-set-password-confirm",
                ),
                re_path(
                    r"^settings/?$",
                    RedirectView.as_view(pattern_name="sentry-account-settings", permanent=False),
                    name="sentry-account-settings-redirect",
                ),
                re_path(
                    r"^settings/2fa/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-security", permanent=False
                    ),
                    name="sentry-account-settings-2fa-security-redirect",
                ),
                re_path(
                    r"^settings/avatar/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-avatar", permanent=False
                    ),
                    name="sentry-account-settings-avatar-redirect",
                ),
                re_path(
                    r"^settings/appearance/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-appearance", permanent=False
                    ),
                    name="sentry-account-settings-appearance-redirect",
                ),
                re_path(
                    r"^settings/identities/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-identities", permanent=False
                    ),
                    name="sentry-account-settings-identities-redirect",
                ),
                re_path(
                    r"^settings/subscriptions/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-subscriptions", permanent=False
                    ),
                    name="sentry-account-settings-subscriptions-redirect",
                ),
                re_path(
                    r"^settings/identities/associate/(?P<organization_slug>[^\/]+)/(?P<provider_key>[^\/]+)/(?P<external_id>[^\/]+)/?$",
                    AccountIdentityAssociateView.as_view(),
                    name="sentry-account-associate-identity",
                ),
                re_path(
                    r"^settings/security/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-security", permanent=False
                    ),
                    name="sentry-account-settings-security-redirect",
                ),
                re_path(
                    r"^settings/emails/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-emails", permanent=False
                    ),
                    name="sentry-account-settings-emails-redirect",
                ),
                # Project Wizard
                re_path(
                    r"^settings/wizard/(?P<wizard_hash>[^\/]+)/?$",
                    SetupWizardView.as_view(),
                    name="sentry-project-wizard-fetch",
                ),
                # compatibility
                re_path(
                    r"^settings/notifications/unsubscribe/(?P<project_id>\d+)/?$",
                    accounts.email_unsubscribe_project,
                    name="sentry-account-settings-compatibility-notifications-unsubscribe",
                ),
                re_path(
                    r"^settings/notifications/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-account-settings-notifications", permanent=False
                    ),
                    name="sentry-account-settings-notifications-redirect",
                ),
                re_path(
                    r"^notifications/unsubscribe/(?P<project_id>\d+)/?$",
                    accounts.email_unsubscribe_project,
                    name="sentry-account-email-unsubscribe-project",
                ),
                re_path(
                    r"^notifications/unsubscribe/issue/(?P<issue_id>\d+)/?$",
                    UnsubscribeIssueNotificationsView.as_view(),
                    name="sentry-account-email-unsubscribe-issue",
                ),
                re_path(
                    r"^notifications/unsubscribe/incident/(?P<incident_id>\d+)/?$",
                    UnsubscribeIncidentNotificationsView.as_view(),
                    name="sentry-account-email-unsubscribe-incident",
                ),
                re_path(
                    r"^remove/?$",
                    RedirectView.as_view(pattern_name="sentry-remove-account", permanent=False),
                    name="sentry-remove-account-redirect",
                ),
                re_path(r"^settings/social/", include("social_auth.urls")),
                re_path(r"^", generic_react_page_view),
            ]
        ),
    ),
    # Onboarding
    re_path(r"^onboarding/?$", generic_react_page_view, name="sentry-onboarding"),
    # Admin
    re_path(r"^manage/?$", react_page_view, name="sentry-admin-overview"),
    # Legacy Redirects
    re_path(
        r"^docs/?$",
        RedirectView.as_view(url="https://docs.sentry.io/", permanent=False),
        name="sentry-docs-redirect",
    ),
    re_path(
        r"^docs/api/?$",
        RedirectView.as_view(url="https://docs.sentry.io/api/", permanent=False),
        name="sentry-api-docs-redirect",
    ),
    re_path(
        r"^api/?$",
        RedirectView.as_view(pattern_name="sentry-api", permanent=False),
        name="sentry-api-redirect",
    ),
    re_path(
        r"^api/applications/?$",
        RedirectView.as_view(pattern_name="sentry-api-applications", permanent=False),
        name="sentry-api-applications-redirect",
    ),
    re_path(
        r"^api/new-token/?$",
        RedirectView.as_view(pattern_name="sentry-api-new-auth-token", permanent=False),
        name="sentry-api-new-auth-token-redirect",
    ),
    re_path(
        r"^api/[^0]+/?$",
        RedirectView.as_view(pattern_name="sentry-api", permanent=False),
        name="sentry-api-not-0-redirect",
    ),
    re_path(r"^out/?$", OutView.as_view(), name="sentry-out"),
    re_path(r"^accept-transfer/?$", react_page_view, name="sentry-accept-project-transfer"),
    re_path(
        r"^accept/(?P<member_id>\d+)/(?P<token>\w+)/?$",
        GenericReactPageView.as_view(auth_required=False),
        name="sentry-accept-invite",
    ),
    # User settings use generic_react_page_view, while any view acting on
    # behalf of an organization should use react_page_view
    re_path(
        r"^settings/",
        include(
            [
                # TODO(mdtro): `account/` has three routes below, determine if we can remove
                #  the duplicates safely.
                re_path(r"^account/?$", generic_react_page_view, name="sentry-account-settings"),
                re_path(
                    r"^account/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-appearance",
                ),
                re_path(
                    r"^account/authorizations/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-authorizations",
                ),
                re_path(
                    r"^account/security/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-security",
                ),
                re_path(
                    r"^account/avatar/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-avatar",
                ),
                re_path(
                    r"^account/identities/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-identities",
                ),
                re_path(
                    r"^account/subscriptions/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-subscriptions",
                ),
                re_path(
                    r"^account/notifications/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-notifications",
                ),
                re_path(
                    r"^account/emails/?$",
                    generic_react_page_view,
                    name="sentry-account-settings-emails",
                ),
                re_path(
                    r"^account/api/applications/?$",
                    generic_react_page_view,
                    name="sentry-api-applications",
                ),
                re_path(
                    r"^account/api/auth-tokens/new-token/?$",
                    generic_react_page_view,
                    name="sentry-api-new-auth-token",
                ),
                re_path(r"^account/api/?$", generic_react_page_view, name="sentry-api"),
                re_path(
                    r"^account/close-account/?$",
                    generic_react_page_view,
                    name="sentry-remove-account",
                ),
                re_path(r"^account/", generic_react_page_view),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/?$",
                    react_page_view,
                    name="sentry-organization-settings",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/teams/?$",
                    react_page_view,
                    name="sentry-organization-teams",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/members/?$",
                    react_page_view,
                    name="sentry-organization-members",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/members/(?P<member_id>\d+)/?$",
                    react_page_view,
                    name="sentry-organization-member-settings",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/auth/?$",
                    react_page_view,
                    name="sentry-organization-auth-settings",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/[\w_-]+/?$",
                    react_page_view,
                    name="sentry-organization-catchall",
                ),
                # TODO(mdtro): Does this catchall need to be here?
                #  It will only match on `/settings/` and not `/settings`.
                re_path(r"^", react_page_view, name="sentry-settings-catchall"),
            ]
        ),
    ),
    re_path(
        r"^extensions/external-install/(?P<provider_id>\w+)/(?P<installation_id>\w+)/?$",
        react_page_view,
        name="integration-installation",
    ),
    # Organizations
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/?$", react_page_view, name="sentry-organization-home"
    ),
    re_path(
        r"^organizations/",
        include(
            [
                re_path(r"^new/?$", generic_react_page_view, name="sentry-organization-new"),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/?$",
                    react_page_view,
                    name="sentry-organization-index",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/issues/?$",
                    react_page_view,
                    name="sentry-organization-issue-list",
                ),
                # TODO(mdtro): These two routes below conflict with each other.
                #  The `sentry-organization-issue` route will always match first. Decide which to keep.
                re_path(
                    # See src.sentry.models.group.Group.get_absolute_url if this changes
                    r"^(?P<organization_slug>[\w_-]+)/issues/(?P<group_id>\d+)/?$",
                    react_page_view,
                    name="sentry-organization-issue",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/issues/(?P<issue_id>\d+)/?$",
                    react_page_view,
                    name="sentry-organization-issue-detail",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/issues/(?P<group_id>\d+)/events/(?P<event_id_or_latest>[\w-]+)/?$",
                    react_page_view,
                    name="sentry-organization-event-detail",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/data-export/(?P<data_export_id>\d+)/?$",
                    react_page_view,
                    name="sentry-data-export-details",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/issues/(?P<group_id>\d+)/events/(?P<event_id_or_latest>[\w-]+)/json/?$",
                    GroupEventJsonView.as_view(),
                    name="sentry-group-event-json",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/projects/(?P<project_slug>[\w_-]+)/events/(?P<client_event_id>[\w_-]+)/?$",
                    ProjectEventRedirect.as_view(),
                    name="sentry-project-event-redirect",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/api-keys/?$",
                    react_page_view,
                    name="sentry-organization-api-keys",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/api-keys/(?P<key_id>[\w_-]+)/?$",
                    react_page_view,
                    name="sentry-organization-api-key-settings",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/auth/configure/?$",
                    OrganizationAuthSettingsView.as_view(),
                    name="sentry-organization-auth-provider-settings",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/integrations/(?P<provider_id>[\w_-]+)/setup/?$",
                    OrganizationIntegrationSetupView.as_view(),
                    name="sentry-organization-integrations-setup",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/members/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-organization-members", permanent=False
                    ),
                    name="sentry-organization-members-old",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/members/(?P<member_id>\d+)/?$",
                    RedirectView.as_view(
                        pattern_name="sentry-organization-member-settings", permanent=False
                    ),
                    name="sentry-organization-member-settings-old",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/stats/?$",
                    react_page_view,
                    name="sentry-organization-stats",
                ),
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/restore/?$",
                    RestoreOrganizationView.as_view(),
                    name="sentry-restore-organization",
                ),
                re_path(
                    r"^(?P<organization_slug>[^/]+)/disabled-member/?$",
                    DisabledMemberView.as_view(),
                    name="sentry-organization-disabled-member",
                ),
                # need to force these to React and ensure organization_slug is captured
                re_path(
                    r"^(?P<organization_slug>[\w_-]+)/[\w_-]+/?$",
                    react_page_view,
                    name="sentry-organization-catchall",
                ),
            ]
        ),
    ),
    # Settings - Projects
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_slug>[\w_-]+)/settings/?$",
        RedirectView.as_view(pattern_name="sentry-manage-project", permanent=False),
        name="sentry-manage-project-redirect",
    ),
    # TODO (mdtro): this will never match as the `/settings` (`sentry-settings-catchall`) route above will always match.
    #  Since it is using a top-level route with includes.
    re_path(
        r"^settings/(?P<organization_slug>[\w_-]+)/projects/(?P<project_slug>[\w_-]+)/?$",
        react_page_view,
        name="sentry-manage-project",
    ),
    re_path(
        r"^avatar/(?P<avatar_id>[^\/]+)/?$",
        UserAvatarPhotoView.as_view(),
        name="sentry-user-avatar-url",
    ),
    re_path(
        r"^organization-avatar/(?P<avatar_id>[^\/]+)/?$",
        OrganizationAvatarPhotoView.as_view(),
        name="sentry-organization-avatar-url",
    ),
    re_path(
        r"^project-avatar/(?P<avatar_id>[^\/]+)/?$",
        ProjectAvatarPhotoView.as_view(),
        name="sentry-project-avatar-url",
    ),
    re_path(
        r"^team-avatar/(?P<avatar_id>[^\/]+)/?$",
        TeamAvatarPhotoView.as_view(),
        name="sentry-team-avatar-url",
    ),
    re_path(
        r"^sentry-app-avatar/(?P<avatar_id>[^\/]+)/?$",
        SentryAppAvatarPhotoView.as_view(),
        name="sentry-app-avatar-url",
    ),
    re_path(
        r"^doc-integration-avatar/(?P<avatar_id>[^\/]+)/?$",
        DocIntegrationAvatarPhotoView.as_view(),
        name="sentry-doc-integration-avatar-url",
    ),
    # Serve chartcuterie configuration module
    re_path(
        r"^_chartcuterie-config.js$",
        serve_chartcuterie_config,
        name="sentry-chartcuterie-config",
    ),
    # Generic
    re_path(r"^$", HomeView.as_view(), name="sentry"),
    re_path(r"^robots\.txt$", api.robots_txt, name="sentry-api-robots-txt"),
    # Force a 404 of favicon.ico.
    # This url is commonly requested by browsers, and without
    # blocking this, it was treated as a 200 OK for a react page view.
    # A side effect of this is it may cause a bad redirect when logging in
    # since this gets stored in session as the last viewed page.
    # See: https://github.com/getsentry/sentry/issues/2195
    re_path(r"favicon\.ico$", lambda r: HttpResponse(status=404), name="sentry-favicon-404"),
    # crossdomain.xml
    re_path(
        r"^crossdomain\.xml$", lambda r: HttpResponse(status=404), name="sentry-crossdomain-404"
    ),
    # plugins
    # XXX(dcramer): preferably we'd be able to use 'integrations' as the URL
    # prefix here, but unfortunately sentry.io has that mapped to marketing
    # assets for the time being
    re_path(
        r"^extensions/",
        include(
            [
                re_path(
                    r"^(?P<provider_id>[\w_-]+)/setup/?$",
                    PipelineAdvancerView.as_view(),
                    name="sentry-extension-setup",
                ),
                re_path(r"^cloudflare/", include("sentry.integrations.cloudflare.urls")),
                re_path(r"^jira/", include("sentry.integrations.jira.urls")),
                re_path(r"^jira-server/", include("sentry.integrations.jira_server.urls")),
                re_path(r"^slack/", include("sentry.integrations.slack.urls")),
                re_path(r"^github/", include("sentry.integrations.github.urls")),
                re_path(
                    r"^github-enterprise/", include("sentry.integrations.github_enterprise.urls")
                ),
                re_path(r"^gitlab/", include("sentry.integrations.gitlab.urls")),
                re_path(r"^vsts/", include("sentry.integrations.vsts.urls")),
                re_path(r"^bitbucket/", include("sentry.integrations.bitbucket.urls")),
                re_path(
                    r"^bitbucket-server/", include("sentry.integrations.bitbucket_server.urls")
                ),
                re_path(r"^vercel/", include("sentry.integrations.vercel.urls")),
                re_path(r"^msteams/", include("sentry.integrations.msteams.urls")),
            ]
        ),
    ),
    re_path(r"^plugins/", include("sentry.plugins.base.urls")),
    # Generic API
    re_path(
        r"^share/(?:group|issue)/(?P<share_id>[\w_-]+)/?$",
        GenericReactPageView.as_view(auth_required=False),
        name="sentry-group-shared",
    ),
    re_path(
        r"^join-request/(?P<organization_slug>[\w_-]+)/?$",
        GenericReactPageView.as_view(auth_required=False),
        name="sentry-join-request",
    ),
    # Keep named URL for for things using reverse
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/issues/(?P<short_id>[\w_-]+)/?$",
        react_page_view,
        name="sentry-short-id",
    ),
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_id>[\w_-]+)/issues/(?P<group_id>\d+)/?$",
        react_page_view,
        name="sentry-group",
    ),
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_slug>[\w_-]+)/issues/(?P<group_id>\d+)/events/(?P<event_id>[\w-]+)/?$",
        react_page_view,
        name="sentry-group-event",
    ),
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_id>[\w_-]+)/?$",
        react_page_view,
        name="sentry-stream",
    ),
    re_path(
        r"^organizations/(?P<organization_slug>[\w_-]+)/alerts/(?P<incident_id>\d+)/?$",
        react_page_view,
        name="sentry-metric-alert",
    ),
    re_path(
        r"^settings/(?P<organization_slug>[\w_-]+)/projects/(?P<project_slug>[\w_-]+)/alerts/metric-rules/(?P<alert_rule_id>\d+)/?$",
        react_page_view,
        name="sentry-alert-rule",
    ),
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_slug>[\w_-]+)/issues/(?P<group_id>\d+)/tags/(?P<key>[^\/]+)/export/?$",
        GroupTagExportView.as_view(),
        name="sentry-group-tag-export",
    ),
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_slug>[\w_-]+)/issues/(?P<group_id>\d+)/actions/(?P<slug>[\w_-]+)/?$",
        GroupPluginActionView.as_view(),
        name="sentry-group-plugin-action",
    ),
    re_path(
        r"^(?P<organization_slug>[\w_-]+)/(?P<project_slug>[\w_-]+)/events/(?P<client_event_id>[\w_-]+)/?$",
        ProjectEventRedirect.as_view(),
        name="sentry-project-event-redirect",
    ),
    # Legacy
    # This triggers a false positive for the urls.W002 Django warning
    re_path(r"/$", react_page_view, name="sentry-catchall"),
]
