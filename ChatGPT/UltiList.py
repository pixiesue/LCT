import requests
from tabulate import tabulate

# Set up the API endpoint URL
endpoint_url = "https://api.mobygames.com/v1/games"

# Prompt the user to enter the limit and offset parameters
limit = input("Enter the maximum number of games to return (default 100, max 100): ")
offset = input("Enter the offset from which to begin returning games (default 0): ")
params = {
    "api_key": "moby_wxjYo7yYkVFG3ADJwiaQnY1aJfm",
    "format": "normal",
    "limit": limit or 100,
    "offset": offset or 0
}

# Send the API request and retrieve the response
response = requests.get(endpoint_url, params=params)
data = response.json()

# Extract the game information and put it into a list of lists
games_list = []
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

# Output the games in a table format
headers = ["Game ID", "Title", "Platforms", "Genre", "Moby URL"]
print(tabulate(games_list, headers=headers))
