from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EmailSerializer, SignupSerializer, VerifyOTPSerializer
from .services import send_otp, verify_otp

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_otp(user)
        return Response(
            {"detail": "Account created. An OTP has been sent to your email."},
            status=status.HTTP_201_CREATED,
        )


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email__iexact=email, is_email_verified=False)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST
            )

        ok, message = verify_otp(user, code)
        return Response(
            {"detail": message},
            status=status.HTTP_200_OK if ok else status.HTTP_400_BAD_REQUEST,
        )


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.filter(email__iexact=email, is_email_verified=False).first()
        if user:
            send_otp(user)
        return Response(
            {"detail": "If the account exists, a new OTP has been sent."}
        )