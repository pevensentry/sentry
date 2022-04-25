from django.urls import re_path

from .metadata import CloudflareMetadataEndpoint
from .webhook import CloudflareWebhookEndpoint

urlpatterns = [
    re_path(
        r"^metadata/?$",
        CloudflareMetadataEndpoint.as_view(),
        name="sentry-extensions-cloudflare-metadata",
    ),
    re_path(
        r"^webhook/?$",
        CloudflareWebhookEndpoint.as_view(),
        name="sentry-extensions-cloudflare-webhook",
    ),
]
