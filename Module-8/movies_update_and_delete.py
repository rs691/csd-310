# Robert Stewart     4/26/2024
# Module 8.2 Assignment
# This program demonstrates how to update and delete records in a MySQL database using Python.

import mysql.connector

# Database configuration
config = {
    'user': 'rob',           # Use your MySQL username
    'password': 'Hankbob2017!',           # Use your MySQL password
    'host': 'learning-projects.mysql.database.azure.com',      # Host where MySQL server is running
    'database': 'movies'     # Name of your MySQL database
}


# Function to display film information
def show_films(cursor, title):
    try:
        # Define SELECT query to display film information
        show_films_query = "SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS Studio FROM film \
            JOIN genre ON film.genre_id = genre.genre_id \
            JOIN studio ON film.studio_id = studio.studio_id \
        "

        # Execute the query
        cursor.execute(show_films_query)

        # Fetch all rows from the result set
        film_data = cursor.fetchall()

        # Print header for the film table
        print(f"-- {title} --")
        for row in film_data:
            print("Film Name:", row['Name'])
            print("Director:", row['Director'])
            print("Genre Name ID:", row['Genre'])
            print("Studio Name:", row['Studio'])
            print()

    except mysql.connector.Error as error:
        print("Error fetching film information:", error)
        

def insert_new_film(cursor):
    try:
        # Define INSERT query to add a new film record
        insert_query = "INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id ) \
            VALUES ('The Moment', 1977, 100, 'Robert Stewart', 1, 1)"

        # Execute the query
        cursor.execute(insert_query)
        
    except mysql.connector.Error as error:
        print("Error inserting new film record:", error)

def update_film_genre(cursor):
    try:
        # Define UPDATE query to change genre of a film
        update_query = "UPDATE film SET genre_id = 2 WHERE film_name = 'Alien'"

        # Execute the query
        cursor.execute(update_query)

    except mysql.connector.Error as error:
        print("Error updating film genre:", error)

def delete_film(cursor):
    try:
        # Define DELETE query to remove a film record
        delete_query = "DELETE FROM film \
            WHERE film_name = 'Gladiator'"

        # Execute the query
        cursor.execute(delete_query)

    except mysql.connector.Error as error:
        print("Error deleting film record:", error)

def main():
    try:
        # Connect to MySQL
        cnx = mysql.connector.connect(**config)
    
        # Check if connection is successful
        if cnx.is_connected():
            print("Connected to MySQL database")
            print()

            # Create a cursor object to execute SQL queries
            cursor = cnx.cursor(dictionary=True)

            try:
                # Display films before modifications
                show_films(cursor, " DISPLAYING FILMS ")

                # Insert a new film record
                insert_new_film(cursor)

                # Display films after insertion
                show_films(cursor, " DISPLAYING FILMS AFTER INSERTION ")

                # Update the genre of the film "Alien" to Horror
                update_film_genre(cursor)

                # Display films after updating genre
                show_films(cursor, " DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror ")

                # Delete the film record for "Gladiator"
                delete_film(cursor)

                # Display films after deletion
                show_films(cursor, " DISPLAYING FILMS AFTER DELETE ")

                # Commit changes and close cursor
                cnx.commit()

            except Exception as e:
                print("An error occurred:", e)

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
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()
