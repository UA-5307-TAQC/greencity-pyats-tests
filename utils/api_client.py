import os
import requests
import logging

log = logging.getLogger(__name__)

def get_auth_token(base_url):
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
        response = requests.post(login_url, json=payload, timeout=10)
        response.raise_for_status() 
        
        response_data = response.json()
        
        # Витягуємо І токен, І userId
        access_token = response_data.get('accessToken')
        user_id = response_data.get('userId') 
        
        if not access_token:
            raise KeyError("Validation Error: 'accessToken' not found in the response payload.")
            
        log.info(f"Successfully extracted accessToken and userId: {user_id}")
        
        return {"token": access_token, "user_id": user_id}
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to authenticate. Error: {e}")
        raise