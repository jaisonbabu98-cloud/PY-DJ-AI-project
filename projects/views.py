from rest_framework import mixins, viewsets

from .models import Project, Step
from .serializers import ProjectDetailSerializer, ProjectSerializer, StepSerializer
from .services import create_project_with_start_steps


class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Project.objects.filter(user=self.request.user)
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("steps")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProjectDetailSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.instance = create_project_with_start_steps(
            self.request.user,
            serializer.validated_data["name"],
        )


class StepViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StepSerializer
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        queryset = Step.objects.filter(project__user=self.request.user)
        project_id = self.request.query_params.get("project")
        if project_id is not None:
            if not project_id.isdigit():
                return queryset.none()
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_update(self, serializer):
        step = serializer.save()
        step.project.save(update_fields=["updated_at"])