from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.apartments.models import Advertisement
from apps.apartments.models.view_advertisement import AdvertisementView
from apps.users.models import User


class AdvertisementTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="apartment_owner@example.com",
            password="TestPassword123!",
            username="apartment_owner",
            first_name="Apartment",
            last_name="Owner",
        )

        self.other_user = User.objects.create_user(
            email="other_user@example.com",
            password="TestPassword123!",
            username="other_user",
            first_name="Other",
            last_name="User",
        )

        self.advertisement = Advertisement.objects.create(
            owner=self.owner,
            title="Test Apartment",
            description="Apartment used in automatic tests",
            price_per_night="65.00",
            city="Huckelhoven",
            street="Teststrasse",
            house_number="10",
            rooms=2,
            properties="APARTMENT",
        )

        self.list_url = reverse("advertisements")
        self.detail_url = reverse(
            "advertisement-detail",
            kwargs={"pk": self.advertisement.pk},
        )

        self.create_data = {
            "title": "New Apartment",
            "description": "New apartment description",
            "price_per_night": "75.00",
            "city": "Huckelhoven",
            "street": "Otherstrasse",
            "house_number": "20",
            "rooms": 3,
            "properties": "APARTMENT",
        }

    def test_anonymous_user_can_view_advertisement_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_anonymous_user_cannot_create_advertisement(self):
        response = self.client.post(
            self.list_url,
            self.create_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(Advertisement.objects.count(), 1)

    def test_authenticated_user_can_create_advertisement(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            self.list_url,
            self.create_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Advertisement.objects.count(), 2)

        created_advertisement = Advertisement.objects.get(
            title="New Apartment"
        )

        self.assertEqual(created_advertisement.owner, self.other_user)

    def test_authenticated_view_increases_counter_and_saves_history(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(self.detail_url)

        self.advertisement.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.advertisement.view_count, 1)
        self.assertTrue(
            AdvertisementView.objects.filter(
                user=self.other_user,
                advertisement=self.advertisement,
            ).exists()
        )

    def test_owner_can_update_advertisement(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated Apartment"},
            format="json",
        )

        self.advertisement.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.advertisement.title,
            "Updated Apartment",
        )

    def test_other_user_cannot_update_advertisement(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.patch(
            self.detail_url,
            {"title": "Unauthorized Update"},
            format="json",
        )

        self.advertisement.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.advertisement.title, "Test Apartment")

    def test_other_user_cannot_delete_advertisement(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Advertisement.objects.filter(
                pk=self.advertisement.pk
            ).exists()
        )

    def test_owner_can_delete_advertisement(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Advertisement.objects.filter(
                pk=self.advertisement.pk
            ).exists()
        )
