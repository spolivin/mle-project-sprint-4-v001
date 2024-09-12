"""Tests the recommendations service."""
import unittest

import requests

from service.constants import (
    BASE_URL,
    MAIN_APP_PORT,
    EVENTS_SERVICE_PORT,
)

# Request components
headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
main_app_url = BASE_URL + ":" + str(MAIN_APP_PORT)
events_url = BASE_URL + ":" + str(EVENTS_SERVICE_PORT)


def send_test_request(params, url, endpoint, headers=headers):
    """Sends a test request to a url/endpoint."""
    resp = requests.post(url + endpoint, headers=headers, params=params)
    if resp.status_code == 200:
        recs = resp.json()
    else:
        recs = []
        print(f"status code: {resp.status_code}")
    
    return recs

class TestRecommendationsService(unittest.TestCase):
    """Class for testing a recommendation service."""

    def test_connection(self):
        """Tests connection to all services comprising the application."""
        response = requests.get(main_app_url + "/healthy")
        response = response.json()
        response = response["status"]
        
        self.assertEqual(response, "healthy")

    def test_default_users(self, user_id_1: int = 5, user_id_2: int = 1):
        """Tests recs for users without personal recs / online history."""
        # Getting recommendations for user_id=5
        params_user_5 = {"user_id": user_id_1}
        response_user_5 = send_test_request(
            params=params_user_5, url=main_app_url, endpoint="/recommendations",
        )
        # Getting recommendations for user_id=1
        params_user_1 = {"user_id": user_id_2}
        response_user_1 = send_test_request(
            params=params_user_1, url=main_app_url, endpoint="/recommendations",
        )

        self.assertEqual(response_user_5["recs"], response_user_1["recs"])

    def test_no_empty_recs_1(self, user_id: int = 28073):
        """Tests the non-emptiness of recommendations (user with personal recs)."""
        params = {"user_id": user_id}
        response = send_test_request(
            params=params, url=main_app_url, endpoint="/recommendations",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])

    def test_no_empty_recs_2(self, user_id: int = 1):
        """Tests the non-emptiness of recommendations (user without personal recs)."""
        params = {"user_id": user_id}
        response = send_test_request(
            params=params, url=main_app_url, endpoint="/recommendations",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])

    def test_online_history(
            self, 
            user_id: int = 54633, 
            events: list = [3911, 1168, 109123, 8449],
        ):
        """Tests if the online history is added upon request."""
        for track_id in events:
            response = requests.post(
                events_url + "/put", 
                params={"user_id": user_id, "track_id": track_id}
            )
        online_history = send_test_request(
            params={"user_id": user_id, "k": 100},
            url=events_url,
            endpoint="/get",
        )

        self.assertIsInstance(online_history["events"], list)
        self.assertNotEqual(online_history["events"], [])

    def test_online_recommendations(self, user_id: int = 54633):
        """Tests if user with online history gets non-empty recommendations."""
        params = {"user_id": user_id}
        response = send_test_request(
            params=params, url=main_app_url, endpoint="/recommendations_online",
        )

        self.assertIsInstance(response["recs"], list)
        self.assertNotEqual(response["recs"], [])

    def test_service_stats(self):
        """Tests if service statistics are changing after requests."""
        # Requesting stats
        response = requests.get(main_app_url + "/stats")
        response = response.json()
        # Separating stats
        response_default_stats = response["request_default_count"]
        response_personal_stats = response["request_personal_count"]
        
        self.assertGreater(response_default_stats, 0)
        self.assertGreater(response_personal_stats, 0)

if __name__ == "__main__":
    unittest.main()
