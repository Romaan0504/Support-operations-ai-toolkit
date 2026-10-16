# Import Chroma for vector search
import chromadb

# Import Streamlit for browser UI
import streamlit as st

# Load GROQ_API_KEY from the .env file
from dotenv import load_dotenv

# Import Groq client to call the LLM
from groq import Groq

# Import our own database functions from database.py
from database import create_table, get_history, save_question


# Load variables from .env
load_dotenv()

# Create the SQLite table when the app starts
create_table()

# Set browser tab name
st.set_page_config(page_title="Policy Assistant")

# App heading
st.title("Company Policy Assistant")

# Small description under heading
st.write("Ask questions about refunds, passwords, delivery, or support.")


# These are our small company-policy document chunks
documents = [
    "Refunds are available within 14 days of purchase if the customer provides an order number.",
    "Customers can reset their password from the login page using the Forgot Password link.",
    "Standard delivery usually takes 5 to 7 business days.",
    "Priority support is available only for Premium plan customers.",
]


# Create a local Chroma vector database
client = chromadb.Client()

# Create or open a collection called company_policies
collection = client.get_or_create_collection(
    name="company_policies"
)

# Save/update policy text inside Chroma
collection.upsert(
    ids=["policy-1", "policy-2", "policy-3", "policy-4"],
    documents=documents,
)


# Create a text box in the browser for the user's question
question = st.text_input(
    "Your question",
    placeholder="Example: How long does delivery take?",
)


# Run this code only when the user clicks Ask
if st.button("Ask", type="primary"):

    # Stop if the user clicked Ask without writing a question
    if not question.strip():
        st.warning("Please enter a question first.")

    else:
        # Search Chroma and get the two most relevant policy chunks
        results = collection.query(
            query_texts=[question],
            n_results=2,
        )

        # Get the returned text chunks
        relevant_chunks = results["documents"][0]

        # Combine chunks into one context string for the LLM
        context = "\n".join(
            f"- {chunk}" for chunk in relevant_chunks
        )

        # Create Groq LLM client
        groq_client = Groq()

        # Ask Groq to answer only from retrieved policy information
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict customer-support assistant. "
                        "Answer only when the policy information directly answers the question. "
                        "Do not guess, assume, or use outside knowledge. "
                        "If the answer is missing or unclear, say exactly: "
                        "'I don't know based on the available policies.'"
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
Policy information:
{context}

Question:
{question}
""",
                },
            ],
        )

        # Extract plain answer text from Groq response
        answer = response.choices[0].message.content

        # Display the answer in browser
        st.subheader("Answer")
        st.write(answer)

        # Save this question, answer, and timestamp in SQLite
        save_question(question, answer)

        # Display the document chunks used as sources
        st.subheader("Sources used")
        for chunk in relevant_chunks:
            st.write(f"- {chunk}")


# Add a visual dividing line
st.divider()

# Show saved database history
st.subheader("Question History")

# Get all saved rows from SQLite
history = get_history()

# Show a message if the database has no history yet
if not history:
    st.write("No saved questions yet.")

# Display each saved question, answer, and timestamp
for saved_question, saved_answer, created_at in history:
    st.write(f"**Question:** {saved_question}")
    st.write(f"**Answer:** {saved_answer}")
    st.caption(f"Asked on: {created_at}")