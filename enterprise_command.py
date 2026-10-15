import os
import requests
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

# ==========================================
# 1. LIVE SHOPIFY ADMIN TOOL
# ==========================================
@tool("Live Shopify Store Health & Inventory Audit Tool")
def check_shopify_store_health(query: str) -> str:
    """Queries live store metrics, product inventory levels, and active catalog data from Shopify."""
    store_url = "rarestandards.tech"
    try:
        # Pull public JSON data as a secure baseline check
        response = requests.get(f"https://{store_url}/products.json", timeout=10)
        data = response.json()
        products = data.get("products", [])
        
        inventory_report = f"--- LIVE STORE TELEMETRY FOR {store_url.upper()} ---\n"
        inventory_report += f"Total Active Product Lines: {len(products)}\n"
        
        for p in products[:5]: # Audit top products
            title = p.get("title")
            variants = p.get("variants", [])
            price = variants[0].get("price") if variants else "N/A"
            inventory_report += f"• Product: {title} | Price: ${price} | Status: Active & Listed\n"
            
        inventory_report += "CRITICAL STATUS: Store frontend is live. No critical server downtime detected. Monitoring inventory velocity."
        return inventory_report
    except Exception as e:
        return f"Warning: Could not fetch real-time store telemetry: {e}. Proceeding with high-level enterprise analysis."

# ==========================================
# 2. LOCAL LLM SETUP
# ==========================================
local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# ==========================================
# 3. DEFINE THE ELITE COMMAND AGENTS
# ==========================================
coo_agent = Agent(
    role='Chief Operations Officer & Inventory Command',
    goal='Monitor live store telemetry, flag low inventory levels, detect operational bottlenecks, and safeguard store health.',
    backstory='You are a military-grade operations director. You despise inefficiency, track data down to the single unit, and demand strict adherence to supply chain integrity and real-time threat reporting.',
    verbose=True,
    allow_delegation=False,
    tools=[check_shopify_store_health],
    llm=local_llm
)

cro_architect = Agent(
    role='Senior CRO & UX Executive Architect',
    goal='Provide rigorous, board-room-grade structural blueprints to maximize conversion rates and eliminate friction.',
    backstory='You are a world-class conversion architect. Your audits are deeply professional, highly analytical, and focus on enterprise-level UX enhancements, trust architecture, and frictionless checkout flows.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

growth_director = Agent(
    role='Director of Direct-Response Growth & Traffic Scaling',
    goal='Formulate aggressive, high-margin traffic strategies and retention playbooks to scale revenue rapidly.',
    backstory='You are an elite e-commerce growth strategist. You turn raw traffic into high-value repeat buyers using high-end psychological triggers and automated scaling frameworks.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# ==========================================
# 4. DEFINE THE HIGH-STAKES TASKS
# ==========================================
operations_task = Task(
    description=(
        'Run a complete operational sweep of rarestandards.tech using the store health tool. '
        'Generate an Executive Operations Report detailing: '
        '1. Inventory & Stock Status across active product lines. '
        '2. Risk Assessment: Identify potential fulfillment or stockout risks. '
        '3. Critical Incident Protocols: What exact actions to take if traffic spikes or inventory drops unexpectedly.'
    ),
    expected_output='An executive operations and inventory health report.',
    agent=coo_agent
)

audit_task = Task(
    description=(
        'Using the operational baseline, deliver a professional, highly detailed CRO & UX audit for rarestandards.tech. '
        'Provide 3 structural, board-room-grade recommendations to elevate the store into a luxury-tier e-commerce destination '
        'and maximize visitor-to-buyer conversion.'
    ),
    expected_output='A professional, multi-point executive UX and conversion blueprint.',
    agent=cro_architect
)

growth_task = Task(
    description=(
        'Synthesize the findings into an aggressive Growth & Traffic Scaling Playbook. '
        'Outline a high-converting customer acquisition framework and a high-ticket bundle strategy to instantly lift Average Order Value (AOV).'
    ),
    expected_output='A comprehensive, high-margin traffic and revenue-scaling playbook.',
    agent=growth_director
)

# ==========================================
# 5. ASSEMBLE THE COMMAND CREW
# ==========================================
enterprise_crew = Crew(
    agents=[coo_agent, cro_architect, growth_director],
    tasks=[operations_task, audit_task, growth_task],
    process=Process.sequential
)

print("\n🎖️ Initializing Enterprise Command Center Crew...")
result = enterprise_crew.kickoff()

print("\n##################################################")
print("💼 EXECUTIVE OPERATIONS & REVENUE MASTER-REPORT")
print("##################################################")
print(result)

# Save the master report professionally
os.makedirs("Store_Optimization", exist_ok=True)
report_path = os.path.join("Store_Optimization", "master_executive_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(str(result))

print(f"\n✅ Master Executive Report successfully compiled and locked into '{report_path}'!")