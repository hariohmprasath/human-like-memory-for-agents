from strands import Agent
from strands.models.openai import OpenAIModel

# --- Model Setup ---
model = OpenAIModel(
    model_id="gpt-5-nano",
    client_args={
        "api_key": "<<api-key>>"
    },
)

# --- Prompts ---
MEMORY_PROMPT = """Extract key information from this conversation as JSON:
- personal_info: name, location, occupation
- preferences: likes, dislikes, restrictions  
- entities: people, places, things mentioned
- summary: brief overview of conversation

Conversation:
{conversation}"""

COMPANION_PROMPT = """You are a friendly companion. Be concise.

Long-term memory about the user:
{memory}

Recent conversation:
{history}"""


def extract_memory(history: list) -> str:
    """Extract long-term memory from conversation history."""
    agent = Agent(model=model, system_prompt=MEMORY_PROMPT.format(conversation="\n".join(history)))
    return str(agent("Extract the key information."))


# --- Main Loop ---
memory = ""
history = []

print("Companion Agent (type 'quit' to exit, 'save' to extract memory)")
while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        break
    
    if user_input.lower() == "save":
        memory = extract_memory(history)
        history.clear()
        print(f"[Memory saved]\n{memory}\n")
        continue
    
    prompt = COMPANION_PROMPT.format(memory=memory or "None yet", history="\n".join(history) or "New conversation")
    agent = Agent(model=model, system_prompt=prompt)
    response = agent(user_input)
    
    history.append(f"User: {user_input}")
    history.append(f"Assistant: {response}")
    print(response)
