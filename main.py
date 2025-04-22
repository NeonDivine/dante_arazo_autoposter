import openai
import requests
import random
import cloudinary
import cloudinary.uploader
import os
from datetime import datetime

# 🔐 API Ključi iz okolja
openai.api_key = os.getenv("OPENAI_API_KEY")
ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")  # ← uporabi pravi PAGE token
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
IG_USER_ID = os.getenv("IG_USER_ID")

# ☁️ Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# 👕 DRIPARA outfiti in lokacije (realistični + z logotipom)
outfits = [
    "black DRIPARA hoodie with embroidered logo on chest",
    "white oversized DRIPARA T-shirt with centered logo",
    "DRIPARA grey tracksuit with minimal logo design",
    "limited edition red DRIPARA hoodie and cap with logo detail",
    "blue DRIPARA hoodie with reflective print logo"
]

locations = [
    "urban basketball court at sunset",
    "modern rooftop with city skyline in background",
    "industrial warehouse with dramatic lighting",
    "Paris street with rain reflections",
    "crosswalk at golden hour with stylish shadow"
]

def allowed_to_post():
    manual_trigger = os.getenv("MANUAL_TRIGGER", "false").lower() == "true"
    if manual_trigger:
        return True
    now = datetime.utcnow()
    hour = now.hour
    return hour in [9, 14]  # 11:00 in 16:00 SLO (UTC+2)

def post_once():
    logs = []
    def log(msg):
        print(msg)
        logs.append(msg)

    if not allowed_to_post():
        log("⏳ Ni pravi čas za objavo, čakamo na naslednji slot.")
        return "\n".join(logs)

    outfit = random.choice(outfits)
    location = random.choice(locations)
    prompt = f"{outfit}, {location}, ultra-realistic fashion editorial photo, soft cinematic lighting, male model, drapery shadows"
    log(f"🎨 Generiram sliko z DALL·E: {prompt}")

    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
    except Exception as e:
        log(f"❌ Napaka pri generaciji slike: {e}")
        return "\n".join(logs)

    img_data = requests.get(image_url).content
    with open("generated_image.jpg", "wb") as f:
        f.write(img_data)

    uploaded = cloudinary.uploader.upload("generated_image.jpg")
    final_url = uploaded['secure_url']
    log(f"☁️ Slika naložena: {final_url}")

    caption_prompt = (
        "Napiši kratek, močan, avtentičen motivacijski citat v slovenščini. "
        "Tema: samozavest, napredek, disciplina. Dodaj 3 moderne hashtage. "
        "Zaključi s CTA kot 'komentiraj' ali 'deli'."
    )
    try:
        chat = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": caption_prompt}]
        )
        caption = chat.choices[0].message.content.strip()
    except Exception as e:
        caption = "Vzemi vajeti v svoje roke. #dripara #samozavest #bodiikona\n💬 Komentiraj spodaj!"
        log(f"⚠️ Napaka pri captionu: {e}")

    log(f"✍️ Caption: {caption}")

    # ✅ Objava na Facebook s PAGE TOKEN
    log("📘 Objavljam na Facebook stran...")
    fb_url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    fb_payload = {
        "url": final_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    fb_res = requests.post(fb_url, data=fb_payload).json()
    log(f"✅ FB objavljeno: {fb_res}")

    # ✅ Objava na Instagram
    log("📸 Objavljam na Instagram...")
    ig_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    media_payload = {
        "image_url": final_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    media_res = requests.post(ig_url, data=media_payload).json()

    if "id" in media_res:
        creation_id = media_res["id"]
        log(f"🧩 Media container ustvarjen: {creation_id}")

        publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
        publish_payload = {
            "creation_id": creation_id,
            "access_token": ACCESS_TOKEN
        }
        publish_res = requests.post(publish_url, data=publish_payload).json()
        log(f"✅ IG objavljeno: {publish_res}")
    else:
        log(f"⚠️ Napaka pri IG objavi: {media_res}")

    return "\n".join(logs)

if __name__ == '__main__':
    output = post_once()
    print("\n--- REZULTAT ---\n")
    print(output)
