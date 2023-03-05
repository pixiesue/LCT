# Let's start by importing some modules
import requests  # We use this to send HTTP requests
import time  # We use this to track how long our program takes to run
import os  # We use this to check if a file already exists
import pandas as pd  # We use this to create and manipulate data in a table format

import time  # This is the second time we're importing the time module... why? Because we can!

# This function retrieves the games from the API
def retrieve_games(num_games, offset):
    # Set up the API endpoint URL
    endpoint_url = "https://api.mobygames.com/v1/games"

    # Retrieve the games
    games = []
    platforms = set()
    request_count = 0
    start_time = time.time()  # Let's start timing how long this takes
    while len(games) < num_games:
        remaining_games = num_games - len(games)
        limit = min(remaining_games, 100)
        params = {"api_key": "moby_wxjYo7yYkVFG3ADJwiaQnY1aJfm", "format": "normal", "limit": limit, "offset": offset}
        response = requests.get(endpoint_url, params=params)
        request_count += 1
        if response.status_code != 200:
            print(f"Error retrieving data (status code {response.status_code})")
            break
        data = response.json()
        for game in data["games"]:
            platforms.update(platform["platform_name"] for platform in game.get("platforms", []))
            games.append({
                "ID": game.get("game_id", "-"),
                "Title": game.get("title", "-"),
                "Release Dates": game.get("platforms", [{"first_release_date": "-"}])[0]["first_release_date"],
                "Genre": ", ".join(genre["genre_name"] for genre in game.get("genres", [])),
                "Platforms": ", ".join(platform["platform_name"] for platform in game.get("platforms", [])),
                "Moby URL": game.get("moby_url", "-")
            })
        offset += limit
        if len(data["games"]) < limit:
            break

    elapsed_time = time.time() - start_time  # We're done timing!
    request_rate = request_count / elapsed_time
    print(f"Retrieved {len(games)} games from {len(platforms)} platforms in {elapsed_time:.2f} seconds.")
    print(f"Made {request_count} requests at a rate of {request_rate:.2f} requests per second.")

    return games, platforms


def output_statistics(games, platforms):
    print(f"Retrieved {len(games)} games from {len(platforms)} platforms.")

    # Release date and titles of first and last games
    if len(games) > 0:
        first_game = games[0]
        last_game = games[-1]
        first_release_date = pd.to_datetime(first_game['Release Dates'], errors='coerce').date()
        last_release_date = pd.to_datetime(last_game['Release Dates'], errors='coerce').date()
        print(f"\nRelease date and titles of first and last games:")
        print(f"First game: ID={first_game['ID']}, Title={first_game['Title']}, Release Date={first_release_date}")
        print(f"Last game: ID={last_game['ID']}, Title={last_game['Title']}, Release Date={last_release_date}")

        # Number of games per platform
        num_games_per_platform = {}
        for game in games:
            for platform in game['Platforms'].split(', '):
                num_games_per_platform[platform] = num_games_per_platform.get(platform, 0) + 1
        print("\nNumber of games per platform (sorted by number of games):")
        for platform, num_games in sorted(num_games_per_platform.items(), key=lambda x: x[1], reverse=True):
            print(f"{platform}: {num_games}")

        # Most common genres
        all_genres = [genre for game in games for genre in game['Genre'].split(', ')]
        genre_counts = {genre: all_genres.count(genre) for genre in set(all_genres)}
        most_common_genres = sorted(genre_counts, key=genre_counts.get, reverse=True)[:5]
        print("\nMost common genres:")
        for genre in most_common_genres:
            print(f"{genre}: {genre_counts[genre]}")

        # Range of release dates
        release_dates = [game['Release Dates'] for game in games if game['Release Dates'] != "-"]
        earliest_release_date = min(release_dates) if release_dates else "-"
        latest_release_date = max(release_dates) if release_dates else "-"
        print(f"\nRange of release dates: {earliest_release_date} - {latest_release_date}")

        # Average number of platforms per game
        avg_num_platforms = sum(len(game['Platforms'].split(', ')) for game in games) / len(games)
        print(f"\nAverage number of platforms per game: {avg_num_platforms:.2f}")


def save_to_excel(games):
    # Check if the file already exists
    filename = f"mobygames_{games[0]['ID']}_{games[-1]['ID']}.xlsx"
    if os.path.isfile(filename):
        overwrite = input(
            f"The file '{filename}' already exists. Do you want to overwrite it (o), increment the filename (i), or enter a new filename (n)? ")
        if overwrite.lower() == 'i':
            i = 1
            while True:
                new_filename = f"mobygames_{games[0]['ID']}_{games[-1]['ID']}_{i}.xlsx"
                if not os.path.isfile(new_filename):
                    filename = new_filename
                    break
                i += 1
        elif overwrite.lower() == 'n':
            new_filename = input("Enter a new filename: ")
            filename = f"{new_filename}.xlsx"

    # Convert the games list to a pandas DataFrame and output to an Excel file
    games_df = pd.DataFrame(games)
    games_df.to_excel(filename, index=False)
    print(f"Data saved to '{filename}'")



def main():
    # Prompt the user to enter the number of games to retrieve
    num_games_input = input("Enter the number of games to retrieve (max 100000): ")
    if num_games_input:
        num_games = min(int(num_games_input), 100000)
    else:
        num_games = 100

    # Prompt the user to enter an offset value
    offset_input = input("Enter the offset value (default is 0): ")
    if offset_input:
        offset = int(offset_input)
    else:
        offset = 0



    # Retrieve the games and platforms
    games, platforms = retrieve_games(num_games, offset)

    # Output the statistics and save to Excel
    output_statistics(games, platforms)
    save_to_excel(games)


if __name__ == "__main__":
    main()
