import requests
import time
import utilities
import os

ARTIST_FILE = "artists.csv"
CHECKPOINT_FILE = "checkpoint.txt"
CALL_LIMIT = 10
DOMAIN = " https://customer.api.soundcharts.com"

def get_top_artists(url):
    headers = {
        "x-app-id": os.environ.get('X_APP_ID'),
        "x-api-key": os.environ.get('X_API_KEY'),
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def main():
    file_disposition = "w" # The first time we write to the file, we want to overwrite it
    url = DOMAIN + "/api/v2/top-artist/spotify/monthly_listeners?sortBy=total&period=week&minValue=0"

    for count in range(0, CALL_LIMIT):
    
        artists_data = get_top_artists(url)
        if artists_data is None: break

        artists = list(map(lambda x: [x['artist']['uuid'], x['artist']['slug'], x['artist']['name']], artists_data['items']))
        utilities.save_data(artists, ARTIST_FILE, file_disposition)

        if artists_data['page']['next'] is None: break
        url = DOMAIN + artists_data['page']['next']
        utilities.take_checkpoint(url, CHECKPOINT_FILE, file_disposition)
        file_disposition = "a" # After the first time, we want to append to the file

if __name__ == "__main__":

    start_time = time.time()
    main()
    stop_time = time.time()
    total_time = stop_time - start_time

    print('\n-----------------------------------------------------------------------')
    print('Execution time was ' + utilities.format_milliseconds(total_time))
    print('-----------------------------------------------------------------------')
    print()
