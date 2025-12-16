import requests
from src.config import NEWSDATA_API_KEY

class ApiClient:
    def get_country_details(self, country_name):
        """Fetches capital, currency, and language from REST Countries."""
        url = f"https://restcountries.com/v3.1/name/{country_name}?fullText=true"
        response = requests.get(url)
        
        if response.status_code != 200:
            return None

        data = response.json()[0]
        
        # Extracting specific data
        currency_code = list(data.get("currencies", {}).keys())[0]
        language_key = list(data.get("languages", {}).keys())[0]
        
        return {
            "name": data.get("name", {}).get("common"),
            "capital": data.get("capital", ["N/A"])[0],
            "currency": f"{currency_code} ({data['currencies'][currency_code]['name']})",
            "language": data["languages"][language_key],
            "cca2": data.get("cca2")
        }

    def get_news(self, country_code, topic, language):
        """Fetches news from Newsdata.io."""
        base_url = "https://newsdata.io/api/1/latest"
        params = {
            "apikey": NEWSDATA_API_KEY,
            "category": topic,
            "country": country_code,
            "language": language
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            return []

        data = response.json()
        return data.get("results", [])[:5] # Return max 5 results