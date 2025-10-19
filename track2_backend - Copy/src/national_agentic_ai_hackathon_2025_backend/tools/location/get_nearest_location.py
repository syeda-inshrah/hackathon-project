from national_agentic_ai_hackathon_2025_backend.config import Config
from national_agentic_ai_hackathon_2025_backend.context.coordinates import Coordinates
from agents import function_tool, RunContextWrapper
from typing import List
import requests

@function_tool
def get_nearest_place(
    wrapper: RunContextWrapper[Coordinates],
    destinations: List[str],
):
    """
    Find the nearest destination from a given origin using the Google Maps Distance Matrix API.

    This tool takes an origin location (latitude,longitude as a string) and a set of predefined
    destination coordinates, and returns the destination that is closest to the origin by driving distance.
    The response includes the nearest destination's address, distance, and duration, as well as the full API results.

    Args:
        origin (str): The origin location as a "lat,lng" string.

    Returns:
        dict: A dictionary containing the nearest place information and all API results.
    """
    origin = f"{wrapper.context.latitude}, {wrapper.context.longitude}"
 
    dest_str = "|".join(destinations)

    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json?"
        f"origins={origin}&destinations={dest_str}&mode=driving&key={Config.get('GOOGLE_API_KEY')}"
    )

    response = requests.get(url)
    data = response.json()

    # Extract nearest location
    elements = data["rows"][0]["elements"]
    min_index = min(range(len(elements)), key=lambda i: elements[i]["distance"]["value"])

    nearest = {
        "destination": data["destination_addresses"][min_index],
        "distance_text": elements[min_index]["distance"]["text"],
        "distance_value_m": elements[min_index]["distance"]["value"],
        "duration_text": elements[min_index]["duration"]["text"],
        "duration_value_s": elements[min_index]["duration"]["value"],
    }
    print({"nearest_place": nearest})
    return {"nearest_place": nearest, "all_results": data}