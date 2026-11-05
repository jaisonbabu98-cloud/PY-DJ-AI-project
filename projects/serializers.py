from rest_framework import serializers

from .models import Project, Step


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ("id", "project", "section", "title", "order", "content", "is_done")
        read_only_fields = ("project", "section", "title", "order", "content")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def validate_name(self, value):
        user = self.context["request"].user
        existing = Project.objects.filter(user=user, name__iexact=value)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError("You already have a project with this name.")
        return value


class ProjectDetailSerializer(ProjectSerializer):
    steps = StepSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ("steps",)