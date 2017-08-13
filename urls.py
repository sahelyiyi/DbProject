from django.conf.urls import url

from anbardari.views import helloworld

urlpatterns = {
    url(r'^helloworld/?$', helloworld),
}
