from django.contrib import admin
from django.urls import path, include
from learn_algoritms_bot import urls as alg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('learn_algoritms_bot/', include(alg)),
]
