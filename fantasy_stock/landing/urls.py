from django.urls import path

import landing.views


urlpatterns = [
    path("", landing.views.index)
]