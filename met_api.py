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

# def search_artwork_title(query):
#     response = requests.get(f"{BASE_URL}/search", params={"title": query})
#     data = response.json()
    
#     if not data["objectIDs"]:
#         return None
    
#     random_art_id = random.choice(data["objectIDs"])
#     art_data = requests.get(f"{BASE_URL}/objects/{random_art_id}").json()
    
#     return {
#         "title": art_data["title"],
#         "artist": art_data.get("artistDisplayName", "Unknown"),
#         "date": art_data.get("objectDate", "Unknown"),
#         "image": art_data.get("primaryImage", None),
#         "url": art_data["objectURL"]
#     }

def get_artworks_by_department(department_id: int):
    response = requests.get(f"{BASE_URL}/objects", params={"departmentIds": department_id}) # FIX THIS!!!
    data = response.json()
    
    # if there are no objects with the department above, return None
    if not data["objectIDs"]:
        return None
    
    random_art_id = random.choice(data["objectIDs"])
    art_data = requests.get(f"{BASE_URL}/objects/{random_art_id}").json()
    
    return {
        "title": art_data["title"],
        "artist": art_data.get("artistDisplayName", "Unknown"),
        "date": art_data.get("objectDate", "Unknown"),
        "image": art_data.get("primaryImage", None),
        "url": art_data["objectURL"]
    }

def get_departments(): 
    response = requests.get(f"{BASE_URL}/departments")
    data = response.json()

    # List of Dictionaries that each have an departmentId and a displayName
    departments_data = data["departments"]
    return departments_data