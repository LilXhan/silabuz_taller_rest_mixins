from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()

router.register(r'todo', api.TodoViewSet, basename='todo')

urlpatterns = router.urls