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

def display_country_info(country_info):
    def do_GET(self):
        url_components = parse.urlsplit(self.path)
        query_string_list = parse.parse_qsl(url_components.query)
        query_params = dict(query_string_list)

        if "country" in query_params:
            country_name = query_params["country"].capitalize()
            country_info = get_country_info(country_name)
            message = str(country_info)
        else:
            message = "Bad Request: Please provide a country parameter."

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

        return


