# api_client.py
import requests

class ApiClient:
    def __init__(self, base_url="thunderstore.io", api_key=None):
        self.base_url = base_url
        self.api_key = api_key

    def _build_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"
    
    def validate_manifest_with_api(self, manifest_file):
        # Implement logic to send manifest data to API for validation
        # and handle API response
        url = " https://thunderstore.io/api/experimental/submission/validate/manifest-v1/"
        response = requests.post(url, json=manifest_file, headers={"Authorization": f"Bearer {self.api_key}"})
        print(response)
        # Process response and return True/False based on validation result
        if response.status_code == 200:
            api_response = response.json()
            return api_response.get('valid', False)
        else:
            # Handle API error response
            return False