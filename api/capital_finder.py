from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

REST_COUNTRIES_API = "https://restcountries.com/v3.1/name"

def get_country_info(name):
    response = requests.get(f"{REST_COUNTRIES_API}/{name}")
    if response.status_code == 200:
        country_data = response.json()[0]
        return country_data
    else:
        return None

class CapitalFinderHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_components = parse.urlsplit(self.path)
        query_string_list = parse.parse_qsl(url_components.query)
        query_params = dict(query_string_list)

        if "country" in query_params:
            country_name = query_params["country"].capitalize()
            country_info = get_country_info(country_name)

            if country_info:
                country_capital = country_info.get("capital", ["N/A"])[0]
                message = f"The capital of {country_name} is {country_capital}."
            else:
                message = f"Country not found for {country_name}."

        elif "capital" in query_params:
            capital_name = query_params["capital"].capitalize()
            country_info = next((info for info in get_country_info("") if capital_name in info.get("capital", [""]).lower()), None)

            if country_info:
                country_name = country_info.get("name", {}).get("common", "N/A")
                message = f"{capital_name} is the capital of {country_name}."
            else:
                message = f"Capital not found for {capital_name}."

        else:
            message = "Bad Request: Please provide a country or capital parameter."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))