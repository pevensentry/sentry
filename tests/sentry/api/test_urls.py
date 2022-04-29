import pytest
from django.urls import resolve

# format of the tuple below:
#   ( route-to-test, expected-matching-route-name, is-route-an-endpoint (ex. index.html) )
PATHS_TO_ROUTE_NAMES = [
    # testing GROUP_URLS
    # these are included in api/urls.py with multiple prefixes `issues`, `groups`,
    # `/organizations/orgslug/issues/` or `/organizations/orgslug/groups/`.
    ("/api/0/issues/issue-id-1234", "sentry-api-0-group-details", False),
    ("/api/0/groups/issue-id-1234", "sentry-api-0-group-details", False),
    ("/api/0/organizations/orgslug/issues/issue-id-1234", "sentry-api-0-group-details", False),
    ("/api/0/organizations/orgslug/groups/issue-id-1234", "sentry-api-0-group-details", False),
    ("/api/0/issues/issue-id-1234/activities", "sentry-api-0-group-activities", False),
    ("/api/0/groups/issue-id-1234/activities", "sentry-api-0-group-activities", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/activities",
        "sentry-api-0-group-activities",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/activities",
        "sentry-api-0-group-activities",
        False,
    ),
    ("/api/0/issues/issue-id-1234/events", "sentry-api-0-group-events", False),
    ("/api/0/groups/issue-id-1234/events", "sentry-api-0-group-events", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/events",
        "sentry-api-0-group-events",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/events",
        "sentry-api-0-group-events",
        False,
    ),
    ("/api/0/issues/issue-id-1234/events/latest", "sentry-api-0-group-events-latest", False),
    ("/api/0/groups/issue-id-1234/events/latest", "sentry-api-0-group-events-latest", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/events/latest",
        "sentry-api-0-group-events-latest",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/events/latest",
        "sentry-api-0-group-events-latest",
        False,
    ),
    ("/api/0/issues/issue-id-1234/events/oldest", "sentry-api-0-group-events-oldest", False),
    ("/api/0/groups/issue-id-1234/events/oldest", "sentry-api-0-group-events-oldest", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/events/oldest",
        "sentry-api-0-group-events-oldest",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/events/oldest",
        "sentry-api-0-group-events-oldest",
        False,
    ),
    ("/api/0/issues/issue-id-1234/notes", "sentry-api-0-group-notes", False),
    ("/api/0/groups/issue-id-1234/notes", "sentry-api-0-group-notes", False),
    ("/api/0/organizations/orgslug/issues/issue-id-1234/notes", "sentry-api-0-group-notes", False),
    ("/api/0/organizations/orgslug/groups/issue-id-1234/notes", "sentry-api-0-group-notes", False),
    ("/api/0/issues/issue-id-1234/comments", "sentry-api-0-group-notes", False),
    ("/api/0/groups/issue-id-1234/comments", "sentry-api-0-group-notes", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/comments",
        "sentry-api-0-group-notes",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/comments",
        "sentry-api-0-group-notes",
        False,
    ),
    ("/api/0/issues/issue-id-1234/notes/note-id-1234", "sentry-api-0-group-notes-details", False),
    ("/api/0/groups/issue-id-1234/notes/note-id-1234", "sentry-api-0-group-notes-details", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/notes/note-id-1234",
        "sentry-api-0-group-notes-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/notes/note-id-1234",
        "sentry-api-0-group-notes-details",
        False,
    ),
    (
        "/api/0/issues/issue-id-1234/comments/note-id-1234",
        "sentry-api-0-group-notes-details",
        False,
    ),
    (
        "/api/0/groups/issue-id-1234/comments/note-id-1234",
        "sentry-api-0-group-notes-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/comments/note-id-1234",
        "sentry-api-0-group-notes-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/comments/note-id-1234",
        "sentry-api-0-group-notes-details",
        False,
    ),
    ("/api/0/issues/issue-id-1234/hashes", "sentry-api-0-group-hashes", False),
    ("/api/0/groups/issue-id-1234/hashes", "sentry-api-0-group-hashes", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/hashes",
        "sentry-api-0-group-hashes",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/hashes",
        "sentry-api-0-group-hashes",
        False,
    ),
    ("/api/0/issues/issue-id-1234/grouping/levels", "sentry-api-0-group-levels", False),
    ("/api/0/groups/issue-id-1234/grouping/levels", "sentry-api-0-group-levels", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/grouping/levels",
        "sentry-api-0-group-levels",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/grouping/levels",
        "sentry-api-0-group-levels",
        False,
    ),
    (
        "/api/0/issues/issue-id-1234/grouping/levels/id-555/new-issues",
        "sentry-api-0-group-level-new-issues",
        False,
    ),
    (
        "/api/0/groups/issue-id-1234/grouping/levels/id-555/new-issues",
        "sentry-api-0-group-level-new-issues",
        False,
    ),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/grouping/levels/id-555/new-issues",
        "sentry-api-0-group-level-new-issues",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/grouping/levels/id-555/new-issues",
        "sentry-api-0-group-level-new-issues",
        False,
    ),
    ("/api/0/issues/issue-id-1234/hashes/split", "sentry-api-0-group-hashes-split", False),
    ("/api/0/groups/issue-id-1234/hashes/split", "sentry-api-0-group-hashes-split", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/hashes/split",
        "sentry-api-0-group-hashes-split",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/hashes/split",
        "sentry-api-0-group-hashes-split",
        False,
    ),
    ("/api/0/issues/issue-id-1234/reprocessing", "sentry-api-0-issues-reprocessing", False),
    ("/api/0/groups/issue-id-1234/reprocessing", "sentry-api-0-issues-reprocessing", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/reprocessing",
        "sentry-api-0-issues-reprocessing",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/reprocessing",
        "sentry-api-0-issues-reprocessing",
        False,
    ),
    ("/api/0/issues/issue-id-1234/stats", "sentry-api-0-group-stats", False),
    ("/api/0/groups/issue-id-1234/stats", "sentry-api-0-group-stats", False),
    ("/api/0/organizations/orgslug/issues/issue-id-1234/stats", "sentry-api-0-group-stats", False),
    ("/api/0/organizations/orgslug/groups/issue-id-1234/stats", "sentry-api-0-group-stats", False),
    ("/api/0/issues/issue-id-1234/tags", "sentry-api-0-group-tags", False),
    ("/api/0/groups/issue-id-1234/tags", "sentry-api-0-group-tags", False),
    ("/api/0/organizations/orgslug/issues/issue-id-1234/tags", "sentry-api-0-group-tags", False),
    ("/api/0/organizations/orgslug/groups/issue-id-1234/tags", "sentry-api-0-group-tags", False),
    ("/api/0/issues/issue-id-1234/tags/key-12345", "sentry-api-0-group-tag-key-detail", False),
    ("/api/0/groups/issue-id-1234/tags/key-12345", "sentry-api-0-group-tag-key-detail", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/tags/key-12345",
        "sentry-api-0-group-tag-key-detail",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/tags/key-12345",
        "sentry-api-0-group-tag-key-detail",
        False,
    ),
    (
        "/api/0/issues/issue-id-1234/tags/key-12345/values",
        "sentry-api-0-group-tag-key-values",
        False,
    ),
    (
        "/api/0/groups/issue-id-1234/tags/key-12345/values",
        "sentry-api-0-group-tag-key-values",
        False,
    ),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/tags/key-12345/values",
        "sentry-api-0-group-tag-key-values",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/tags/key-12345/values",
        "sentry-api-0-group-tag-key-values",
        False,
    ),
    ("/api/0/issues/issue-id-1234/user-feedback", "sentry-api-0-user-reports", False),
    ("/api/0/groups/issue-id-1234/user-feedback", "sentry-api-0-user-reports", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/user-feedback",
        "sentry-api-0-user-reports",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/user-feedback",
        "sentry-api-0-user-reports",
        False,
    ),
    ("/api/0/issues/issue-id-1234/user-reports", "sentry-api-0-user-reports", False),
    ("/api/0/groups/issue-id-1234/user-reports", "sentry-api-0-user-reports", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/user-reports",
        "sentry-api-0-user-reports",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/user-reports",
        "sentry-api-0-user-reports",
        False,
    ),
    ("/api/0/issues/issue-id-1234/attachments", "sentry-api-0-group-attachments", False),
    ("/api/0/groups/issue-id-1234/attachments", "sentry-api-0-group-attachments", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/attachments",
        "sentry-api-0-group-attachments",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/attachments",
        "sentry-api-0-group-attachments",
        False,
    ),
    ("/api/0/issues/issue-id-1234/similar", "sentry-api-0-group-similar-issues", False),
    ("/api/0/groups/issue-id-1234/similar", "sentry-api-0-group-similar-issues", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/similar",
        "sentry-api-0-group-similar-issues",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/similar",
        "sentry-api-0-group-similar-issues",
        False,
    ),
    ("/api/0/issues/issue-id-1234/external-issues", "external-issues", False),
    ("/api/0/groups/issue-id-1234/external-issues", "external-issues", False),
    ("/api/0/organizations/orgslug/issues/issue-id-1234/external-issues", "external-issues", False),
    ("/api/0/organizations/orgslug/groups/issue-id-1234/external-issues", "external-issues", False),
    (
        "/api/0/issues/issue-id-1234/external-issues/5454",
        "sentry-api-0-group-external-issue-detail",
        False,
    ),
    (
        "/api/0/groups/issue-id-1234/external-issues/5454",
        "sentry-api-0-group-external-issue-detail",
        False,
    ),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/external-issues/5454",
        "sentry-api-0-group-external-issue-detail",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/external-issues/5454",
        "sentry-api-0-group-external-issue-detail",
        False,
    ),
    ("/api/0/issues/issue-id-1234/integrations", "sentry-api-0-group-integrations", False),
    ("/api/0/groups/issue-id-1234/integrations", "sentry-api-0-group-integrations", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/integrations",
        "sentry-api-0-group-integrations",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/integrations",
        "sentry-api-0-group-integrations",
        False,
    ),
    ("/api/0/issues/issue-id-1234/integrations/7412", "integration-details", False),
    ("/api/0/groups/issue-id-1234/integrations/7412", "integration-details", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/integrations/7412",
        "integration-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/integrations/7412",
        "integration-details",
        False,
    ),
    ("/api/0/issues/issue-id-1234/current-release", "sentry-api-0-group-current-release", False),
    ("/api/0/groups/issue-id-1234/current-release", "sentry-api-0-group-current-release", False),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/current-release",
        "sentry-api-0-group-current-release",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/current-release",
        "sentry-api-0-group-current-release",
        False,
    ),
    (
        "/api/0/issues/issue-id-1234/first-last-release",
        "sentry-api-0-group-first-last-release",
        False,
    ),
    (
        "/api/0/groups/issue-id-1234/first-last-release",
        "sentry-api-0-group-first-last-release",
        False,
    ),
    (
        "/api/0/organizations/orgslug/issues/issue-id-1234/first-last-release",
        "sentry-api-0-group-first-last-release",
        False,
    ),
    (
        "/api/0/organizations/orgslug/groups/issue-id-1234/first-last-release",
        "sentry-api-0-group-first-last-release",
        False,
    ),
    # ('/issues/issue-id-1234/plugins?/', '', False),
    # ('/groups/issue-id-1234/plugins?/', '', False),
    # ('/orgslug/issues/issue-id-1234/plugins?/', '', False),
    # ('/orgslug/groups/issue-id-1234/plugins?/', '', False)
    # Relays
    ("/api/0/relays", "sentry-api-0-relays-index", False),
    ("/api/0/relays/register/challenge", "sentry-api-0-relay-register-challenge", False),
    ("/api/0/relays/register/response", "sentry-api-0-relay-register-response", False),
    ("/api/0/relays/projectconfigs", "sentry-api-0-relay-projectconfigs", False),
    ("/api/0/relays/projectids", "sentry-api-0-relay-projectids", False),
    ("/api/0/relays/publickeys", "sentry-api-0-relay-publickeys", False),
    ("/api/0/relays/live", "sentry-api-0-relays-healthcheck", False),
    ("/api/0/relays/relay-12345-id", "sentry-api-0-relays-details", False),
    # API Data
    ("/api/0/assistant", "sentry-api-0-assistant", False),
    ("/api/0/api-applications", "sentry-api-0-api-applications", False),
    ("/api/0/api-applications/app_id-23456", "sentry-api-0-api-application-details", False),
    ("/api/0/api-authorizations", "sentry-api-0-api-authorizations", False),
    ("/api/0/api-tokens", "sentry-api-0-api-tokens", False),
    ("/api/0/prompts-activity", "sentry-api-0-prompts-activity", False),
    # Auth
    ("/api/0/auth", "sentry-api-0-auth", False),
    ("/api/0/auth/config", "sentry-api-0-auth-config", False),
    ("/api/0/auth/login", "sentry-api-0-auth-login", False),
    # Authenticators
    ("/api/0/authenticators", "sentry-api-0-authenticator-index", False),
    # Broadcasts
    ("/api/0/broadcasts", "sentry-api-0-broadcast-index", False),
    ("/api/0/broadcasts/some-broadcast-id-1234", "sentry-api-0-broadcast-detail", False),
    # Project Transfer
    ("/api/0/accept-transfer", "sentry-api-0-accept-project-transfer", False),
    # Organization invite
    (
        "/api/0/accept-invite/member-id-1234/someToken_134-0134",
        "sentry-api-0-accept-organization-invite",
        False,
    ),
    # Monitors
    ("/api/0/monitors/monitor-id-12345", "sentry-api-0-monitor-details", False),
    ("/api/0/monitors/monitor-id-12345/checkins", "sentry-api-0-monitor-check-in-index", False),
    (
        "/api/0/monitors/monitor-id-12345/checkins/checkin-id-12345",
        "sentry-api-0-monitor-check-in-details",
        False,
    ),
    ("/api/0/monitors/monitor-id-12345/stats", "sentry-api-0-monitor-stats", False),
    # Users
    ("/api/0/users", "sentry-api-0-user-index", False),
    ("/api/0/users/user-id-123", "sentry-api-0-user-details", False),
    ("/api/0/users/user-id-123/avatar", "sentry-api-0-user-avatar", False),
    ("/api/0/users/user-id-123/authenticators", "sentry-api-0-user-authenticator-index", False),
    (
        "/api/0/users/user-id-123/authenticators/auth_id-1234/interface_device-id-1234",
        "sentry-api-0-user-authenticator-device-details",
        False,
    ),
    (
        "/api/0/users/user-id-123/authenticators/auth_id-1234",
        "sentry-api-0-user-authenticator-details",
        False,
    ),
    ("/api/0/users/user-id-123/emails", "sentry-api-0-user-emails", False),
    ("/api/0/users/user-id-123/emails/confirm", "sentry-api-0-user-emails-confirm", False),
    (
        "/api/0/users/user-id-123/identities/identity_id-1234",
        "sentry-api-0-user-identity-details",
        False,
    ),
    ("/api/0/users/user-id-123/identities", "sentry-api-0-user-identity", False),
    ("/api/0/users/user-id-123/ips", "sentry-api-0-user-ips", False),
    ("/api/0/users/user-id-123/organizations", "sentry-api-0-user-organizations", False),
    (
        "/api/0/users/user-id-123/notification-settings",
        "sentry-api-0-user-notification-settings",
        False,
    ),
    ("/api/0/users/user-id-123/notifications", "sentry-api-0-user-notifications", False),
    (
        "/api/0/users/user-id-123/notifications/notification_type-1234",
        "sentry-api-0-user-notifications-fine-tuning",
        False,
    ),
    ("/api/0/users/user-id-123/password", "sentry-api-0-user-password", False),
    ("/api/0/users/user-id-123/permissions", "sentry-api-0-user-permissions", False),
    ("/api/0/users/user-id-123/permissions/config", "sentry-api-0-user-permissions-config", False),
    (
        "/api/0/users/user-id-123/permissions/some_permission-name-1234",
        "sentry-api-0-user-permission-details",
        False,
    ),
    ("/api/0/users/user-id-123/roles", "sentry-api-0-user-userroles", False),
    (
        "/api/0/users/user-id-123/roles/some_role-name-1234",
        "sentry-api-0-user-userrole-details",
        False,
    ),
    (
        "/api/0/users/user-id-123/social-identities",
        "sentry-api-0-user-social-identities-index",
        False,
    ),
    (
        "/api/0/users/user-id-123/social-identities/identity_id-1234",
        "sentry-api-0-user-social-identity-details",
        False,
    ),
    ("/api/0/users/user-id-123/subscriptions", "sentry-api-0-user-subscriptions", False),
    (
        "/api/0/users/user-id-123/organization-integrations",
        "sentry-api-0-user-organization-integrations",
        False,
    ),
    ("/api/0/users/user-id-123/user-identities", "sentry-api-0-user-identity-config", False),
    (
        "/api/0/users/user-id-123/user-identities/a-test_category/identity_id-1234",
        "sentry-api-0-user-identity-config-details",
        False,
    ),
    # UserRoles
    ("/api/0/userroles", "sentry-api-0-userroles", False),
    ("/api/0/userroles/role_name-1234", "sentry-api-0-userroles-details", False),
    # Organizations
    ("/api/0/organizations", "sentry-api-0-organizations", False),
    ("/api/0/organizations/orgslug", "sentry-api-0-organization-details", False),
    # Alert Rules
    (
        "/api/0/organizations/orgslug/alert-rules/available-actions",
        "sentry-api-0-organization-alert-rule-available-actions",
        False,
    ),
    (
        "/api/0/organizations/orgslug/alert-rules/alert_rule_id-1234",
        "sentry-api-0-organization-alert-rule-details",
        False,
    ),
    ("/api/0/organizations/orgslug/alert-rules", "sentry-api-0-organization-alert-rules", False),
    (
        "/api/0/organizations/orgslug/combined-rules",
        "sentry-api-0-organization-combined-rules",
        False,
    ),
    # Data Export
    ("/api/0/organizations/orgslug/data-export", "sentry-api-0-organization-data-export", False),
    (
        "/api/0/organizations/orgslug/data-export/data_export-id-1234",
        "sentry-api-0-organization-data-export-details",
        False,
    ),
    # Incidents
    (
        "/api/0/organizations/orgslug/incidents/inc_id-1234/activity",
        "sentry-api-0-organization-incident-activity",
        False,
    ),
    (
        "/api/0/organizations/orgslug/incidents/inc_id-1234/comments",
        "sentry-api-0-organization-incident-comments",
        False,
    ),
    (
        "/api/0/organizations/orgslug/incidents/inc_id-1234/comments/activity_id-1234",
        "sentry-api-0-organization-incident-comment-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/incidents/inc_id-1234",
        "sentry-api-0-organization-incident-details",
        False,
    ),
    ("/api/0/organizations/orgslug/incidents", "sentry-api-0-organization-incident-index", False),
    (
        "/api/0/organizations/orgslug/incidents/inc_id-1234/seen",
        "sentry-api-0-organization-incident-seen",
        False,
    ),
    (
        "/api/0/organizations/orgslug/incidents/inc_id-1234/subscriptions",
        "sentry-api-0-organization-incident-subscription-index",
        False,
    ),
    ("/api/0/organizations/orgslug/chunk-upload", "sentry-api-0-chunk-upload", False),
    # Code Path Mappings
    (
        "/api/0/organizations/orgslug/code-mappings",
        "sentry-api-0-organization-code-mappings",
        False,
    ),
    (
        "/api/0/organizations/orgslug/code-mappings/config_id-1234",
        "sentry-api-0-organization-code-mapping-details",
        False,
    ),
    # Codeowners
    (
        "/api/0/organizations/orgslug/code-mappings/config_id-1234/codeowners",
        "sentry-api-0-organization-code-mapping-codeowners",
        False,
    ),
    (
        "/api/0/organizations/orgslug/codeowners-associations",
        "sentry-api-0-organization-codeowners-associations",
        False,
    ),
    # Discover
    ("/api/0/organizations/orgslug/discover/query", "sentry-api-0-discover-query", False),
    ("/api/0/organizations/orgslug/discover/saved", "sentry-api-0-discover-saved-queries", False),
    (
        "/api/0/organizations/orgslug/discover/saved/123456",
        "sentry-api-0-discover-saved-query-detail",
        False,
    ),
    (
        "/api/0/organizations/orgslug/discover/saved/123456/visit",
        "sentry-api-0-discover-saved-query-visit",
        False,
    ),
    (
        "/api/0/organizations/orgslug/key-transactions",
        "sentry-api-0-organization-key-transactions",
        False,
    ),
    (
        "/api/0/organizations/orgslug/key-transactions-list",
        "sentry-api-0-organization-key-transactions-list",
        False,
    ),
    (
        "/api/0/organizations/orgslug/related-issues",
        "sentry-api-0-organization-related-issues",
        False,
    ),
    (
        "/api/0/organizations/orgslug/project-transaction-threshold-override",
        "sentry-api-0-organization-project-transaction-threshold-override",
        False,
    ),
    # Dashboards
    ("/api/0/organizations/orgslug/dashboards", "sentry-api-0-organization-dashboards", False),
    (
        "/api/0/organizations/orgslug/dashboards/widgets",
        "sentry-api-0-organization-dashboard-widget-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/dashboards/dashboard_id-1234",
        "sentry-api-0-organization-dashboard-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/dashboards/dashboard_id-1234/visit",
        "sentry-api-0-organization-dashboard-visit",
        False,
    ),
    ("/api/0/organizations/orgslug/shortids/short_id-1234", "sentry-api-0-short-id-lookup", False),
    ("/api/0/organizations/orgslug/eventids/123456789", "sentry-api-0-event-id-lookup", False),
    (
        "/api/0/organizations/orgslug/data-scrubbing-selector-suggestions",
        "sentry-api-0-data-scrubbing-selector-suggestions",
        False,
    ),
    ("/api/0/organizations/orgslug/slugs", "sentry-api-0-short-ids-update", False),
    (
        "/api/0/organizations/orgslug/access-requests",
        "sentry-api-0-organization-access-requests",
        False,
    ),
    (
        "/api/0/organizations/orgslug/access-requests/1234567",
        "sentry-api-0-organization-access-request-details",
        False,
    ),
    ("/api/0/organizations/orgslug/activity", "sentry-api-0-organization-activity", False),
    ("/api/0/organizations/orgslug/api-keys", "sentry-api-0-organization-api-key-index", False),
    (
        "/api/0/organizations/orgslug/api-keys/api_key_id-12345",
        "sentry-api-0-organization-api-key-details",
        False,
    ),
    ("/api/0/organizations/orgslug/audit-logs", "sentry-api-0-organization-audit-logs", False),
    (
        "/api/0/organizations/orgslug/auth-provider",
        "sentry-api-0-organization-auth-provider",
        False,
    ),
    (
        "/api/0/organizations/orgslug/auth-providers",
        "sentry-api-0-organization-auth-providers",
        False,
    ),
    (
        "/api/0/organizations/orgslug/auth-provider/send-reminders",
        "sentry-api-0-organization-auth-provider-send-reminders",
        False,
    ),
    ("/api/0/organizations/orgslug/avatar", "sentry-api-0-organization-avatar", False),
    (
        "/api/0/organizations/orgslug/config/integrations",
        "sentry-api-0-organization-config-integrations",
        False,
    ),
    (
        "/api/0/organizations/orgslug/config/repos",
        "sentry-api-0-organization-config-repositories",
        False,
    ),
    ("/api/0/organizations/orgslug/sdk-updates", "sentry-api-0-organization-sdk-updates", False),
    (
        "/api/0/organizations/orgslug/has-mobile-app-events",
        "sentry-api-0-organization-has-mobile-events",
        False,
    ),
    # TODO add an alias for /organizations/:slug/events/ and deprecate eventsv2
    ("/api/0/organizations/orgslug/eventsv2", "sentry-api-0-organization-eventsv2", False),
    # TODO (mdtro): this is some interesting regex for a URL path?
    #  r"^(?P<organization_slug>[^\/]+)/events/(?P<project_slug>[^\/]+):(?P<event_id>(?:\d+|[A-Fa-f0-9-]{32,36}))/$",
    (
        "/api/0/organizations/orgslug/events/projectslug:1234",
        "sentry-api-0-organization-event-details",
        False,
    ),
    ("/api/0/organizations/orgslug/events-stats", "sentry-api-0-organization-events-stats", False),
    ("/api/0/organizations/orgslug/events-geo", "sentry-api-0-organization-events-geo", False),
    (
        "/api/0/organizations/orgslug/events-facets",
        "sentry-api-0-organization-events-facets",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-facets-performance",
        "sentry-api-0-organization-events-facets-performance",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-facets-performance-histogram",
        "sentry-api-0-organization-events-facets-performance-histogram",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-span-ops",
        "sentry-api-0-organization-events-span-ops",
        False,
    ),
    ("/api/0/organizations/orgslug/events-spans", "sentry-api-0-organization-events-spans", False),
    (
        "/api/0/organizations/orgslug/events-spans-performance",
        "sentry-api-0-organization-events-spans-performance",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-spans-stats",
        "sentry-api-0-organization-events-spans-stats",
        False,
    ),
    ("/api/0/organizations/orgslug/events-meta", "sentry-api-0-organization-events-meta", False),
    (
        "/api/0/organizations/orgslug/events-histogram",
        "sentry-api-0-organization-events-histogram",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-spans-histogram",
        "sentry-api-0-organization-events-spans-histogram",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-trends",
        "sentry-api-0-organization-events-trends",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-vitals",
        "sentry-api-0-organization-events-vitals",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-has-measurements",
        "sentry-api-0-organization-events-has-measurements",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-trends-stats",
        "sentry-api-0-organization-events-trends-stats",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-trace-light/12345678",
        "sentry-api-0-organization-events-trace-light",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-trace/12345678",
        "sentry-api-0-organization-events-trace",
        False,
    ),
    (
        "/api/0/organizations/orgslug/events-trace-meta/12345678",
        "sentry-api-0-organization-events-trace-meta",
        False,
    ),
    ("/api/0/organizations/orgslug/issues", "sentry-api-0-organization-group-index", False),
    ("/api/0/organizations/orgslug/issues-count", "sentry-api-0-organization-issues-count", False),
    (
        "/api/0/organizations/orgslug/issues-stats",
        "sentry-api-0-organization-group-index-stats",
        False,
    ),
    ("/api/0/organizations/orgslug/integrations", "sentry-api-0-organization-integrations", False),
    (
        "/api/0/organizations/orgslug/integrations/integration_id-1234",
        "sentry-api-0-organization-integration-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/integrations/integration_id-1234/repos",
        "sentry-api-0-organization-integration-repos",
        False,
    ),
    (
        "/api/0/organizations/orgslug/integrations/integration_id-1234/serverless-functions",
        "sentry-api-0-organization-integration-serverless-functions",
        False,
    ),
    ("/api/0/organizations/orgslug/members", "sentry-api-0-organization-member-index", False),
    (
        "/api/0/organizations/orgslug/external-users",
        "sentry-api-0-organization-external-user",
        False,
    ),
    (
        "/api/0/organizations/orgslug/external-users/external_user_id-1234",
        "sentry-api-0-organization-external-user-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/integration-requests",
        "sentry-api-0-organization-integration-request",
        False,
    ),
    (
        "/api/0/organizations/orgslug/invite-requests",
        "sentry-api-0-organization-invite-request-index",
        False,
    ),
    (
        "/api/0/organizations/orgslug/invite-requests/member-id_1234",
        "sentry-api-0-organization-invite-request-detail",
        False,
    ),
    ("/api/0/organizations/orgslug/monitors", "sentry-api-0-organization-monitors", False),
    (
        "/api/0/organizations/orgslug/pinned-searches",
        "sentry-api-0-organization-pinned-searches",
        False,
    ),
    (
        "/api/0/organizations/orgslug/recent-searches",
        "sentry-api-0-organization-recent-searches",
        False,
    ),
    (
        "/api/0/organizations/orgslug/searches/search_id-1234",
        "sentry-api-0-organization-search-details",
        False,
    ),
    ("/api/0/organizations/orgslug/searches", "sentry-api-0-organization-searches", False),
    ("/api/0/organizations/orgslug/sessions", "sentry-api-0-organization-sessions", False),
    ("/api/0/organizations/orgslug/users/issues", "sentry-api-0-organization-issue-search", False),
    (
        "/api/0/organizations/orgslug/users/user_id-123/issues",
        "sentry-api-0-organization-user-issues",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/resolved",
        "sentry-api-0-organization-release-resolved",
        False,
    ),
    (
        "/api/0/organizations/orgslug/members/member-id_1234",
        "sentry-api-0-organization-member-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/members/member-id_1234/unreleased-commits",
        "sentry-api-0-organization-member-unreleased-commits",
        False,
    ),
    (
        "/api/0/organizations/orgslug/members/member-id_1234/issues/assigned",
        "sentry-api-0-organization-member-issues-assigned",
        False,
    ),
    (
        "/api/0/organizations/orgslug/members/member-id_1234/issues/bookmarked",
        "sentry-api-0-organization-member-issues-bookmarked",
        False,
    ),
    (
        "/api/0/organizations/orgslug/members/member-id_1234/issues/viewed",
        "sentry-api-0-organization-member-issues-viewed",
        False,
    ),
    (
        "/api/0/organizations/orgslug/members/member-id_1234/teams/team_slug-123",
        "sentry-api-0-organization-member-team-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/processingissues",
        "sentry-api-0-organization-processing-issues",
        False,
    ),
    ("/api/0/organizations/orgslug/projects", "sentry-api-0-organization-projects", False),
    (
        "/api/0/organizations/orgslug/projects-count",
        "sentry-api-0-organization-projects-count",
        False,
    ),
    (
        "/api/0/organizations/orgslug/sent-first-event",
        "sentry-api-0-organization-sent-first-event",
        False,
    ),
    ("/api/0/organizations/orgslug/repos", "sentry-api-0-organization-repositories", False),
    (
        "/api/0/organizations/orgslug/repos/repo_id-123",
        "sentry-api-0-organization-repository-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/repos/repo_id-123/commits",
        "sentry-api-0-organization-repository-commits",
        False,
    ),
    ("/api/0/organizations/orgslug/plugins", "sentry-api-0-organization-plugins", False),
    (
        "/api/0/organizations/orgslug/plugins/configs",
        "sentry-api-0-organization-plugins-configs",
        False,
    ),
    ("/api/0/organizations/orgslug/releases", "sentry-api-0-organization-releases", False),
    (
        "/api/0/organizations/orgslug/releases/stats",
        "sentry-api-0-organization-releases-stats",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123",
        "sentry-api-0-organization-release-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/meta",
        "sentry-api-0-organization-release-meta",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/assemble",
        "sentry-api-0-organization-release-assemble",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/files",
        "sentry-api-0-organization-release-files",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/files/file_id-1234",
        "sentry-api-0-organization-release-file-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/commitfiles",
        "sentry-api-0-release-commitfilechange",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/deploys",
        "sentry-api-0-organization-release-deploys",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/commits",
        "sentry-api-0-organization-release-commits",
        False,
    ),
    (
        "/api/0/organizations/orgslug/releases/version-123/previous-with-commits",
        "sentry-api-0-organization-release-previous-with-commits",
        False,
    ),
    (
        "/api/0/organizations/orgslug/user-feedback",
        "sentry-api-0-organization-user-feedback",
        False,
    ),
    ("/api/0/organizations/orgslug/user-teams", "sentry-api-0-organization-user-teams", False),
    ("/api/0/organizations/orgslug/users", "sentry-api-0-organization-users", False),
    (
        "/api/0/organizations/orgslug/users/user_id-123",
        "sentry-api-0-organization-user-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/sentry-app-installations",
        "sentry-api-0-sentry-app-installations",
        False,
    ),
    ("/api/0/organizations/orgslug/sentry-apps", "sentry-api-0-organization-sentry-apps", False),
    ("/api/0/organizations/orgslug/stats", "sentry-api-0-organization-stats", False),
    ("/api/0/organizations/orgslug/stats_v2", "sentry-api-0-organization-stats-v2", False),
    ("/api/0/organizations/orgslug/teams", "sentry-api-0-organization-teams", False),
    ("/api/0/organizations/orgslug/tags", "sentry-api-0-organization-tags", False),
    (
        "/api/0/organizations/orgslug/tags/tagkey_123/values",
        "sentry-api-0-organization-tagkey-values",
        False,
    ),
    (
        "/api/0/organizations/orgslug/onboarding-tasks",
        "sentry-api-0-organization-onboardingtasks",
        False,
    ),
    ("/api/0/organizations/orgslug/environments", "sentry-api-0-organization-environments", False),
    ("/api/0/organizations/orgslug/broadcasts", "sentry-api-0-organization-broadcasts", False),
    ("/api/0/organizations/orgslug/join-request", "sentry-api-0-organization-join-request", False),
    (
        "/api/0/organizations/orgslug/transaction-anomaly-detection",
        "sentry-api-0-organization-transaction-anomaly-detection",
        False,
    ),
    # relay usage
    ("/api/0/organizations/orgslug/relay_usage", "sentry-api-0-organization-relay-usage", False),
    (
        "/api/0/organizations/orgslug/request-project-creation",
        "sentry-api-0-organization-request-project-creation",
        False,
    ),
    (
        "/api/0/organizations/orgslug/scim/v2/Users",
        "sentry-api-0-organization-scim-member-index",
        False,
    ),
    (
        "/api/0/organizations/orgslug/scim/v2/Users/1234",
        "sentry-api-0-organization-scim-member-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/scim/v2/Groups",
        "sentry-api-0-organization-scim-team-index",
        False,
    ),
    (
        "/api/0/organizations/orgslug/scim/v2/Groups/123456",
        "sentry-api-0-organization-scim-team-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/scim/v2/Schemas",
        "sentry-api-0-organization-scim-schema-index",
        False,
    ),
    ("/api/0/organizations/orgslug/metrics/meta", "sentry-api-0-organization-metrics-index", False),
    (
        "/api/0/organizations/orgslug/metrics/meta/metric_name-1234",
        "sentry-api-0-organization-metric-details",
        False,
    ),
    ("/api/0/organizations/orgslug/metrics/data", "sentry-api-0-organization-metrics-data", False),
    ("/api/0/organizations/orgslug/metrics/tags", "sentry-api-0-organization-metrics-tags", False),
    (
        "/api/0/organizations/orgslug/metrics/tags/tag_name-1234",
        "sentry-api-0-organization-metrics-tag-details",
        False,
    ),
    (
        "/api/0/organizations/orgslug/profiling/profiles",
        "sentry-api-0-organization-profiling-profiles",
        False,
    ),
    (
        "/api/0/organizations/orgslug/profiling/filters",
        "sentry-api-0-organization-profiling-filters",
        False,
    ),
    (
        "/api/0/organizations/orgslug/client-state",
        "sentry-api-0-organization-client-state-list",
        False,
    ),
    (
        "/api/0/organizations/orgslug/client-state/category_1234-2",
        "sentry-api-0-organization-client-state",
        False,
    ),
    # Top Level App Installs
    (
        "/api/0/sentry-app-installations/8B97CF20-6B23-42A1-BB6B-87706C99ADEE",
        "sentry-api-0-sentry-app-installation-details",
        False,
    ),
    (
        "/api/0/sentry-app-installations/8B97CF20-6B23-42A1-BB6B-87706C99ADEE/external-requests",
        "sentry-api-0-sentry-app-installation-external-requests",
        False,
    ),
    (
        "/api/0/sentry-app-installations/8B97CF20-6B23-42A1-BB6B-87706C99ADEE/external-issue-actions",
        "sentry-api-0-sentry-app-installation-external-issue-actions",
        False,
    ),
    (
        "/api/0/sentry-app-installations/8B97CF20-6B23-42A1-BB6B-87706C99ADEE/external-issues",
        "sentry-api-0-sentry-app-installation-external-issues",
        False,
    ),
    (
        "/api/0/sentry-app-installations/8B97CF20-6B23-42A1-BB6B-87706C99ADEE/external-issues/external_issue-id-123",
        "sentry-api-0-sentry-app-installation-external-issue-details",
        False,
    ),
]


@pytest.mark.url_resolve
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
