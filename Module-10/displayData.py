
import mysql.connector

# Database configuration
config = {
    'user': 'root',           # Use your MySQL username
    'password': '',           # Use your MySQL password
    'host': '127.0.0.1',      # Host where MySQL server is running
    'database': 'bacchus_winery'     # Name of your MySQL database
}

# Link to the MySQL documentation and explanation used for the connection
# MySQL :: MySQL Connector/Python Developer Guide :: 5.1 Connecting to MySQL using Connector/Python. (n.d.). 
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

try:
    # Connect to MySQL
    cnx = mysql.connector.connect(**config)
    
    # Check if connection is successful
    if cnx.is_connected():
        # print("Connected to MySQL database")
        
        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()

        try:
           
            # First query to select all fields from the roles table
            roles_query = "SELECT * FROM roles"

            # Execute the query to retrieve all rows from the roles table
            cursor.execute(roles_query)

            # Fetch all rows from the result set
            roles_rows = cursor.fetchall()

            print()
            # Print header for the roles table
            print("-- DISPLAYING ROLES RECORDS --")
            # for loop to iterate through the rows
            for row in roles_rows:
                print("Role ID: ", row[0])
                print("Role Name: ", row[1])
            # Add a blank line for separation
                print()
                
                 

            # Query to select all fields from the Employees table
            employees_query = "SELECT * FROM Employees"

            # Execute the query to retrieve all rows from the Employees table
            cursor.execute(employees_query)

            # Fetch all rows from the result set
            employees_rows = cursor.fetchall()
            # For readability, add a blank line
            print()
            # Print header for the Employees table
            print("-- DISPLAYING EMPLOYEE RECORDS --")
            # for loop to iterate through the rows
            for row in employees_rows:
                print("Employee ID: ", row[0])
                print("First Name: ", row[1])
                print("Last Name: ", row[2])
                print("Role ID: ", row[3])
                print("Hours Worked: ", row[4])
            # Add a blank line for separation
                print()
            
            # Query to select the supplier names from the suppliers table
            suppliers_query = "SELECT * FROM Suppliers"
            
             # Execute the query
            cursor.execute(suppliers_query)
            
            # Fetch all rows from the result set
            suppliers_rows = cursor.fetchall()
            
            # print header for the Suppliers table
            print("-- DISPLAYING SUPPLIERS RECORDS--")
            # loop through the rows and print the supplier attributes
            for row in suppliers_rows:
                print("Supplier ID: ", row[0])
                print("Supplier Name: ", row[1])
                print("Contact Person: ", row[2])
                print("Contact Email: ", row[3])
            # Add a blank line for separation
                print()
                
            # query Supplies table
            supplies_query = "select * from Supplies"
            
            # execute the query
            cursor.execute(supplies_query)
            
            # fetch all rows from the result set
            supplies_rows = cursor.fetchall()
            
            # print header for the Supplies table
            print("-- DISPLAYING SUPPLIES DATA --")
            # loop through the rows and print each supply
            for row in supplies_rows:
                print("Supply ID: ", row[0])
                print("Supply Name: ", row[1])
                print("Supplier ID: ", row[2])
                print("Quantity: ", row[3])
                print("Price Per Unit: ", row[4])
                print("Date Received: ", row[5])
                
            # Add a blank line for separation
                print()
                
            # query the Distributors table
            distributors_query = "select * from Distributors"
            
            # execute the query
            cursor.execute(distributors_query)
            
            # fetch all rows from the result set
            distributors_rows = cursor.fetchall()
            
            # print header for the Distributors table
            print("-- DISPLAYING DISTRIBUTORS DATA --")
            
            # loop through the rows and print each distributor attribute
            for row in distributors_rows:
                print("Distributor ID: ", row[0])
                print("Distributor Name: ", row[1])
                print("Distributor Street Number: ", row[2])
                print("Distributor Street Name: ", row[3])
                print("Distributor City: ", row[4])
                print("Distributor State: ", row[5])
                print("Distributor Zip Code: ", row[6])
                print("Contact Phone Number: ", row[7])
                print("Contact Name: ", row[8])
                print("Phone Email: ", row[9])
                # Add a blank line for separation
                print()
            
            # query the WineShipments table
            wine_shipments_query = "select * from WineShipments"
            
            # execute the query
            cursor.execute(wine_shipments_query)
            
            # fetch all rows from the result set
            wine_shipments_rows = cursor.fetchall()
            
            # print header for the WineShipments table
            print("-- DISPLAYING WineShipments DATA --")
            
            # loop through the rows and print each wine shipment attribute
            for row in wine_shipments_rows:
                print("Shipment ID: ", row[0])
                print("Distributor ID: ", row[1])
                print("Wine ID Number: ", row[2])
                print("Quantity Shipped: ", row[3])
                print("Date Shipped: ", row[4])
                # Add a blank line for separation
                print()
            
        except mysql.connector.Error as error:
            print("Error retrieving data:", error)

        finally:
            # Close the cursor
            cursor.close()

    else:
        print("Failed to connect to MySQL database")

except mysql.connector.Error as error:
    print("Error connecting to MySQL database:", error)

finally:
    # Close the connection
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()
        # print("MySQL connection is closed")
