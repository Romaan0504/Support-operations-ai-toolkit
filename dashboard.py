# Counter counts repeated values, such as Delivery appearing many times
from collections import Counter

# Streamlit creates the browser dashboard
import streamlit as st

# Get tickets saved in SQLite
from database import get_tickets


# Browser tab title and layout
st.set_page_config(page_title="Support Analytics", layout="wide")

# Dashboard heading
st.title("Support Operations Dashboard")
st.write("Analytics from AI-triaged customer support tickets.")

# Get all saved ticket records from SQLite
tickets = get_tickets()

# Stop neatly if there is no data yet
if not tickets:
    st.warning("No tickets found yet. Run triage_ticket.py a few times first.")
    st.stop()

# Separate each database column into its own list
categories = [ticket[1] for ticket in tickets]
priorities = [ticket[2] for ticket in tickets]
sentiments = [ticket[3] for ticket in tickets]

# Create headline metric boxes
column_1, column_2, column_3 = st.columns(3)

column_1.metric("Total tickets", len(tickets))
column_2.metric("High-priority tickets", priorities.count("High"))
column_3.metric("Negative tickets", sentiments.count("Negative"))

# Count how many tickets belong to each category
category_counts = Counter(categories)

st.subheader("Tickets by Category")
st.bar_chart(category_counts)

# Count tickets by priority
priority_counts = Counter(priorities)

st.subheader("Tickets by Priority")
st.bar_chart(priority_counts)

# Show the latest tickets
st.subheader("Recent Tickets")

for ticket, category, priority, sentiment, summary, created_at in tickets:
    st.write(f"**Category:** {category} | **Priority:** {priority} | **Sentiment:** {sentiment}")
    st.write(f"**Customer ticket:** {ticket}")
    st.write(f"**AI summary:** {summary}")
    st.caption(f"Created: {created_at}")
    st.divider()