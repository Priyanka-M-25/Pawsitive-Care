import sqlite3

# Connect to the database
conn = sqlite3.connect("pet_care_app.db")
cursor = conn.cursor()

# Create the pet_adoptions table (if it does not exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pet_adoptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stay INTEGER,
        space_requirement INTEGER,
        height REAL,
        animal_type INTEGER,
        predicted_breed TEXT
    )
''')

conn.commit()
print("Table 'pet_adoptions' has been created successfully.")



# Fetch all records from the pet_adoptions table after deletion
cursor.execute("SELECT * FROM pet_adoptions")
rows = cursor.fetchall()

# Print the data
print("\n📌 Pet Adoptions Data :")
if rows:
    for row in rows:
        print(row)
else:
    print("No data found in the pet_adoptions table.")

# Close the connection
conn.close()
