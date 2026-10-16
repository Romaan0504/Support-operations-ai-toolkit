# Import SQLite
import sqlite3

# Open the RAG app database
connection = sqlite3.connect("rag_app.db")

# Create cursor to run SQL
cursor = connection.cursor()

# Read saved ticket-triage rows
cursor.execute("""
    SELECT id, ticket, category, priority, sentiment, summary, created_at
    FROM ticket_history
    ORDER BY id ASC
""")

# Get all results
rows = cursor.fetchall()

# Print each saved ticket clearly
for row in rows:
    print("\nID:", row[0])
    print("Ticket:", row[1])
    print("Category:", row[2])
    print("Priority:", row[3])
    print("Sentiment:", row[4])
    print("Summary:", row[5])
    print("Created at:", row[6])

# Close the database
connection.close()



'''
# Import SQLite
import sqlite3

# Open the RAG app database
connection = sqlite3.connect("rag_app.db")

# Create cursor to run SQL
cursor = connection.cursor()

# Read saved rows
cursor.execute("""
    SELECT id, question, answer, created_at
    FROM question_history
    ORDER BY id asc
""")

# Get all results
rows = cursor.fetchall()

# Print each saved row in the terminal
for row in rows:
    print(row)

# Close the database
connection.close()
'''
