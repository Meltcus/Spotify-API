# Import necessary modules
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Load environment variables from .env file
load_dotenv()

# Get client ID and client secret from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Main function
def main():
    # Get user input for artist name
    artist_name = input("Enter an Artist: ")

    # Get token for accessing Spotify API
    token = get_token()

    # Search for artist by name
    result = search_for_artist(token, artist_name)

    # If artist not found, print message and exit
    if result is None:
        return

    # Get artist ID from search result
    artist_id = result["id"]

    # Get top songs by artist
    songs = get_songs_by_artist(token, artist_id)

    # Print top songs
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

# Function to get token for accessing Spotify API
def get_token():
    # Encode client ID and client secret for authentication
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Spotify API endpoint for token
    url = "https://accounts.spotify.com/api/token"

    # Headers for token request
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Data for token request
    data = {"grant_type": "client_credentials"}

    # Send token request and get response
    result = post(url, headers=headers, data=data)

    # Parse response JSON and get access token
    json_results = json.loads(result.content)
    token = json_results["access_token"]
    return token

# Function to get authorization header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# Function to search for artist by name
def search_for_artist(token, artist_name):
    # Spotify API endpoint for artist search
    url = "https://api.spotify.com/v1/search"

    # Headers for search request
    headers = get_auth_header(token)

    # Query parameters for search request
    query = f"?q={artist_name}&type=artist&limit=1"

    # Construct full query URL
    query_url = url + query

    # Send search request and get response
    result = get(query_url, headers=headers)

    # Parse response JSON and get artist information
    json_result = json.loads(result.content)["artists"]["items"]

    # If no artist found, print message and return None
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    # Return first artist found
    return json_result[0]

# Function to get top songs by artist
def get_songs_by_artist(token, artist_id):
    # Spotify API endpoint for artist's top tracks
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"

    # Headers for top tracks request
    headers = get_auth_header(token)

    # Send top tracks request and get response
    result = get(url, headers=headers)

    # Parse response JSON and get top tracks
    json_result = json.loads(result.content)["tracks"]

    # Return top tracks
    return json_result

# Call main function to start the program
main()
