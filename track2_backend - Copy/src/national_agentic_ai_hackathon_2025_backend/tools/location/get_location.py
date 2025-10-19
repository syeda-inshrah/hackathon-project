from national_agentic_ai_hackathon_2025_backend.config import Config
from agents import function_tool, RunContextWrapper
import requests

@function_tool
def get_location_info(
    wrapper: RunContextWrapper,
    lat: float,
    lng: float,
):
    """
    Extract location information (city, country, etc.) from latitude and longitude coordinates.
    
    Args:
        lat (float): Latitude coordinate
        lng (float): Longitude coordinate
    
    Returns:
        dict: Location information including city, country, and other details
    """
    url = (
        f"https://maps.googleapis.com/maps/api/geocode/json?"
        f"latlng={lat},{lng}&key={Config.get('GOOGLE_API_KEY')}"
    )
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] != "OK" or not data["results"]:
        return {"error": "Location not found", "status": data["status"]}
    
    result = data["results"][0]
    address_components = result["address_components"]
    
    location_info = {
        "formatted_address": result["formatted_address"],
        "place_id": result["place_id"],
        "geometry": {
            "lat": result["geometry"]["location"]["lat"],
            "lng": result["geometry"]["location"]["lng"]
        }
    }
    
    # Extract specific components
    for component in address_components:
        types = component["types"]
        if "locality" in types:
            location_info["city"] = component["long_name"]
        elif "administrative_area_level_1" in types:
            location_info["state_province"] = component["long_name"]
        elif "country" in types:
            location_info["country"] = component["long_name"]
            location_info["country_code"] = component["short_name"]
        elif "postal_code" in types:
            location_info["postal_code"] = component["long_name"]
        elif "route" in types:
            location_info["street"] = component["long_name"]
        elif "street_number" in types:
            location_info["street_number"] = component["long_name"]
    
    return location_info
