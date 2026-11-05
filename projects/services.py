from django.db import transaction

from .models import Project, Step

START_STEPS = [
    "Install Python",
    "Install VS Code",
    "Create the project folder",
    "Create a virtual environment",
    "Install Django and packages",
    "Create the Django project",
]


@transaction.atomic
def create_project_with_start_steps(user, name):
    project = Project.objects.create(user=user, name=name)
    Step.objects.bulk_create(
        [
            Step(
                project=project,
                section=Step.Section.START,
                title=title,
                order=index,
            )
            for index, title in enumerate(START_STEPS, start=1)
        ]
    )
    return project