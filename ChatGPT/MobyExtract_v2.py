import requests
import time
from tabulate import tabulate

# Set up the API endpoint URL
endpoint_url = "https://api.mobygames.com/v1/games"

# Prompt the user to enter the limit parameter
limit = input("Enter the maximum number of games to return (default 100, max 100000): ")

# Calculate the number of requests needed based on the limit
num_requests = (int(limit) + 99) // 100

# Send the API requests and retrieve the responses
games_list = []
for i in range(num_requests):
    # Set the offset parameter for the current request
    offset = i * 100

    # Set the parameters for the current request
    params = {
        "api_key": "moby_wxjYo7yYkVFG3ADJwiaQnY1aJfm",
        "format": "normal",
        "limit": 100,
        "offset": offset
    }

    # Send the API request and retrieve the response
    response = requests.get(endpoint_url, params=params)
    data = response.json()

    # Extract the game information and add it to the games_list
    for game in data["games"]:
        platform_list = []
        for platform in game.get("platforms", []):
            platform_info = f"{platform.get('platform_name')} ({platform.get('first_release_date', '-')})"
            platform_list.append(platform_info)

        genre_list = []
        for genre in game.get("genres", []):
            genre_name = genre.get("genre_name", "-")
            genre_list.append(genre_name)

        game_info = [
            game.get("game_id", "-"),
            game.get("title", "-"),
            ", ".join(platform_list),
            ", ".join(genre_list),
            game.get("moby_url", "-")
        ]
        games_list.append(game_info)

    # Wait for 5 seconds before making the next request
    time.sleep(5)

# Output the games in a table format
headers = ["ID", "Title", "Platforms", "Genre", "Moby URL"]
print(tabulate(games_list, headers=headers))
