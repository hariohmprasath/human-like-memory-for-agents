import os
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import shell

openai_model = OpenAIModel(
    model_id="gpt-5-nano",
    client_args={
        "api_key": "<<api-key>>"
    },
)

system_prompt = """
You are a companion agent that engages in friendly conversations. For context, here is the conversation history:
{message_history}

## Guidelines
- Listen and respond naturally to what the user shares
- Ask follow-up questions to keep the conversation flowing
- Be helpful and supportive
- Stay focused on the current conversation

Be very concise and to the point.
"""

print("Welcome to the companion agent! Type 'quit' to exit.")
message_history = []
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    agent = Agent(model=openai_model, system_prompt=system_prompt.format(message_history=message_history))
    response = agent(user_input)
    message_history.append("User: " + user_input)
    message_history.append("Assistant: " + str(response))
    print(response)
