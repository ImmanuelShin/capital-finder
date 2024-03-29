from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

REST_COUNTRIES_NAME = "https://restcountries.com/v3.1/name"
REST_COUNTRIES_API_CAPITAL = "https://restcountries.com/v3.1/capital"

def get_country_info(name):
    """
    Fetches information about a country from the REST Countries API.

    Parameters:
        name (str): The common name of the country.

    Returns:
        dict or None: A dictionary containing information about the country if found, 
                      otherwise None.
    """
    response = requests.get(f"{REST_COUNTRIES_NAME}/{name}")
    if response.status_code == 200:
        country_data = response.json()[0]
        return country_data
    else:
        return None
    
def get_country_info_by_capital(capital):
    """
    Fetches information about a country by searching for its capital.

    Parameters:
        capital (str): The capital city of the country.

    Returns:
        dict or None: A dictionary containing information about the country if found, 
                      otherwise None.
    """
    response = requests.get(f"{REST_COUNTRIES_API_CAPITAL}/{capital}")
    if response.status_code == 200:
        country_data = response.json()[0]
        return country_data
    else:
        return None
    
def generate_response(country_info, int, cap=None):
    """
    Generates a response message based on the country information.

    Parameters:
        country_info (dict): A dictionary containing information about the country.
        response_type (int): An integer indicating the response format:
                             - 1: "The capital of X is Y" for country queries.
                             - 2: "{cap} is the capital of X" for capital queries.
        cap (str, optional): The capital name (used in case of response_type == 2).

    Returns:
        str: A formatted response message.
    """
    message = ''
    if int == 1:
        country_name = country_info.get("name", {}).get("common", "N/A")
        country_capitals = country_info.get("capital", ["N/A"])
        if len(country_capitals) == 1:
            message = f"The capital of {country_name} is {country_capitals[0]}."
        else:
            message = "N/A"
    if int == 2:
        country_name = country_info.get("name", {}).get("common", "N/A")
        message = f"{cap} is the capital of {country_name}."

    return message

class handler(BaseHTTPRequestHandler):
    """
    Handles incoming GET requests and responds accordingly based on the provided parameters.

    Returns:
        None
    """
    def do_GET(self):
        """
        Handles GET requests and sends an appropriate response.

        Returns:
            None
        """
        url_components = parse.urlsplit(self.path)
        query_string_list = parse.parse_qsl(url_components.query)
        query_params = dict(query_string_list)

        if "country" in query_params:
            country_name = query_params["country"].capitalize()
            country_info = get_country_info(country_name)

            if country_info:
                message = generate_response(country_info, 1)
            else:
                message = f"Country not found: {country_name}."

        elif "capital" in query_params:
            capital_name = query_params["capital"].capitalize()
            country_capital = get_country_info_by_capital(capital_name)

            if country_capital:
                message = generate_response(country_capital, 2, capital_name)
            else:
                message = f"Capital not found: {capital_name}."

        else:
            message = "Bad Request: Please provide a country or capital parameter."

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

        return