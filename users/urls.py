from .routers import CustomRouter

from .api import UserViewSet, UserOneViewSet, UserCreateView, UserUpdateViewSet

router = CustomRouter()

router.register('users/', UserViewSet, basename='users')
router.register('users', UserOneViewSet, basename='userOne')
router.register(r'', UserCreateView, basename='user')
router.register('users', UserUpdateViewSet, basename='user')

urlpatterns = router.urls