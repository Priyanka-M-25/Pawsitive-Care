import sqlite3

# Connect to the database
conn = sqlite3.connect("pet_care_app.db")
cursor = conn.cursor()

# Retrieve and display all pet records
cursor.execute("SELECT * FROM pets_info_details")
rows = cursor.fetchall()

print("Database Contents:")
for row in rows:
    print(row)

# Close the connection
conn.close()


