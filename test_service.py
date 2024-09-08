import json
import logging

import requests

# Creating a custom logger with logging to a file
logger = logging.getLogger("test_service_log")
logging.basicConfig(filename="test_service.log", level=logging.INFO)

# Request components
headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
main_app_url = "http://127.0.0.1:8000"
events_url = "http://127.0.0.1:8002"

def send_test_request(params, url, endpoint, headers=headers):
    """Sends a test request to a url/endpoint."""
    resp = requests.post(url + endpoint, headers=headers, params=params)
    if resp.status_code == 200:
        recs = resp.json()
    else:
        recs = []
        print(f"status code: {resp.status_code}")
    
    return recs


if __name__ == "__main__":
    # User without personal recommendations and no online history
    params = {"user_id": 5, "k": 5}
    recs = send_test_request(params=params, url=main_app_url, endpoint="/recommendations")
    logger.info(f"No personal/no online - {params} => {recs}")

    # Testing for another user without personal recommendations/online history
    params = {"user_id": 1, "k": 5}
    recs = send_test_request(params=params, url=main_app_url, endpoint="/recommendations")
    logger.info(f"No personal/no online - {params} => {recs}")

    # User with personal history and no online history
    params = {"user_id": 28073, "k": 5}
    recs = send_test_request(params=params, url=main_app_url, endpoint="/recommendations")
    logger.info(f"Personal/no online{params} => {recs}")

    # User with personal history and online history
    # Adding events to the online history
    user_id = 54633
    track_ids = [3911, 1168, 109123, 8449]
    for track_id in track_ids:
        response = requests.post(
            events_url + "/put", 
            params={"user_id": user_id, "track_id": track_id}
        )
    # Checking if the events have been added
    inspect = send_test_request(
        params={"user_id": user_id, "k": 100},
        url=events_url,
        endpoint="/get",
    )
    logger.info(inspect)

    # Checking offline recommendations
    params = {"user_id": user_id, "k": 5}
    recs = send_test_request(params=params, url=main_app_url, endpoint="/recommendations_offline")
    logger.info(f"Offline - {params} => {recs}")

    # Checking online recommendations
    recs = send_test_request(params=params, url=main_app_url, endpoint="/recommendations_online")
    logger.info(f"Online - {params} => {recs}")

    # Checking blended recommendations
    recs = send_test_request(params=params, url=main_app_url, endpoint="/recommendations")
    logger.info(f"Blended - {params} => {recs}")

    # Saving blended recommendations
    with open("recs_blended.json", "w") as file:
        json.dump(recs, file)
