
from django.contrib import admin
from django.urls import path , include
from FinanceTracker import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/",include("rest_framework.urls")),
    path("api/",include("FinanceTracker.api.urls"))
]
