from rest_framework.routers import SimpleRouter

from .views import ProjectViewSet, StepViewSet

router = SimpleRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("steps", StepViewSet, basename="step")

urlpatterns = router.urls