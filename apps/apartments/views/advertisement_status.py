from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.advertisements import Advertisement
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer


class ToggleAdvertisementStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name='AdvertisementStatusResponse',
                fields={
                    'status': serializers.CharField(),
                    'is_active': serializers.BooleanField(),
                },
            ),
            404: inline_serializer(
                name='AdvertisementStatusErrorResponse',
                fields={
                    'error': serializers.CharField(),
                },
            ),
        },
    )

    def post(self, request, pk):
        try:
            advertisement = Advertisement.objects.get(pk=pk, owner=request.user)
        except Advertisement.DoesNotExist:
            return Response({"error": "Advertisement not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)

        advertisement.is_active = not advertisement.is_active
        advertisement.save()

        return Response({"status": "success", "is_active": advertisement.is_active}, status=status.HTTP_200_OK)
