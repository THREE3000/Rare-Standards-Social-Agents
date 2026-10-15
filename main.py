import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. Connect to the free local Ollama server
local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# 2. Define the Agents
copywriter = Agent(
    role='Lead Social Media Strategist',
    goal='Write initial drafts for tech-savvy social media captions.',
    backstory='You are a digital marketer. You understand specs like RPM, VRAM, and GaN charging technology.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

editor = Agent(
    role='Quality Assurance Editor',
    goal='Refine marketing copy to ensure it sounds human, professional, and avoids generic AI cliches.',
    backstory='You are a strict editor for Rare Standards, a premium Enterprise IT brand. You hate generic phrases like "Say goodbye to" or "Level up". You rewrite copy to be punchy, authoritative, and highly technical.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# 3. Define the Tasks
write_task = Task(
    description='Write 3 engaging TikTok captions and a 3-part Twitter (X) thread promoting the Wolfbox MegaFlow MF100 Electric Air Duster (150,000 RPM, rechargeable).',
    expected_output='Three short TikTok captions and one Twitter thread.',
    agent=copywriter
)

edit_task = Task(
    description='Review the copywriter\'s draft. Completely rewrite any generic hooks. Ensure the tone is highly professional and appeals directly to PC builders and IT professionals.',
    expected_output='The final, polished Twitter thread and TikTok captions ready for publishing.',
    agent=editor
)

# 4. Assemble the Crew
rare_standards_crew = Crew(
    agents=[copywriter, editor],
    tasks=[write_task, edit_task],
    process=Process.sequential # The Copywriter drafts, then the Editor reviews
)

# Run the crew!
print("Starting the Multi-Agent Crew...")
result = rare_standards_crew.kickoff()

print("######################")
print("FINAL POLISHED RESULT")
print("######################")
print(result)