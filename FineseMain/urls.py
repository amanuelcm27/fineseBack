
from django.contrib import admin
from django.urls import path , include
from django.views.generic import RedirectView
from FinanceTracker import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/",include("rest_framework.urls")),
    path("api/",include("FinanceTracker.api.urls")),
    path('', RedirectView.as_view(url='/api/', permanent=True))
]
