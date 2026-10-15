import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS

# ==========================================
# 1. LIVE WEB SCRAPING & SEARCH TOOLS
# ==========================================
@tool("Web Scraping & Search Tool")
def live_store_analyzer(query: str) -> str:
    """Search live data and analyze e-commerce benchmarks for rarestandards.tech."""
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=4)]
        return str(results)

local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# ==========================================
# 2. DEFINE DUAL-ACTION AGENTS
# ==========================================
cro_analyst = Agent(
    role='Lead E-Commerce CRO & Store Auditor',
    goal='Audit the live infrastructure of rarestandards.tech and pinpoint exact user-experience conversion leaks.',
    backstory='You specialize in elite Shopify conversion architecture. You look at page structure, trust signals, bundle architecture, and checkout friction.',
    verbose=True,
    allow_delegation=False,
    tools=[live_store_analyzer],
    llm=local_llm
)

pricing_copywriter = Agent(
    role='Psychological Pricing & Luxury Copywriter',
    goal='Write high-converting, high-end product copy and retention flows that eliminate buyer hesitation.',
    backstory='You write magnetic, high-status copy that frames tech accessories as essential lifestyle upgrades rather than commodities.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# ==========================================
# 3. DEFINE THE DUAL TASKS
# ==========================================
audit_task = Task(
    description=(
        'Review the live e-commerce setup for "rarestandards.tech" (selling tech gadgets like air dusters and MagSafe stands). '
        'Provide a 2-part action plan: '
        '1. STORE AUDIT: Identify 2 specific layout or trust-building elements missing from standard Shopify templates that kill conversion rates. '
        '2. TRAFFIC MULTIPLIER: Outline a concrete "Bundle & Save" strategy for the catalog to immediately lift Average Order Value (AOV).'
    ),
    expected_output='A strategic store audit and AOV-boosting bundle blueprint.',
    agent=cro_analyst
)

copy_task = Task(
    description=(
        'Using the store optimization strategy, write: '
        '1. A high-impact, luxury-focused product description block for the Wolfbox Air Duster that focuses on lifetime savings and pristine performance. '
        '2. A 2-part automated Abandoned Cart email sequence to recover lost checkouts. '
        'Keep output clean and formatted.'
    ),
    expected_output='High-end product description and automated cart recovery emails.',
    agent=pricing_copywriter
)

# ==========================================
# 4. EXECUTE CREW
# ==========================================
conversion_crew = Crew(
    agents=[cro_analyst, pricing_copywriter],
    tasks=[audit_task, copy_task],
    process=Process.sequential
)

print("\n🚀 Initializing Dual-Action Store Optimization Crew...")
result = conversion_crew.kickoff()

print("\n##################################")
print("💰 DUAL-ACTION REVENUE BLUEPRINT")
print("##################################")
print(result)

# Save locally
os.makedirs("Store_Optimization", exist_ok=True)
output_path = os.path.join("Store_Optimization", "conversion_blueprint.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(str(result))

print(f"\n✅ Blueprint saved to '{output_path}'!")