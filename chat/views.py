import logging
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.models import Step
from .llm import LLMError, generate_text
from .models import StepMessage
from .prompts import STEP_SYSTEM_PROMPT, build_step_messages

logger = logging.getLogger(__name__)

class GenerateStepContentView(APIView):
    def post(self, request, step_id):
        step = get_object_or_404(
            Step.objects.select_related("project"),
            pk=step_id,
            project__user=request.user,
        )
        
        force = request.data.get("force") is True
        if step.content and not force:
            return Response({"id": step.id, "content": step.content, "generated": False})

        previous_titles = list(
            Step.objects.filter(
                project=step.project,
                section=step.section,
                order__lt=step.order,
            ).values_list("title", flat=True)
        )

        try:
            text = generate_text(
                STEP_SYSTEM_PROMPT,
                build_step_messages(step.project, step, previous_titles),
            )
        except LLMError:
            logger.exception("LLM call failed for step %s", step.id)
            return Response(
                {"error": "Could not generate content right now. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        step.content = text
        step.save(update_fields=["content"])
        step.project.save(update_fields=["updated_at"])
        
        return Response({"id": step.id, "content": step.content, "generated": True})


class StepChatView(APIView):
    def post(self, request, step_id):
        step = get_object_or_404(
            Step.objects.select_related("project"),
            pk=step_id,
            project__user=request.user,
        )
        
        user_message = request.data.get("message", "").strip()
        if not user_message:
            return Response({"error": "Message cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        StepMessage.objects.create(step=step, user=request.user, role="user", content=user_message)

        # Fetch previous chat history for context
        history = StepMessage.objects.filter(step=step, user=request.user)
        messages_payload = [{"role": msg.role, "content": msg.content} for msg in history]

        chat_system_prompt = (
            f"You are a helpful programming mentor assisting a beginner with the step: '{step.title}' "
            f"in the project '{step.project.name}'. Answer questions clearly and concisely."
        )

        try:
            ai_response_text = generate_text(chat_system_prompt, messages_payload)
        except LLMError:
            return Response({"error": "Failed to get response from AI."}, status=status.HTTP_502_BAD_GATEWAY)

        # Save assistant response
        StepMessage.objects.create(step=step, user=request.user, role="assistant", content=ai_response_text)

        return Response({
            "user_message": user_message,
            "assistant_response": ai_response_text
        }, status=status.HTTP_200_OK)