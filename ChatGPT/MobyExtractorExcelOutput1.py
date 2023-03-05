import requests
import time
import pandas as pd

# Set up the API endpoint URL
endpoint_url = "https://api.mobygames.com/v1/games"

# Prompt the user to enter the number of games to retrieve
num_games = input("Enter the number of games to retrieve (max 300000): ")
if not num_games:
    num_games = 100  # Default to retrieving 100 games if no input is provided
else:
    num_games = min(int(num_games), 300000)  # Limit the number of games to 300000

# Send the API requests and retrieve the response
params = {
    "api_key": "moby_wxjYo7yYkVFG3ADJwiaQnY1aJfm",
    "format": "normal",
    "limit": 100,  # We will retrieve games in batches of 100
    "offset": 0
}

# Keep track of the platforms and number of games retrieved
platforms = set()  # We will use a set to keep track of unique platforms
games_list = []
num_games_retrieved = 0
num_requests = 0

# Loop until we have retrieved the desired number of games or there are no more games left to retrieve
while num_games_retrieved < num_games:

    # Send the API request and retrieve the response
    response = requests.get(endpoint_url, params=params)
    num_requests += 1  # Increment the number of API requests made
    if response.status_code != 200:
        print(f"Error retrieving data (status code {response.status_code})")
        break

    # Extract the game information from the response
    data = response.json()
    for game in data["games"]:
        platform_list = []
        for platform in game.get("platforms", []):
            # Build a string with the platform name and first release date
            platform_info = f"{platform.get('platform_name')} ({platform.get('first_release_date', '-')})"
            platform_list.append(platform_info)
            platforms.add(platform.get('platform_name'))  # Add the platform name to the set of platforms

        genre_list = []
        for genre in game.get("genres", []):
            genre_name = genre.get("genre_name", "-")
            genre_list.append(genre_name)

        game_info = {
            "ID": game.get("game_id", "-"),
            "Title": game.get("title", "-"),
            "Platforms": ", ".join(platform_list),
            "Genre": ", ".join(genre_list),
            "Moby URL": game.get("moby_url", "-")
        }
        games_list.append(game_info)

    num_games_retrieved += len(data["games"])
    print(f"Retrieved {num_games_retrieved} games out of {num_games}...")

    # Check if we have retrieved all the games
    if len(data["games"]) < 100:
        break

    # Sleep for 10 seconds between requests
    time.sleep(10)

    # Increment the offset for the next request
    params["offset"] += 100

# Output the statistics
print(f"\nRetrieved {num_games_retrieved} games from {len(platforms)} platforms in {num_requests} API requests.")

# Convert the games list to a pandas DataFrame and output to an Excel file
games_df = pd.DataFrame(games_list)
games_df.to_excel("mobygames_full.xlsx", index=False)

print("Data saved to 'mobygames_full.xlsx'")
