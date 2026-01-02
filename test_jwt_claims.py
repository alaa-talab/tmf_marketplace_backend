import requests
import base64
import json

BASE_URL = "http://127.0.0.1:8000/api/auth"

def decode_token(token):
    # Decode the payload (second part of the token)
    try:
        payload = token.split('.')[1]
        # Add padding if needed
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        decoded = base64.b64decode(payload).decode('utf-8')
        return json.loads(decoded)
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

def test_login_claims():
    # Use the admin account we know exists (or create one if needed, but assume admin/admin from previous context or generic user)
    # Actually, let's use the 'admin' superuser we supposedly created, or register a fresh one.
    # To be safe, let's try to register a temp user first.
    
    username = "claim_test_user"
    password = "testpassword123"
    email = "claimtest@example.com"
    role = "Uploader"

    # 1. Register
    reg_response = requests.post(f"{BASE_URL}/register/", json={
        "username": username,
        "email": email,
        "password": password,
        "role": role
    })
    
    # If user already exists (400), that's fine, we proceed to login
    if reg_response.status_code == 201:
        print(f"User {username} registered successfully.")
    elif reg_response.status_code == 400 and "username" in reg_response.json():
        print(f"User {username} already exists, proceeding to login.")
    else:
        print(f"Registration failed: {reg_response.text}")
        # Assuming we can try logging in anyway if it's a known user
    
    # 2. Login
    login_response = requests.post(f"{BASE_URL}/login/", json={
        "username": username,
        "password": password
    })

    if login_response.status_code == 200:
        data = login_response.json()
        access_token = data.get('access')
        refresh_token = data.get('refresh')
        
        print("\nLogin Successful!")
        print(f"Access Token: {access_token[:20]}...")
        
        # 3. Decode and Inspect Claims
        claims = decode_token(access_token)
        if claims:
            print("\nToken Claims:")
            print(f"- Role: {claims.get('role')}")
            print(f"- Username: {claims.get('username')}")
            
            if claims.get('role') == role:
                print("\nSUCCESS: Role claim matches registered role!")
            else:
                print(f"\nFAILURE: Role mismatch. Expected {role}, got {claims.get('role')}")
        else:
            print("\nFAILURE: Could not decode token claims.")
    else:
        print(f"\nLogin Failed: {login_response.text}")

if __name__ == "__main__":
    test_login_claims()
