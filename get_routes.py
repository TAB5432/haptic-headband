import requests
import math

API_KEY = "XXX"

START_POINT = [-0.1278, 51.5074]  # [Lng, Lat] Trafalgar Square
END_POINT = [-0.1416, 51.5010]    # [Lng, Lat] Buckingham Palace

def fetch_walking_waypoints(start, end, api_key):
    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
    
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    
    body = {
        "coordinates": [start, end],
        "options": {
            "avoid_features": ["steps"]
        }
    }

    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return []

    data = response.json()
    
    feature = data["features"][0]
    coordinates = feature["geometry"]["coordinates"]
    steps = feature["properties"]["segments"][0]["steps"]
    
    waypoints = []
    for idx, step in enumerate(steps, start=1):
        start_idx = step["way_points"][0]
        lng, lat = coordinates[start_idx]

        waypoints.append({
            "id": idx,
            "lat": lat,
            "lng": lng,
            "instruction": step["instruction"],
            "distance_m": step["distance"]
        })
        
    return waypoints

route = fetch_walking_waypoints(START_POINT, END_POINT, API_KEY)


for i in range(len(route)-1):
    pt = route[i]
    pt2 = route[i+1]

    delta_lat = pt2["lat"] - pt["lat"]
    delta_lng = pt2["lng"] - pt["lng"]

    delta_lat = math.radians(delta_lat)
    delta_lng = math.radians(delta_lng)

    lat = math.radians(pt["lat"])
    lng = math.radians(pt["lng"])
    lat2 = math.radians(pt2["lat"])
    lng2 = math.radians(pt2["lng"])

    theta = math.atan2(math.sin(delta_lng) * math.cos(lat2), math.cos(lat) * math.sin(lat2) - math.sin(lat) * math.cos(lat2) * math.cos(delta_lng))

    theta = math.degrees(theta)
    theta = theta % 360

        
    print(f"Waypoint {pt["id"]}: [{pt["lat"]}, {pt["lng"]}] - ({pt["distance_m"]}m)")
    print(f"    Bearing: {theta}")