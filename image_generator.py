# image_generator.py
import cloudinary
import cloudinary.uploader
import uuid

def generate_new_image():
    # 🔁 Tukaj pride tvoj AI image generation koda, zaenkrat damo placeholder
    image_path = "drip_placeholder.jpg"  # Pot do AI-generirane slike

    # 📤 Upload v Cloudinary s unique public_id
    public_id = f"dante_{uuid.uuid4().hex}"
    upload_result = cloudinary.uploader.upload(image_path, public_id=public_id, folder="dante_arazo")

    return upload_result['secure_url']
