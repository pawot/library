from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path, include
from django.conf import settings
from strawberry.django.views import GraphQLView

from api.schema import schema


urlpatterns = [
    path("accounts/", include(("accounts.urls", "accounts"))),
    path("auth/", include(("auth.urls", "auth"))),
    path("bookcase/", include(("bookcase.urls", "books"))),
    path("graphql/", GraphQLView.as_view(schema=schema)),

]

if settings.DEBUG:

    urlpatterns += [
        path("docs/openapi/", SpectacularAPIView.as_view(), name="schema"),
        path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    ]
