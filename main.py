import os
import random
import requests
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS

# ==========================================
# 1. YOUR FULL 10-PRODUCT CATALOG
# ==========================================
rare_standards_catalog = [
    {
        "name": "Wolfbox MegaFlow MF100 Electric Air Duster", 
        "url": "https://rarestandards.tech/products/compressed-air-duster",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/3239-HG_TurboFan_GPCT5104.0.td_size_1_1c8df284-28df-4068-a1e9-1ec2bb54cd92.webp?v=1791907518&width=1100"]
    },
    {
        "name": "HyperGear UpRite Air Portable Laptop Cooling Stand", 
        "url": "https://rarestandards.tech/products/uprite-air-portable-laptop-cooling-stand",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/956-15614.0.td_size_1_117c5e35-8621-4e83-b765-36b802c1b3d1.webp?v=1791907240&width=1100"]
    },
    {
        "name": "HyperGear MaxCharge Pro 3-in-1 MagSafe Stand", 
        "url": "https://rarestandards.tech/products/hypergear-maxcharge-pro-3-in-1-magsafe-charging-stand",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/274-16189-HYP.0.td_size_1.webp?v=1791907360&width=1100"]
    },
    {
        "name": "Naztech Nexus T100 100W USB-C GaN Charger", 
        "url": "https://rarestandards.tech/products/naztech-nexus-t100-100w-usb-c-pd-usb-3-port",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/274-16118-HYP.0.td_size_1_414773b1-e670-4943-8103-0fd4bec52daf.webp?v=1791907345&width=1100"]
    },
    {
        "name": "5 Core Recording Podcast Bundle", 
        "url": "https://rarestandards.tech/products/recording-microphone-podcast-bundle-professional-condenser-cardioid-mic-kit-w-boom-arm",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/3206-RM_208_20BG.0.td_size_1_8dea785a-3738-4d11-8c87-56db28358faa.webp?v=1791907355&width=1100"]
    },
    {
        "name": "HyperGear 10000mAh Wireless Solar Power Bank", 
        "url": "https://rarestandards.tech/products/solar-10000mah-wireless-power-bank",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/956-633755146596.0.td_size_1_e408e260-c51a-488c-9c08-6b2c44152a70.webp?v=1791907334&width=1100"]
    },
    {
        "name": "EZ Sleep Eye Blind Fold with Bluetooth Music", 
        "url": "https://rarestandards.tech/products/ez-sleep-eye-blind-fold-with-bluetooth-music",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/1249-33014654632022.0.td_size_1_b9f6698e-ae22-4664-abc7-a1954231f40e.webp?v=1791907453&width=1100"]
    },
    {
        "name": "3-Channel Dash Cam Front Inside Rear", 
        "url": "https://rarestandards.tech/products/3-channel-dash-cam-front-inside-rear",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/3239-CA_CarDashCam_GPCT4210.0.td_size_1_fbf7a498-48f2-4a58-a5ec-12a198b7e34f.webp?v=1791907339&width=1100"]
    },
    {
        "name": "HyperGear CineMini Portable Mini Projector", 
        "url": "https://rarestandards.tech/products/hypergear-cinemini-portable-mini-projector",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/274-16072-HYP.0.td_size_1_1afaa6e9-cf14-4e54-8df6-e27dfd8e6dfb.webp?v=1791907393&width=1100"]
    },
    {
        "name": "Marquee Innovations Roadproof Heads Up Display", 
        "url": "https://rarestandards.tech/products/roadproof-heads-up-display-3-5",
        "media_vault": ["https://rarestandards.tech/cdn/shop/files/2637-RPFHUD01.0.td_size_1_e7716ddf-c40c-4b34-afb5-4f188ebd9487.webp?v=1791907329&width=1100"]
    }
]

# Pick a random product
daily_pick = random.choice(rare_standards_catalog)
product_of_the_day = daily_pick["name"]
product_link = daily_pick["url"]
available_media = daily_pick["media_vault"]

print(f"Today's target: {product_of_the_day}")

# ==========================================
# 2. TOOLS AND LLM SETUP
# ==========================================
@tool("Web Search Tool")
def search_tool(search_query: str) -> str:
    """Search the web for real-world information and product specs."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(search_query, max_results=3)]
        return str(results)

local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# ==========================================
# 3. DEFINE THE 4 AGENTS
# ==========================================
researcher = Agent(
    role='Tech Hardware Researcher',
    goal='Search the internet for accurate product specifications.',
    backstory='You search the web for exact product specs and provide bulletproof fact sheets.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=local_llm
)

copywriter = Agent(
    role='Lead Social Media Strategist',
    goal='Write initial drafts for tech-savvy social media captions based STRICTLY on the provided research.',
    backstory='You write engaging copy but NEVER invent specs.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

editor = Agent(
    role='Quality Assurance Editor',
    goal='Refine marketing copy to ensure it sounds professional and includes the correct website link.',
    backstory='You are a strict editor for Rare Standards. You rewrite copy to be punchy and highly technical.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

media_director = Agent(
    role='Visual Asset Manager',
    goal='Select the single best official media URL from the vault to accompany the post.',
    backstory='You are an Art Director. You analyze the written post and select the most relevant official image URL to maximize engagement. You NEVER invent URLs.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# ==========================================
# 4. DEFINE THE 4 TASKS
# ==========================================
research_task = Task(
    description=f'Search for specs of the "{product_of_the_day}". Create a factual bulleted list.',
    expected_output='A factual bulleted list of specifications.',
    agent=researcher
)

write_task = Task(
    description=(
        f'Using the research, write 1 engaging Facebook post for the "{product_of_the_day}". '
        f'End with this exact link: {product_link}. '
        f'CRITICAL RULE: Output ONLY the exact text that will be posted. Do not include labels like "**Facebook Post:**", do not use quotation marks, and NEVER write content for other platforms like TikTok.'
    ),
    expected_output='The exact text of the Facebook post, with zero labels or filler.',
    agent=copywriter
)

edit_task = Task(
    description=(
        'Review the draft. Ensure it sounds professional. Verify the link is prominently displayed at the bottom. '
        'CRITICAL RULE: Strip out any conversational filler, labels, quotation marks, or extra platforms. The output must be 100% clean, raw text ready to be published.'
    ),
    expected_output='The final, polished Facebook post text only.',
    agent=editor
)

media_task = Task(
    description=(
        f'Review the final Facebook post. Select exactly ONE media URL from this approved vault: {available_media}. '
        f'CRITICAL: Return NOTHING but the raw URL starting with https. No other text.'
    ),
    expected_output='A single valid URL pointing to an image.',
    agent=media_director
)

# ==========================================
# 5. ASSEMBLE THE CREW
# ==========================================
rare_standards_crew = Crew(
    agents=[researcher, copywriter, editor, media_director],
    tasks=[research_task, write_task, edit_task, media_task],
    process=Process.sequential 
)

print("\nStarting the Autonomous Marketing Machine...")
result = rare_standards_crew.kickoff()

final_text = edit_task.output.raw
selected_media = result.raw.strip()

print("\n######################\nFINAL OUTPUT\n######################")
print(f"TEXT:\n{final_text}\n")
print(f"MEDIA URL:\n{selected_media}\n")

# ==========================================
# 6. SEND TO MAKE.COM
# ==========================================
webhook_url = "https://hook.us2.make.com/y6tcp9x1u2nt5x98stjqxaie0y9oba1c"

payload = {
    "social_copy": final_text,
    "media_url": selected_media
}

try:
    response = requests.post(webhook_url, json=payload)
    print(f"\nSuccessfully sent to Make.com Webhook! Status: {response.status_code}")
except Exception as e:
    print(f"\nFailed to send to Webhook: {e}")