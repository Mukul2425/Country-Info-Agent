import requests


BASE_URL = "https://restcountries.com/v3.1/name"


def get_country_data(country: str) -> dict | None:
    """
    Fetch country information from REST Countries API.
    Returns the first match or None if not found.
    """

    try:
        response = requests.get(f"{BASE_URL}/{country}", timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        return data[0]

    except requests.RequestException:
        return None
    
