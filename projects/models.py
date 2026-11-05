from django.conf import settings
from django.db import models


class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name


class Step(models.Model):
    class Section(models.TextChoices):
        START = "start", "Start"
        BUILD = "build", "Build"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    section = models.CharField(max_length=10, choices=Section.choices)
    title = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)
    content = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ["section", "order"]

    def __str__(self):
        return f"{self.project.name} - {self.title}"