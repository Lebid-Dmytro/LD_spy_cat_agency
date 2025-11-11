from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CatViewSet, MissionViewSet, TargetViewSet


router = DefaultRouter()
router.register(r"cats", CatViewSet, basename="cat")
router.register(r"missions", MissionViewSet, basename="mission")
router.register(r"targets", TargetViewSet, basename="target")

urlpatterns = [
    path("", include(router.urls)),
]
