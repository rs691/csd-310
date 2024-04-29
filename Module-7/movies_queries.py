# Robert Stewart     4/26/2024
# Module 7.2 Assignment

import mysql.connector

# Database configuration
config = {
    'user': 'root',           # Use your MySQL username
    'password': '',           # Use your MySQL password
    'host': '127.0.0.1',      # Host where MySQL server is running
    'database': 'csd-310'     # Name of your MySQL database
}

try:
    # Connect to MySQL
    cnx = mysql.connector.connect(**config)
    
    # Check if connection is successful
    if cnx.is_connected():
        # print("Connected to MySQL database")
        
        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()

        try:
           
            # First query to select all fields from the studio table
            studio_query = "SELECT * FROM studio"

            # Execute the query to retrieve all rows from the studio table
            cursor.execute(studio_query)

            # Fetch all rows from the result set
            studio_rows = cursor.fetchall()

            print()
            # Print header for the studio table
            print("-- DISPLAYING Studio RECORDS --")
            # for loop to iterate through the rows
            for row in studio_rows:
                print("Studio ID: ", row[0])
                print("Studio Name: ", row[1])
            # Add a blank line for separation
                print()
                
                 

            # Query to select all fields from the genre table
            genre_query = "SELECT * FROM genre"

            # Execute the query to retrieve all rows from the genre table
            cursor.execute(genre_query)

            # Fetch all rows from the result set
            genre_rows = cursor.fetchall()
            # For readability, add a blank line
            print()
            # Print header for the genre table
            print("-- DISPLAYING Genre RECORDS --")
            # for loop to iterate through the rows
            for row in genre_rows:
                print("Genre ID: ", row[0])
                print("Genre Name: ", row[1])
            # Add a blank line for separation
                print()
            
            # Query to select the movie names for those movies that have a run time of less than two hours
            short_films_query = "SELECT f.film_name, f.film_runtime FROM film f WHERE f.film_runtime < 120"
            
             # Execute the query
            cursor.execute(short_films_query)
            
            # Fetch all rows from the result set
            short_films_rows = cursor.fetchall()
            
            # print header for the short films
            print("-- DISPLAYING Short Film RECORDS--")
            # loop through the rows and print the film names that are < 120 minutes
            for row in short_films_rows:
               
                print("Film Name: ", row[0])
                print("Runtime: ", row[1])
            # Add a blank line for separation
                print()
                
            # query film table to get a list of film names, and directors grouped by director name
            director_query = "select film_name, film_director FROM film order by film_director"
            
            # execute the query
            cursor.execute(director_query)
            
            # fetch all rows from the result set
            director_rows = cursor.fetchall()
            
            # print header for the director table
            print("-- DISPLAYING Director RECORDS in Order --")
            # loop through the rows and print the film names and directors
            for row in director_rows:
                print("Film Name: ", row[0])
                print("Director: ", row[1])
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
