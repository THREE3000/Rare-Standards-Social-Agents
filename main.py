import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. Connect to your free local Ollama server using CrewAI's native LLM tool
local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# 2. Define the Agent
copywriter = Agent(
    role='Lead Social Media Strategist',
    goal='Write high-converting, tech-savvy social media captions for Rare Standards.',
    backstory=(
        'You are the lead digital marketer for Rare Standards, a premium Enterprise IT '
        'and Mobile Accessories brand. Your tone is authoritative, sharp, and engaging. '
        'You speak directly to PC builders, remote workers, and tech enthusiasts. '
        'You understand specs like RPM, VRAM, and GaN charging technology.'
    ),
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# 3. Define the Task
create_content = Task(
    description=(
        'Write 3 engaging TikTok captions and a 3-part Twitter (X) thread promoting '
        'the Wolfbox MegaFlow MF100 Electric Air Duster. Emphasize that it features a '
        '150,000 RPM motor, is rechargeable, and replaces the cost of disposable canned air. '
        'Include highly targeted hashtags.'
    ),
    expected_output='Three short TikTok captions with hooks, and one formatted Twitter thread.',
    agent=copywriter
)

# 4. Assemble the Crew and Kickoff
rare_standards_crew = Crew(
    agents=[copywriter],
    tasks=[create_content],
    process=Process.sequential
)

# Run the agent!
print("Starting the Local AI Agent...")
result = rare_standards_crew.kickoff()

print("######################")
print("FINAL RESULT")
print("######################")
print(result)