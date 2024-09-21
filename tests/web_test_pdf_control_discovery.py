import requests
import os
import json

# Replace with your actual API Gateway URL
api_url = "https://bhqsyirakl.execute-api.us-east-1.amazonaws.com/Prod/pdf-control-discovery"


def test_discover_pdf_fields(template_name):
    """Test the API by sending a request to discover form fields in the PDF."""

    # Fetch the API key from the environment variable
    api_key = os.getenv('PDF_CONTROL_DISCOVERY_API_KEY')
    if not api_key:
        print("Error: API key not found. Please set the 'PDF_CONTROL_DISCOVERY_API_KEY' environment variable.")
        return

    # Prepare the request with the templateName as a query parameter
    params = {'templateName': template_name}

    # Set the headers, including the API key
    headers = {
        'x-api-key': api_key  # This is where API Gateway expects the API key
    }

    try:
        # Send the GET request to the API
        response = requests.get(api_url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f"Success! Response data: {json.dumps(response.json(), indent=4)}")
        elif response.status_code == 400:
            print(f"Client error: {response.status_code}. Message: {response.json().get('message')}")
        elif response.status_code == 403:
            print(f"Authentication error: {response.status_code}. Check your API key.")
        else:
            print(f"Unexpected error: {response.status_code}. Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error while calling the API: {str(e)}")


if __name__ == "__main__":
    # Test with a specific PDF template (replace with actual template name stored in your S3 bucket)
    test_discover_pdf_fields('template_form1.pdf')
