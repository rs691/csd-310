import mysql.connector

# Database configuration
config = {
    'user': 'root',  # Use your MySQL username
    'password': 'Jayden#811',  # Use your MySQL password
    'host': '127.0.0.1',  # Host where MySQL server is running
    'database': 'winery'  # Name of your MySQL database
}

try:
    # Connect to MySQL
    cnx = mysql.connector.connect(**config)

    # Check if connection is successful
    if cnx.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()

        # Updated query to select and format hours worked from the Employees table
        query = """
        SELECT 
            CONCAT(employees.first_name, ' ', employees.last_name) AS employee_name, 
            ROUND(SUM(Work.hours_worked), 2) AS total_hours,
            ROUND(SUM(Work.hours_worked) / COUNT(DISTINCT Work.quarter), 2) AS average_hours_per_quarter
        FROM Work
        JOIN employees ON Work.employee_id = employees.employee_id
        JOIN (SELECT DISTINCT quarter FROM Work ORDER BY quarter DESC LIMIT 4) AS recent_quarters ON Work.quarter = recent_quarters.quarter
        GROUP BY employees.employee_id
        LIMIT 0, 400;
        """

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Print header for the output
        print("\n-- DISPLAYING EMPLOYEE WORK RECORDS IN THE LAST FOUR QUARTERS --\n")

        # Print column headers
        print("Employee Name\t\tTotal Hours\tAverage Hours Per Quarter")

        # Print each row of data
        for row in rows:
            print(f"{row[0]}\t\t{row[1]}\t\t{row[2]}")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if cnx.is_connected():
        cnx.close()
        print("Connection closed.")
        input("Press Enter to exit...")