from django.conf.urls import re_path

from .webhook import GitHubEnterpriseWebhookEndpoint

urlpatterns = [
    re_path(
        r"^webhook/?$",
        GitHubEnterpriseWebhookEndpoint.as_view(),
        name="sentry-extensions-githubenterprise-webhook",
    )
]
