import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from duckduckgo_search import DDGS

# 1. Build our own custom, crash-free search tool!
@tool("Web Search Tool")
def search_tool(search_query: str) -> str:
    """Search the web for real-world information and product specs."""
    with DDGS() as ddgs:
        # Grab the top 3 search results from DuckDuckGo
        results = [r for r in ddgs.text(search_query, max_results=3)]
        return str(results)

# 2. Connect to the free local Ollama server
local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# 3. Define the Agents
researcher = Agent(
    role='Tech Hardware Researcher',
    goal='Search the internet for accurate product specifications and prevent hallucinated data.',
    backstory='You are a meticulous hardware analyst. You only trust real data. You search the web for exact product specs (like weight, RPM, features) and provide bulletproof fact sheets.',
    verbose=True,
    allow_delegation=False,
    tools=[search_tool], # <--- Giving the agent your newly built tool!
    llm=local_llm
)

copywriter = Agent(
    role='Lead Social Media Strategist',
    goal='Write initial drafts for tech-savvy social media captions based STRICTLY on the provided research.',
    backstory='You are a digital marketer. You write engaging copy but you NEVER invent specs. You only use the facts provided by the researcher.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

editor = Agent(
    role='Quality Assurance Editor',
    goal='Refine marketing copy to ensure it sounds human, professional, and avoids generic AI cliches.',
    backstory='You are a strict editor for Rare Standards, a premium Enterprise IT brand. You rewrite copy to be punchy, authoritative, and highly technical.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# 4. Define the Tasks
research_task = Task(
    description='Search the internet for the exact specifications of the "Wolfbox MegaFlow MF100 Electric Air Duster". Find its true RPM, attachments, and main features. Create a factual bulleted list.',
    expected_output='A strict, factual bulleted list of the product\'s exact specifications.',
    agent=researcher
)

write_task = Task(
    description='Using ONLY the facts from the research step, write 3 engaging TikTok captions and a 3-part Twitter (X) thread promoting the product. Do not invent any numbers or features.',
    expected_output='Three short TikTok captions and one Twitter thread.',
    agent=copywriter
)

edit_task = Task(
    description='Review the copywriter\'s draft. Completely rewrite any generic hooks. Ensure the tone is highly professional and appeals directly to PC builders and IT professionals.',
    expected_output='The final, polished Twitter thread and TikTok captions ready for publishing.',
    agent=editor
)

# 5. Assemble the Crew
rare_standards_crew = Crew(
    agents=[researcher, copywriter, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential 
)

# Run the crew!
print("Starting the Custom Search-Enabled Crew...")
result = rare_standards_crew.kickoff()

print("######################")
print("FINAL FACT-CHECKED RESULT")
print("######################")
print(result)