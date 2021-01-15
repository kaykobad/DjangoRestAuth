from rest_framework import routers
from .views import AuthViewSet

router = routers.DefaultRouter()
router.register('auth', AuthViewSet, basename='authentication')

urlpatterns = router.urls
