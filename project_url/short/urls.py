from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Shorturl', views.Urlviewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)), #使用router
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
