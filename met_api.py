import requests, random

BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

def get_random_artwork(): 

    # Get all object IDs
    response = requests.get(f"{BASE_URL}/objects")
    data = response.json()
    object_ids = data['objectIDs']

    # Pick a random object ID
    random_id = random.choice(object_ids)

    # Get details about the selected artwork
    art_response = requests.get(f"{BASE_URL}/objects/{random_id}")
    art_data = art_response.json()

    # Return important info
    return {
        "title": art_data.get("title"),
        "artist": art_data.get("artistDisplayName"),
        "date": art_data.get("objectDate"),
        "image": art_data.get("primaryImageSmall"),
        "url": art_data.get("objectURL"),
    }
