from django.urls import path
from .views import GenerateStepContentView,StepChatView

urlpatterns = [
    path("steps/<int:step_id>/generate/", GenerateStepContentView.as_view(), name="generate-step-content"),
    path("steps/<int:step_id>/chat/", StepChatView.as_view(), name="step-chat"),
]