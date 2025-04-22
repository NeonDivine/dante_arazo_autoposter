import requests
from config import PAGE_ID, USER_ACCESS_TOKEN

def post_to_facebook(image_url, caption):
    # Pridobi page token
    token_url = f"https://graph.facebook.com/v19.0/{PAGE_ID}?fields=access_token&access_token={USER_ACCESS_TOKEN}"
    res = requests.get(token_url)
    page_token = res.json().get("access_token")

    # Objavi sliko
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
    payload = {
        "url": image_url,
        "caption": caption,
        "access_token": page_token
    }
    response = requests.post(url, data=payload)
    print(response.status_code)
    print(response.json())
