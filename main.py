from scheduler import should_post_now
from image_generator import generate_image
from caption_generator import generate_caption
from poster import post_to_facebook

if should_post_now():
    print("🟢 Čas za objavo!")
    image_url = generate_image()
    caption = generate_caption()
    post_to_facebook(image_url, caption)
else:
    print("🔵 Ni še čas za objavo.")
