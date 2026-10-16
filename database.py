# Import SQLite, which is already included with Python
import sqlite3

# Import datetime so we can save the time of each question
from datetime import datetime


# This function creates the database table if it does not exist already
def create_table():
    # Create or open the local database file
    connection = sqlite3.connect("rag_app.db")

    # cursor lets us execute SQL commands
    cursor = connection.cursor()

    # Create a table to store RAG questions and answers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Save the table creation
    connection.commit()

    # Close database connection
    connection.close()


# This function saves one question and its answer
def save_question(question, answer):
    # Open the database
    connection = sqlite3.connect("rag_app.db")
    cursor = connection.cursor()

    # Add one new row to the table
    # ? placeholders safely insert Python values into SQL
    cursor.execute(
        """
        INSERT INTO question_history (question, answer, created_at)
        VALUES (?, ?, ?)
        """,
        (
            question,
            answer,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    # Save the new row
    connection.commit()

    # Close database connection
    connection.close()


# This function gets saved history, newest first
def get_history():
    # Open the database
    connection = sqlite3.connect("rag_app.db")
    cursor = connection.cursor()

    # Read all saved questions and answers
    cursor.execute("""
        SELECT question, answer, created_at
        FROM question_history
        ORDER BY id DESC
    """)

    # Store all rows returned by SELECT
    rows = cursor.fetchall()

    # Close database connection
    connection.close()

    # Give the rows back to app.py
    return rows
##added
    # Create a table where ticket-triage results will be saved
def create_ticket_table():
    connection = sqlite3.connect("rag_app.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticket_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Save one triaged ticket in the database
def save_ticket(ticket, category, priority, sentiment, summary):
    connection = sqlite3.connect("rag_app.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO ticket_history
        (ticket, category, priority, sentiment, summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            ticket,
            category,
            priority,
            sentiment,
            summary,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    connection.commit()
    connection.close()


# Return every saved ticket, newest first
def get_tickets():
    connection = sqlite3.connect("rag_app.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticket, category, priority, sentiment, summary, created_at
        FROM ticket_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return rows