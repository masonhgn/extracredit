from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Define database connection parameters
db_config = {
    "host": "104.236.8.179",
    "user": "root1",
    "password": "Root#123456",
    "database": "fsu",
}

# Function to create a database connection
def get_database_connection():
    return mysql.connector.connect(**db_config)




@app.route('/')
def homepage():
    return render_template('homepage.html')




# Route to display all listings and their associated property info
@app.route('/listings')
def display_listings():
    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch house listings
    cursor.execute("SELECT * FROM House")
    houses = cursor.fetchall()

    # Fetch business property listings
    cursor.execute("SELECT * FROM BusinessProperty")
    business_properties = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('listings.html', houses=houses, business_properties=business_properties)

# Route to search houses based on price range, bedrooms, and bathrooms
@app.route('/search_houses')
def search_houses():
    # Retrieve query parameters from the URL
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_bedrooms = request.args.get('min_bedrooms')
    min_bathrooms = request.args.get('min_bathrooms')

    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    # Construct the SQL query based on the provided parameters
    query = "SELECT * FROM House WHERE price BETWEEN %s AND %s AND bedrooms >= %s AND bathrooms >= %s"
    cursor.execute(query, (min_price, max_price, min_bedrooms, min_bathrooms))
    houses = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('house_search_results.html', houses=houses)

# Route to search business properties based on price range and size
@app.route('/search_business_properties')
def search_business_properties():
    # Retrieve query parameters from the URL
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    min_size = request.args.get('min_size')
    max_size = request.args.get('max_size')

    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    # Construct the SQL query based on the provided parameters
    query = "SELECT * FROM BusinessProperty WHERE price BETWEEN %s AND %s AND size BETWEEN %s AND %s"
    cursor.execute(query, (min_price, max_price, min_size, max_size))
    business_properties = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('business_property_search_results.html', business_properties=business_properties)



# Route to display all agents and their associated info
@app.route('/agents')
def display_agents():
    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all agents and their info from the database
    cursor.execute("SELECT * FROM Agent")
    agents = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('agents.html', agents=agents)



# Route to display all buyers and their associated info, including preferences
@app.route('/buyers')
def display_buyers():
    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all buyers and their info from the database
    cursor.execute("SELECT * FROM Buyer")
    buyers = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template('buyers.html', buyers=buyers)



if __name__ == '__main__':
    app.run(debug=True)

