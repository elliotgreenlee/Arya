# Arya
Personal Assistant

Arya's design for her logo. 
![A networked 'A' character on a lavender background](Design%20Files/Arya%20Logo%20Scaled.png)

## Access

### APIs
Google cloud api credentials from https://console.cloud.google.com/auth/clients are needed
in client_secret.apps.googleusercontent.com.json
* google calendar
* google sheets

OpenWeather api credentials from https://home.openweathermap.org/api_keys are needed
in api_keys.json.

OpenAI api credentials from https://platform.openai.com/settings/organization/api-keys are
needed in api_keys.json.

Spoonacular api credentials from https://spoonacular.com/food-api/console#Profile are needed in
api_keys.json.

### Google User Consent
Users must be added to https://console.cloud.google.com/auth/audience to have test access.
On first use, a login screen will open to accept the app on your Google account.
A json file with your user credentials will be added to the Credentials folder.

*This will need to be regenerated to accept any new google APIs!*

## Requirements
- Generated with `pip freeze > requirements.txt`
- Install with `pip install -r requirements.txt`