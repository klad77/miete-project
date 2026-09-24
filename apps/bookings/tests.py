from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.apartments.models import Advertisement
from apps.bookings.models import Booking
from apps.users.models import User


class BookingCreateTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com",
            password="TestPassword123!",
            username="test_owner",
            first_name="Test",
            last_name="Owner",
        )

        self.tenant = User.objects.create_user(
            email="tenant@example.com",
            password="TestPassword123!",
            username="test_tenant",
            first_name="Test",
            last_name="Tenant",
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

        self.url = reverse("create-booking")
        self.client.force_authenticate(user=self.tenant)

        self.start_date = timezone.now().date() + timedelta(days=10)
        self.end_date = self.start_date + timedelta(days=2)

    def test_authenticated_user_can_create_booking(self):
        data = {
            "advertisement": self.advertisement.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.get()
        self.assertEqual(booking.user, self.tenant)
        self.assertEqual(booking.advertisement, self.advertisement)
        self.assertEqual(booking.status, Booking.PENDING)

    def test_overlapping_booking_is_rejected(self):
        Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        data = {
            "advertisement": self.advertisement.id,
            "start_date": self.start_date + timedelta(days=1),
            "end_date": self.end_date + timedelta(days=1),
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertIn("non_field_errors", response.data)

    def test_checkout_date_can_be_used_as_next_checkin(self):
        Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        data = {
            "advertisement": self.advertisement.id,
            "start_date": self.end_date,
            "end_date": self.end_date + timedelta(days=2),
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)

class BookingCancellationTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner_cancel@example.com",
            password="TestPassword123!",
            username="cancel_owner",
            first_name="Test",
            last_name="Owner",
        )

        self.tenant = User.objects.create_user(
            email="tenant_cancel@example.com",
            password="TestPassword123!",
            username="cancel_tenant",
            first_name="Test",
            last_name="Tenant",
        )

        self.other_tenant = User.objects.create_user(
            email="other_tenant@example.com",
            password="TestPassword123!",
            username="other_tenant",
            first_name="Other",
            last_name="Tenant",
        )

        self.advertisement = Advertisement.objects.create(
            owner=self.owner,
            title="Cancellation Test Apartment",
            description="Apartment used for cancellation tests",
            price_per_night="75.00",
            city="Huckelhoven",
            street="Teststrasse",
            house_number="20",
            rooms=2,
            properties="APARTMENT",
        )

    def create_booking(self, days_until_start):
        start_date = timezone.now().date() + timedelta(
            days=days_until_start
        )

        return Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=start_date,
            end_date=start_date + timedelta(days=2),
        )

    def test_booking_can_be_canceled_two_days_before_start(self):
        booking = self.create_booking(days_until_start=2)
        self.client.force_authenticate(user=self.tenant)

        url = reverse("cancel-booking", kwargs={"pk": booking.pk})
        response = self.client.patch(url, {}, format="json")

        booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(booking.status, Booking.CANCELED)

    def test_booking_cannot_be_canceled_one_day_before_start(self):
        booking = self.create_booking(days_until_start=1)
        self.client.force_authenticate(user=self.tenant)

        url = reverse("cancel-booking", kwargs={"pk": booking.pk})
        response = self.client.patch(url, {}, format="json")

        booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(booking.status, Booking.PENDING)
        self.assertIn("error", response.data)

    def test_user_cannot_cancel_another_users_booking(self):
        booking = self.create_booking(days_until_start=10)
        self.client.force_authenticate(user=self.other_tenant)

        url = reverse("cancel-booking", kwargs={"pk": booking.pk})
        response = self.client.patch(url, {}, format="json")

        booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(booking.status, Booking.PENDING)

    def test_unauthenticated_user_cannot_cancel_booking(self):
        booking = self.create_booking(days_until_start=10)

        url = reverse("cancel-booking", kwargs={"pk": booking.pk})
        response = self.client.patch(url, {}, format="json")

        booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(booking.status, Booking.PENDING)

class OwnerBookingStatusTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="status_owner@example.com",
            password="TestPassword123!",
            username="status_owner",
            first_name="Status",
            last_name="Owner",
        )

        self.tenant = User.objects.create_user(
            email="status_tenant@example.com",
            password="TestPassword123!",
            username="status_tenant",
            first_name="Status",
            last_name="Tenant",
        )

        self.advertisement = Advertisement.objects.create(
            owner=self.owner,
            title="Owner Status Test Apartment",
            description="Apartment used for owner status tests",
            price_per_night="80.00",
            city="Huckelhoven",
            street="Teststrasse",
            house_number="30",
            rooms=3,
            properties="APARTMENT",
        )

        start_date = timezone.now().date() + timedelta(days=10)

        self.booking = Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=start_date,
            end_date=start_date + timedelta(days=2),
        )

        self.url = reverse(
            "owner-booking-status",
            kwargs={"pk": self.booking.pk},
        )

    def test_owner_can_confirm_pending_booking(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.url,
            {"status": Booking.CONFIRMED},
            format="json",
        )

        self.booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.booking.status, Booking.CONFIRMED)

    def test_owner_can_reject_pending_booking(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.url,
            {"status": Booking.CANCELED},
            format="json",
        )

        self.booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.booking.status, Booking.CANCELED)

    def test_owner_cannot_change_status_twice(self):
        self.booking.status = Booking.CONFIRMED
        self.booking.save()

        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.url,
            {"status": Booking.CANCELED},
            format="json",
        )

        self.booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking.status, Booking.CONFIRMED)
        self.assertIn("status", response.data)

    def test_tenant_cannot_use_owner_status_endpoint(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.patch(
            self.url,
            {"status": Booking.CONFIRMED},
            format="json",
        )

        self.booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.booking.status, Booking.PENDING)

    def test_invalid_status_is_rejected(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.url,
            {"status": Booking.COMPLETED},
            format="json",
        )

        self.booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.booking.status, Booking.PENDING)
        self.assertIn("status", response.data)

    def test_unauthenticated_user_cannot_change_status(self):
        response = self.client.patch(
            self.url,
            {"status": Booking.CONFIRMED},
            format="json",
        )

        self.booking.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.booking.status, Booking.PENDING)
class AvailableDatesTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="calendar_owner@example.com",
            password="TestPassword123!",
            username="calendar_owner",
            first_name="Calendar",
            last_name="Owner",
        )

        self.tenant = User.objects.create_user(
            email="calendar_tenant@example.com",
            password="TestPassword123!",
            username="calendar_tenant",
            first_name="Calendar",
            last_name="Tenant",
        )

        self.advertisement = Advertisement.objects.create(
            owner=self.owner,
            title="Calendar Test Apartment",
            description="Apartment used for available dates tests",
            price_per_night="90.00",
            city="Huckelhoven",
            street="Teststrasse",
            house_number="40",
            rooms=2,
            properties="APARTMENT",
        )

        self.start_date = timezone.now().date() + timedelta(days=10)
        self.end_date = self.start_date + timedelta(days=2)

    def test_pending_booking_blocks_occupied_dates(self):
        Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=self.start_date,
            end_date=self.end_date,
            status=Booking.PENDING,
        )

        available_dates = self.advertisement.get_available_dates()

        self.assertNotIn(self.start_date, available_dates)
        self.assertNotIn(
            self.start_date + timedelta(days=1),
            available_dates,
        )

    def test_checkout_date_is_available(self):
        Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=self.start_date,
            end_date=self.end_date,
            status=Booking.CONFIRMED,
        )

        available_dates = self.advertisement.get_available_dates()

        self.assertIn(self.end_date, available_dates)

    def test_canceled_booking_does_not_block_dates(self):
        Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=self.start_date,
            end_date=self.end_date,
            status=Booking.CANCELED,
        )

        available_dates = self.advertisement.get_available_dates()

        self.assertIn(self.start_date, available_dates)
        self.assertIn(
            self.start_date + timedelta(days=1),
            available_dates,
        )

    def test_available_dates_endpoint_returns_success(self):
        url = reverse(
            "available-dates",
            kwargs={"pk": self.advertisement.pk},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("available_dates", response.data)
        self.assertEqual(len(response.data["available_dates"]), 90)

class BookingListAndDetailTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="list_owner@example.com",
            password="TestPassword123!",
            username="list_owner",
            first_name="List",
            last_name="Owner",
        )

        self.other_owner = User.objects.create_user(
            email="other_owner@example.com",
            password="TestPassword123!",
            username="other_owner",
            first_name="Other",
            last_name="Owner",
        )

        self.tenant = User.objects.create_user(
            email="list_tenant@example.com",
            password="TestPassword123!",
            username="list_tenant",
            first_name="List",
            last_name="Tenant",
        )

        self.other_tenant = User.objects.create_user(
            email="second_tenant@example.com",
            password="TestPassword123!",
            username="second_tenant",
            first_name="Second",
            last_name="Tenant",
        )

        self.advertisement = Advertisement.objects.create(
            owner=self.owner,
            title="Owner Apartment",
            description="Apartment for booking list tests",
            price_per_night="70.00",
            city="Huckelhoven",
            street="Ownerstrasse",
            house_number="1",
            rooms=2,
            properties="APARTMENT",
        )

        self.other_advertisement = Advertisement.objects.create(
            owner=self.other_owner,
            title="Other Owner Apartment",
            description="Apartment belonging to another owner",
            price_per_night="90.00",
            city="Erkelenz",
            street="Otherstrasse",
            house_number="2",
            rooms=3,
            properties="APARTMENT",
        )

        start_date = timezone.now().date() + timedelta(days=10)

        self.pending_booking = Booking.objects.create(
            user=self.tenant,
            advertisement=self.advertisement,
            start_date=start_date,
            end_date=start_date + timedelta(days=2),
            status=Booking.PENDING,
        )

        self.confirmed_booking = Booking.objects.create(
            user=self.other_tenant,
            advertisement=self.advertisement,
            start_date=start_date + timedelta(days=3),
            end_date=start_date + timedelta(days=5),
            status=Booking.CONFIRMED,
        )

        self.other_booking = Booking.objects.create(
            user=self.tenant,
            advertisement=self.other_advertisement,
            start_date=start_date + timedelta(days=6),
            end_date=start_date + timedelta(days=8),
            status=Booking.PENDING,
        )

        self.user_list_url = reverse("user-bookings")
        self.owner_list_url = reverse("owner-bookings")

    def test_booking_lists_require_authentication(self):
        user_response = self.client.get(self.user_list_url)
        owner_response = self.client.get(self.owner_list_url)

        self.assertEqual(
            user_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            owner_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_tenant_sees_only_own_bookings(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        returned_ids = {
            item["id"] for item in response.data["results"]
        }

        self.assertEqual(
            returned_ids,
            {
                self.pending_booking.id,
                self.other_booking.id,
            },
        )

    def test_tenant_can_filter_bookings_by_status(self):
        self.client.force_authenticate(user=self.tenant)

        response = self.client.get(
            self.user_list_url,
            {"status": Booking.PENDING},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        for booking in response.data["results"]:
            self.assertEqual(booking["status"], Booking.PENDING)

    def test_owner_sees_only_bookings_for_own_advertisements(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.owner_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        returned_ids = {
            item["id"] for item in response.data["results"]
        }

        self.assertEqual(
            returned_ids,
            {
                self.pending_booking.id,
                self.confirmed_booking.id,
            },
        )
        self.assertNotIn(self.other_booking.id, returned_ids)

    def test_owner_can_filter_bookings_by_status(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(
            self.owner_list_url,
            {"status": Booking.CONFIRMED},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["id"],
            self.confirmed_booking.id,
        )

    def test_tenant_can_view_own_booking_detail(self):
        self.client.force_authenticate(user=self.tenant)

        url = reverse(
            "booking-detail",
            kwargs={"pk": self.pending_booking.pk},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["status"],
            Booking.PENDING,
        )

    def test_tenant_cannot_view_another_users_booking(self):
        self.client.force_authenticate(user=self.tenant)

        url = reverse(
            "booking-detail",
            kwargs={"pk": self.confirmed_booking.pk},
        )
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_booking_detail_does_not_allow_patch(self):
        self.client.force_authenticate(user=self.tenant)

        url = reverse(
            "booking-detail",
            kwargs={"pk": self.pending_booking.pk},
        )
        response = self.client.patch(
            url,
            {"status": Booking.CONFIRMED},
            format="json",
        )

        self.pending_booking.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
        self.assertEqual(
            self.pending_booking.status,
            Booking.PENDING,
        )
