import os
import requests
import logging

log = logging.getLogger(__name__)

def get_auth_token(base_url):
    """
    Helper method to handle the /ownSecurity/signIn flow.
    Extracts and returns the accessToken.
    """
    log.info("Attempting to authenticate and fetch access token...")
    
    email = os.getenv("GREENCITY_EMAIL")
    password = os.getenv("GREENCITY_PASSWORD")
    
    if not email or not password:
        raise ValueError("Security Error: Credentials not found! Please set GREENCITY_EMAIL and GREENCITY_PASSWORD environment variables.")
        
    login_url = f"{base_url}/ownSecurity/signIn"
    
    payload = {
        "email": email,
        "password": password,
        "projectName": "GREENCITY"
    }
    
    try:
        log.info(f"Sending POST request to {login_url} with secure payload.")
        
        response = requests.post(login_url, json=payload, timeout=10)
        
        response.raise_for_status() 
        
        access_token = response.json().get('accessToken')
        
        if not access_token:
            raise KeyError("Validation Error: 'accessToken' not found in the response payload.")
            
        log.info("Successfully extracted accessToken from response.")
        return access_token
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to authenticate. Connection error or invalid credentials: {e}")
        if response is not None:
            log.error(f"Server response details: {response.text}")
        raise