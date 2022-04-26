from django.urls import re_path

from .views import JiraExtensionConfigurationView, JiraIssueHookView, JiraUiHookView
from .webhooks import (
    JiraDescriptorEndpoint,
    JiraInstalledEndpoint,
    JiraIssueUpdatedWebhook,
    JiraSearchEndpoint,
    JiraUninstalledEndpoint,
)

urlpatterns = [
    re_path(r"^ui-hook/?$", JiraUiHookView.as_view(), name="sentry-extensions-jira-uihook"),
    re_path(
        r"^descriptor/?$",
        JiraDescriptorEndpoint.as_view(),
        name="sentry-extensions-jira-descriptor",
    ),
    re_path(
        r"^installed/?$", JiraInstalledEndpoint.as_view(), name="sentry-extensions-jira-installed"
    ),
    re_path(
        r"^uninstalled/?$",
        JiraUninstalledEndpoint.as_view(),
        name="sentry-extensions-jira-uninstalled",
    ),
    re_path(
        r"^issue-updated/?$",
        JiraIssueUpdatedWebhook.as_view(),
        name="sentry-extensions-jira-issue-updated",
    ),
    re_path(
        r"^search/(?P<organization_slug>[^\/]+)/(?P<integration_id>\d+)/?$",
        JiraSearchEndpoint.as_view(),
        name="sentry-extensions-jira-search",
    ),
    re_path(
        r"^configure/?$",
        JiraExtensionConfigurationView.as_view(),
        name="sentry-extensions-jira-configure",
    ),
    re_path(
        r"^issue/(?P<issue_key>[^\/]+)/?$",
        JiraIssueHookView.as_view(),
        name="sentry-extensions-jira-issue-hook",
    ),
]
