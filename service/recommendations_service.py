"""Main application: launching different recommendation services."""
import requests
from fastapi import FastAPI

headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
recommendations_url = "http://127.0.0.1:8001"
events_url = "http://127.0.0.1:8002"
features_url = "http://127.0.0.1:8003"

# Creating an app
app = FastAPI(title="recommendations_main")

def dedup_ids(ids):
    """Removes duplicates from a list."""
    seen = set()
    ids = [id for id in ids if not (id in seen or seen.add(id))]

    return ids

@app.post("/recommendations_offline")
async def recommendations_offline(user_id: int, k: int = 5):
    """Displays k offline recommendations."""
    params = {"user_id": user_id, "k": k}
    response = requests.post(
        recommendations_url + "/get_recs", params=params, headers=headers
        )
    response = response.json()

    return {"recs": response}

@app.post("/recommendations_online")
async def recommendations_online(user_id: int, k: int = 5, num_events: int = 3):
    """Displays k online recommendations based on last online events."""
    # Retrieving the online history for a user
    params = {"user_id": user_id, "k": num_events}
    response = requests.post(events_url + "/get", params=params, headers=headers)
    events = response.json()
    events = events["events"]

    # Getting online recommendations for each event (track)
    tracks = []
    scores = []
    for track_id in events:
        params = {"track_id": track_id, "k": k}
        response = requests.post(
            features_url + "/similar_tracks", headers=headers, params=params
        )
        response = response.json()
        tracks += response["track_id_2"]
        scores += response["score"]
    combined = list(zip(tracks, scores))
    combined = sorted(combined, key=lambda x: x[1], reverse=True)
    combined = [track for track, _ in combined]

    # Removing duplicates from recommendations
    combined = dedup_ids(combined)

    return {"recs": combined[:k]}

@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 50):
    """Computes recommendations based on online/offline history."""
    # Computing both types of recommendations
    result_online = await recommendations_online(user_id=user_id, k=k)
    result_offline = await recommendations_offline(user_id=user_id, k=k)
    # Stopping if there is no online history
    if result_online["recs"] == []:
        return {"recs": result_offline["recs"]}
    
    # Blending online and offline recommendations (if online history present)
    recs_online = result_online["recs"]
    recs_offline = result_offline["recs"]

    recs_blended = []
    min_length = min(len(recs_offline), len(recs_online))
    for i in range(min_length):
        recs_blended.append(recs_online[i])
        recs_blended.append(recs_offline[i])

    # Removing duplicates
    recs_blended = dedup_ids(recs_blended)

    return {"recs": recs_blended[:k]}
