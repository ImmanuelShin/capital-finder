import requests

REST_API_NAME = 'https://restcountries.com/v3.1/name'

def get_country_info(name):
  response = requests.get(f'{REST_API_NAME}/{name}')
  if response.status_code == 200:
    country_data = response.json()[0]
    return country_data
  else:
    return None

def handler(request):
    country = request.args.get("country")
    capital = request.args.get("capital")

    if country:
        country_name = country.capitalize()
        country_info = get_country_info(country_name)

        if country_info:
            country_capital = country_info["capital"][0]
            return f"The capital of {country_name} is {country_capital}.", 200
        else:
            return f"Country not found for {country_name}.", 404
    elif capital:
        capital_name = capital.capitalize()
        country_name = next((key for key, value in capitals.items() if value == capital_name), None)

        if country_name:
            return f"{capital_name} is the capital of {country_name}.", 200
        else:
            return f"Country not found for {capital_name}.", 404
    else:
        return "Bad Request: Please provide a country or capital parameter.", 400