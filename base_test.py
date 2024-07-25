import requests
import json

# Custom API base URL and token
API_BASE_URL = "https://your-custom-api-base-url/v1"
API_KEY = "your_custom_api_key"

# Endpoint for the OpenAI API (for example, completions)
COMPLETION_ENDPOINT = f"{API_BASE_URL}/completions"

# Headers for the request
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Data to send in the request
data = {
    "model": "text-davinci-003",  # Specify the model you want to use
    "prompt": "Translate the following English text to French: 'Hello, how are you?'",
    "max_tokens": 50  # Control the response length
}

def test_openai_completion():
    response = requests.post(COMPLETION_ENDPOINT, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        completion = response.json()
        print("API Response:", json.dumps(completion, indent=2))
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_openai_completion()
