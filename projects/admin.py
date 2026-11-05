from django.contrib import admin

from .models import Project, Step


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "updated_at")


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "section", "order", "is_done")
    list_filter = ("section", "is_done")