
import mysql.connector

# Define database connection parameters
db_config = {
    "host": "104.236.8.179",
    "user": "madeline",
    "password": "Madeline#123456",
    "database": "fsu",
}

# Function to create a database connection
def get_database_connection():
    return mysql.connector.connect(**db_config)


conn = get_database_connection()
cursor = conn.cursor(dictionary=True)

#cursor.execute("SELECT * FROM Property")
#property_record = cursor.fetchone()
#print(property_record)


query = """
    SELECT House.*, Property.price
    FROM House
    JOIN Property ON House.address = Property.address
"""

cursor.execute(query)
houses = cursor.fetchone()
print(houses)



