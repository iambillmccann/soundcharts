import requests

def get_top_artists(api_key, url):
    headers = {
        "x-app-id": "soundcharts",
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def main():
    api_key = "soundcharts"
    url = "https://sandbox.api.soundcharts.com/api/v2/top-artist/spotify/monthly_listeners?sortBy=total&period=week&minValue=0"

    artists_data = get_top_artists(api_key, url)

    if artists_data is not None:
        print("List of Top Artists on SoundCharts:")
        for item in artists_data['items']:
            print(f"{item['artist']['name']} (Monthly Listeners: {item['total']})")

if __name__ == "__main__":
    main()
