from django.conf.urls import url

from anbardari.views import health_check

urlpatterns = {
    url(r'^health/?$', health_check),
}
