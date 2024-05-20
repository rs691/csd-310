
import mysql.connector

config = {
    'user': 'root',  # Use your MySQL username
    'password': 'Sublime11!',  # Use your MySQL password
    'host': '127.0.0.1',  # Host where MySQL server is running
    'database': 'bacchus'  # Name of your MySQL database
}

try:
    # Connect to MySQL
    cnx = mysql.connector.connect(**config)

    # Check if connection is successful
    if cnx.is_connected():
        print("Connected to MySQL Database")
        cursor = cnx.cursor()

        query = "SELECT supply_id, supply_name, supplier_id, supply_order_date, received_date, lead_time FROM supplies"
        cursor.execute(query)
        rows = cursor.fetchall()

        all_columns = ["Supply ID", "Supply Name", "Supplier ID", "Order Date", "Received Date", "Lead Time"]
        all_data = [str(col) for row in rows for col in row]
        all_columns_and_data = all_columns + all_data

        column_widths = [max(len(str(col)) for col in column) for column in zip(all_columns_and_data)]

        header = "  ".join(f"{col:<{width}}" for col, width in zip(all_columns, column_widths))
        print(header)
        print("-" * len(header))

        for row in rows:
            row_formatted = "  ".join("{:<{width}}".format(str(col), width=width) for col, width in zip(row, column_widths))
            print(row_formatted)


        query_2 = "SELECT supply_id, supply_name, supplier_id, supply_order_date, received_date, lead_time FROM supplies WHERE lead_time >= '18'"
        cursor.execute(query_2)
        rows_2 = cursor.fetchall()

        print("\nThis Report Shows all orders requiring over 18 days from order to delivery date:")
        print(header)
        print("-" * len(header))

        for row in rows_2:
            row_formatted = " | ".join("{:<{width}}".format(str(col), width=width) for col, width in zip(row, column_widths))
            print(row_formatted)

except mysql.connector.Error as e:
    print("Error accessing database:", e)

finally:

    if 'cursor' in locals():
        cursor.close()
    if 'cnx' in locals() and cnx.is_connected():
        cnx.close()