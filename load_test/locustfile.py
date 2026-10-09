import csv
import os
import threading
from itertools import count
from pathlib import Path

from locust import HttpUser, constant, task
from locust.exception import StopUser

# Replace these with your real booking endpoint and request fields.
BOOKING_ENDPOINT = "/api/v1/book-seats"

EVENT_ID = "a5436a99-83e8-43b5-ab78-e983d2b19d5c"
SEAT_ID_LIST = ["ee9f14b9-3811-434f-97da-0765b48490bf"]

USERS_FILE = Path(__file__).with_name("locust_users.csv")

with USERS_FILE.open(newline="", encoding="utf-8") as file:
    TEST_USERS = list(csv.DictReader(file))

if not TEST_USERS:
    raise RuntimeError("locust_users.csv contains no test users")

# This credential allocator is intended for a single Locust process.
_user_index = count()
_user_lock = threading.Lock()


def get_test_user():
    with _user_lock:
        index = next(_user_index)

    if index >= len(TEST_USERS):
        raise RuntimeError(
            "Not enough test accounts for the requested Locust users"
        )

    return TEST_USERS[index]


class SeatBookingUser(HttpUser):
    # Start booking attempts as soon as each user is ready.
    wait_time = constant(0)

    def on_start(self):
        credentials = get_test_user()

        # Assumes the login endpoint accepts OAuth2 form data.
        # If your endpoint accepts JSON, change data= to json=.
        response = self.client.post(
            "/api/v1/login",
            data={
                "username": credentials["email"],
                "password": credentials["password"],
            },
            name="POST /api/v1/login",
        )

        if response.status_code != 200:
            print(f"Login failed: HTTP {response.status_code}")
            raise StopUser()

        try:
            token = response.json()["access_token"]
        except (ValueError, KeyError):
            print("Login response did not contain access_token")
            raise StopUser()

        self.headers = {
            "Authorization": f"Bearer {token}"
        }

    @task
    def book_same_seat(self):
        # Each simulated user makes exactly one booking attempt.
        with self.client.post(
            BOOKING_ENDPOINT,
            headers=self.headers,
            json={
                "event_id": EVENT_ID,
                "id_list": SEAT_ID_LIST,
            },
            name="POST /booking (same seat)",
            catch_response=True,
        ) as response:

            if response.status_code in (200, 201):
                response.success()

            elif response.status_code == 409:
                # Expected result: another user got the seat first.
                response.success()

            else:
                response.failure(
                    f"Unexpected booking response: "
                    f"HTTP {response.status_code}"
                )

        # Do not let this user retry and distort the experiment.
        self.stop(True)
