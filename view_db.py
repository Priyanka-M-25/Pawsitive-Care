import sqlite3

# Connect to the database
conn = sqlite3.connect("pet_care_app.db")
cursor = conn.cursor()




# Fetch all records from the pet_adoptions table after deletion
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()


if rows:
    for row in rows:
        print(row)
else:
    print("No data found in the pet_adoptions table.")

# Close the connection
conn.close()
