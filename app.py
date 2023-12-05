from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

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
    max_bedrooms = request.args.get('max_bedrooms')

    min_bathrooms = request.args.get('min_bathrooms')
    max_bathrooms = request.args.get('max_bathrooms')

    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    
    query = """
            SELECT House.*, Property.price
            FROM House
            JOIN Property ON House.address = Property.address
            WHERE 1=1
        """
        
    params = {}

    # Add conditions for price range
    if min_price is not None and len(min_price) > 0:
        query += " AND Property.price >= %(min_price)s"
        params['min_price'] = min_price

    if max_price is not None and len(max_price) > 0:
        query += " AND Property.price <= %(max_price)s"
        params['max_price'] = max_price

    # Add conditions for bedrooms and bathrooms if provided in the query parameters
    if min_bathrooms is not None and len(min_bathrooms) > 0:
        query += " AND House.bathrooms >= %(min_bathrooms)s"
        params['min_bathrooms'] = min_bathrooms

    if max_bathrooms is not None and len(max_bathrooms) > 0:
        query += " AND House.bathrooms <= %(max_bathrooms)s"
        params['max_bathrooms'] = max_bathrooms


    if min_bedrooms is not None and len(min_bedrooms) > 0:
        query += " AND House.bedrooms >= %(min_bedrooms)s"
        params['min_bedrooms'] = min_bedrooms

    if max_bedrooms is not None and len(max_bedrooms) > 0:
        query += " AND House.bedrooms <= %(max_bedrooms)s"
        params['max_bedrooms'] = max_bedrooms

    print(query)

    cursor.execute(query, params)
    houses = cursor.fetchall()


    # Close the database connection
    conn.close()

    return render_template('house_search_results.html', houses=houses)

# Route to search business properties based on price range and size
@app.route('/search_business_properties')
def search_business_properties():
    # Retrieve query parameters from the URL
    # Retrieve query parameters from the URL
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    min_size = request.args.get('min_size')
    max_size = request.args.get('max_size')

    # Create a database connection
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)


    query = """
            SELECT BusinessProperty.*, Property.price
            FROM BusinessProperty
            JOIN Property ON BusinessProperty.address = Property.address
            WHERE 1=1
        """

    params = {}

    # Add conditions for price range
    if min_price is not None and len(min_price) > 0:
        query += " AND Property.price >= %(min_price)s"
        params['min_price'] = min_price

    if max_price is not None and len(max_price) > 0:
        query += " AND Property.price <= %(max_price)s"
        params['max_price'] = max_price

    # Add conditions for bedrooms and bathrooms if provided in the query parameters
    if min_size is not None and len(min_size) > 0:
        query += " AND BusinessProperty.size >= %(min_size)s"
        params['min_size'] = min_size

    if max_size is not None and len(max_size) > 0:
        query += " AND BusinessProperty.size <= %(max_size)s"
        params['max_size'] = max_size


    cursor.execute(query, params)
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

