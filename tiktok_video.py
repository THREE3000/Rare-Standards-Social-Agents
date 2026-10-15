import os
import random
import requests
from crewai import Agent, Task, Crew, Process, LLM
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip

# ==========================================
# 1. LIVE SHOPIFY CATALOG SYNC
# ==========================================
# Replace these with your actual Shopify store details if needed, 
# or keep your dynamic list. To pull live items automatically:
SHOPIFY_STORE_URL = "rarestandards.tech"

def fetch_shopify_catalog():
    """Dynamically fetches products from your live Shopify store so new items are auto-added."""
    try:
        # Shopify public JSON endpoint for products
        response = requests.get(f"https://{SHOPIFY_STORE_URL}/products.json")
        data = response.json()
        catalog = []
        for product in data.get("products", []):
            name = product.get("title")
            handle = product.get("handle")
            url = f"https://{SHOPIFY_STORE_URL}/products/{handle}"
            # Grab the primary product image if available
            images = product.get("images", [])
            image_url = images[0]["src"] if images else "https://rarestandards.tech/cdn/shop/files/default.jpg"
            
            catalog.append({
                "name": name,
                "url": url,
                "media_vault": [image_url],
                "angle": f"Premium design and elite performance of {name}"
            })
        return catalog
    except Exception as e:
        print(f"⚠️ Live sync fallback triggered: {e}")
        # Fallback static list if network is down
        return [
            {
                "name": "Wolfbox MegaFlow MF100 Electric Air Duster", 
                "media_vault": ["https://rarestandards.tech/cdn/shop/files/3239-HG_TurboFan_GPCT5104.0.td_size_1_1c8df284-28df-4068-a1e9-1ec2bb54cd92.webp?v=1791907518&width=1100"],
                "angle": "150,000 RPM raw power & eliminating disposable canned air costs"
            }
        ]

# Load catalog dynamically
rare_standards_catalog = fetch_shopify_catalog()

# ==========================================
# 2. ANTI-DUPLICATE MEMORY SYSTEM
# ==========================================
HISTORY_FILE = "post_history.txt"

def get_recent_products():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()][-3:] # Keeps track of last 3 posts
    return []

def log_product_used(product_name):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{product_name}\n")

recent_posts = get_recent_products()
available_products = [p for p in rare_standards_catalog if p["name"] not in recent_posts]

# If all products have been used recently, reset memory pool
if not available_products:
    available_products = rare_standards_catalog

daily_pick = random.choice(available_products)
product_of_the_day = daily_pick["name"]
product_image_url = daily_pick["media_vault"][0]
selling_angle = daily_pick["angle"]
product_link = daily_pick.get("url", "https://rarestandards.tech")

log_product_used(product_of_the_day)
print(f"🎬 Selected Product (Memory Verified): {product_of_the_day}")

# ==========================================
# 3. LOCAL LLM INITIALIZATION
# ==========================================
local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# ==========================================
# 4. ELITE DIRECTOR AGENT & SCRIPTING
# ==========================================
director = Agent(
    role='Elite Direct-Response TikTok Commercial Director',
    goal='Write a witty, high-converting, million-dollar commercial script for luxury tech.',
    backstory='You are a top-tier commercial director known for sharp, self-aware luxury tech spots. You hook viewers in 2 seconds flat.',
    allow_delegation=False,
    llm=local_llm
)

script_task = Task(
    description=(
        f'You are a multi-award-winning commercial director for luxury tech. Write a 15-second high-converting TikTok script for the "{product_of_the_day}". '
        f'Core luxury positioning: {selling_angle}. '
        'Tone: Premium, razor-sharp, effortlessly funny, high-status. '
        'Structure precisely into: '
        '1. [VISUAL & AUDIO CUE]: Cinematic, relatable luxury frustration. '
        '2. [VOICEOVER]: Deadpan, high-end commercial voiceover. '
        '3. [THE FLEX / CTA]: Closing transition directing traffic to ' + product_link + '. '
        'After the script, start a new line with exactly "CAPTION:" followed by a clean, high-converting caption with 3 hashtags. '
        'CRITICAL: No AI intro chatter, no quotation marks around the output.'
    ),
    expected_output='Cinematic commercial blueprint followed by CAPTION: and raw caption text.',
    agent=director
)

tiktok_crew = Crew(agents=[director], tasks=[script_task], process=Process.sequential)
result = tiktok_crew.kickoff()
raw_output = result.raw

if "CAPTION:" in raw_output:
    parts = raw_output.split("CAPTION:")
    voiceover_text = parts[0].strip().replace('"', '')
    tiktok_caption = parts[1].strip()
else:
    voiceover_text = raw_output.strip().replace('"', '')
    tiktok_caption = f"Elevate your setup with the {product_of_the_day}. Available now at {product_link}. #RareStandards #LuxuryTech"

print("🎙️ Synthesizing voiceover audio...")
tts = gTTS(text=voiceover_text, lang='en', tld='com', slow=False)
tts.save("voiceover.mp3")

# ==========================================
# 5. RENDERING VIDEO ASSET
# ==========================================
print("🖼️ Fetching high-res store asset...")
img_bytes = requests.get(product_image_url).content
with open("product_image.jpg", 'wb') as img_file:
    img_file.write(img_bytes)

print("🎞️ Rendering high-fps video asset...")
audio_clip = AudioFileClip("voiceover.mp3")
image_clip = ImageClip("product_image.jpg").set_duration(audio_clip.duration)
video_clip = image_clip.set_audio(audio_clip)

output_filename = "ready_to_post_tiktok.mp4"
video_clip.write_videofile(
    output_filename, 
    fps=30, 
    codec="libx264", 
    audio_codec="aac",
    preset="medium",
    bitrate="3000k"
)

audio_clip.close()
video_clip.close()

# ==========================================
# 6. PACKAGING OUTPUT
# ==========================================
print("\n📦 Organizing assets into output directory...")
os.makedirs("TikTok_Ready_Content", exist_ok=True)

if os.path.exists(output_filename):
    os.replace(output_filename, os.path.join("TikTok_Ready_Content", output_filename))

caption_path = os.path.join("TikTok_Ready_Content", "caption.txt")
with open(caption_path, "w", encoding="utf-8") as cap_file:
    cap_file.write(tiktok_caption)

print("🚀 Elite System Upgraded! Auto-synced with Shopify & Anti-Duplicate Memory Engaged.")