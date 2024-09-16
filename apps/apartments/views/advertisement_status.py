from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.advertisements import Advertisement


class ToggleAdvertisementStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            advertisement = Advertisement.objects.get(pk=pk, owner=request.user)
        except Advertisement.DoesNotExist:
            return Response({"error": "Advertisement not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)

        advertisement.is_active = not advertisement.is_active
        advertisement.save()

        return Response({"status": "success", "is_active": advertisement.is_active}, status=status.HTTP_200_OK)
