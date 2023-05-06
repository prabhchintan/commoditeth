from typing import Dict, Any, Optional
import os
import requests

# Define custom exception classes
class ApiError(Exception):
    """Exception raised for API-related errors."""
    def __init__(self, message: str):
        super().__init__(message)

class ApiUnexpectedError(Exception):
    """Exception raised for unexpected errors during API request."""
    def __init__(self, message: str):
        super().__init__(message)

# Define the default base URL for the commodities API
API_BASE_URL = 'https://commodities-api.com/api'

def process_rates(rates: Dict[str, float]) -> Dict[str, float]:
    """
    Process the rates and return the reciprocal values.

    Parameters:
        rates (Dict[str, float]): A dictionary of rates with keys as symbols.

    Returns:
        Dict[str, float]: A dictionary of processed rates with keys as symbols.
    """
    return {key: 1 / value if value != 0 else float('inf') for key, value in rates.items()}

def fetch_commodity_data(
    base: str,
    commodity: str,
    endpoint: str = 'latest',
    base_url: str = API_BASE_URL,
    access_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch commodity data from the external API.

    Parameters:
        base (str): The base currency.
        commodity (str): The commodity symbols separated by commas.
        endpoint (str): The API endpoint (default is 'latest').
        base_url (str): The base URL for the API (default is API_BASE_URL).
        access_key (str): Optional API key.

    Returns:
        dict: The JSON response from the API containing commodity data.
    """
    access_key = access_key or os.environ.get('API_KEY')
    if not access_key:
        raise ValueError('API key not found in environment variable API_KEY or provided as argument.')

    try:
        # Construct the URL for the API request
        url = f'{base_url}/{endpoint}'
        
        # Define query parameters as a dictionary
        query_params: Dict[str, str] = {
            'access_key': access_key,
            'base': base,
            'symbols': commodity
        }
        
        # Make the GET request with query parameters
        resp = requests.get(url, params=query_params)
        
        # Check for errors in the response status code
        resp.raise_for_status()
        
        response_data = resp.json()
        if response_data.get('data'):
            rates = response_data['data'].get('rates')
            if rates:
                processed_rates = process_rates(rates)
                response_data['data']['rates'] = processed_rates
        return response_data
    except requests.exceptions.HTTPError as e:
        raise ApiError(f"An API error occurred: {e}") from e
    except Exception as e:
        raise ApiUnexpectedError(f"An unexpected error occurred: {e}") from e

# Usage example
base = 'BTC'
commodity = 'COFFEE,LUMBER,BRENTOIL,XAU'
try:
    data = fetch_commodity_data(base, commodity)
    print(data)
except ApiError as e:
    print(e)
except ApiUnexpectedError as e:
    print(e)

# Note: This code cannot be run in this environment because it requires access to the internet
# and environment variables. Please run this code in your local Python environment.
