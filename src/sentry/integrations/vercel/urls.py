from django.urls import re_path

from sentry.web.frontend.vercel_extension_configuration import VercelExtensionConfigurationView

from .generic_webhook import VercelGenericWebhookEndpoint
from .webhook import VercelWebhookEndpoint

urlpatterns = [
    re_path(
        r"^webhook/?$", VercelWebhookEndpoint.as_view(), name="sentry-extensions-vercel-webhook"
    ),
    re_path(
        r"^configure/?$",
        VercelExtensionConfigurationView.as_view(),
        name="sentry-extensions-vercel-configure",
    ),
    # XXX(meredith): This route has become our generic hook, in
    # the future we'll need to update the route name to reflect that.
    re_path(
        r"^delete/?$",
        VercelGenericWebhookEndpoint.as_view(),
        name="sentry-extensions-vercel-generic-webhook",
    ),
]
