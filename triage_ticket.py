# Convert LLM JSON text into Python data
import json

# Read the Groq API key from .env
from dotenv import load_dotenv

# Use Groq to call the LLM
from groq import Groq

# Import our database functions
from database import create_ticket_table, save_ticket


# Load the API key from .env
load_dotenv()

# Make sure the ticket table exists before saving anything
create_ticket_table()

# Create the Groq client
groq_client = Groq()

# Ask the user for a customer ticket
ticket = input("Paste a customer support ticket: ")

# Ask the LLM to classify the ticket
response = groq_client.chat.completions.create(
    model="openai/gpt-oss-20b",

    # Ask for JSON, not a normal paragraph
    response_format={"type": "json_object"},

    messages=[
        {
            "role": "system",
            "content": """
You are a support-ticket triage assistant.

Return ONLY valid JSON using exactly these fields:

{
  "category": "Refund, Delivery, Password, Billing, Account, or Other",
  "priority": "Low, Medium, or High",
  "sentiment": "Positive, Neutral, or Negative",
  "summary": "A short one-sentence summary",
  "suggested_reply": "A helpful professional reply"
}
"""
        },
        {
            "role": "user",
            "content": ticket
        }
    ]
)

# Get the JSON returned by the LLM
json_text = response.choices[0].message.content

# Convert JSON text into a Python dictionary
triage_result = json.loads(json_text)

# Save useful ticket fields in SQLite
save_ticket(
    ticket,
    triage_result["category"],
    triage_result["priority"],
    triage_result["sentiment"],
    triage_result["summary"],
)

# Show the result in the terminal
print("\n--- Ticket Triage Result ---")
print("Category:", triage_result["category"])
print("Priority:", triage_result["priority"])
print("Sentiment:", triage_result["sentiment"])
print("Summary:", triage_result["summary"])
print("Suggested reply:", triage_result["suggested_reply"])

print("\nTicket saved successfully in rag_app.db")