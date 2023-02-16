from rest_framework.routers import DefaultRouter

from .api import TodoViewSet

router = DefaultRouter()

router.register(r'todo', TodoViewSet, basename='todosCustom')

api_urlpatterns = router.urls