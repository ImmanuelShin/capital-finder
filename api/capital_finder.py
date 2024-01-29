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
    
def generate_response(country_info):
    country_name = country_info.get("name", {}).get("common", "N/A")
    country_capitals = country_info.get("capital", ["N/A"])
    
    currencies_data = country_info.get("currencies", {})
    currencies_info = []

    for currency_code, currency_data in currencies_data.items():
        currency_name = currency_data.get("name", "N/A")
        currency_symbol = currency_data.get("symbol", "N/A")
        currencies_info.append((currency_name, currency_code, currency_symbol))

    currencies_formatted = ", ".join(currencies_info)

    country_languages = list(country_info.get("languages", {}).values())

    response = f"Country: {country_name}\n"
    response += f"Capitals: {', '.join(country_capitals)}\n"
    response += f"Currencies: {', '.join(currencies_formatted)}\n"
    response += f"Languages: {', '.join(country_languages)}"

    return response

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url_components = parse.urlsplit(self.path)
        query_string_list = parse.parse_qsl(url_components.query)
        query_params = dict(query_string_list)

        if "country" in query_params and "capital" in query_params:
            country_name = query_params["country"].capitalize()
            capital_name = query_params["capital"].capitalize()
            
            country_info = get_country_info(country_name)

            if country_info and capital_name in country_info.get("capital", []):
                message = f"Correct! The capital of {country_name} is {capital_name}\n"
                message += generate_response(country_info)
            else:
                message = f"Invalid country/capital combination: {country_name}/{capital_name}."

        elif "country" in query_params:
            country_name = query_params["country"].capitalize()
            country_info = get_country_info(country_name)

            if country_info:
                message = generate_response(country_info)
            else:
                message = f"Country not found: {country_name}."

        elif "capital" in query_params:
            capital_name = query_params["capital"].capitalize()
            country_info = next((info for info in get_country_info("") if capital_name in info.get("capital", [""]).lower()), None)

            if country_info:
                message = generate_response(country_info)
            else:
                message = f"Capital not found: {capital_name}."

        else:
            message = "Bad Request: Please provide a country or capital parameter."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

        return