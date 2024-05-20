import mysql.connector
import datetime
from collections import defaultdict

config = {
    'user': 'root',  # Use your MySQL username
    'password': 'Sublime11!',  # Use your MySQL password
    'host': '127.0.0.1',  # Host where MySQL server is running
    'database': 'bacchus'  # Name of your MySQL database
}

now = datetime.datetime.now()

print("This report was generated on: ")
print(now.strftime("%Y-%m-%d %H:%M;S"))

try:
    # Connect to MySQL
    cnx = mysql.connector.connect(**config)

    # Check if connection is successful
    if cnx.is_connected():
        print("Connected to MySQL Database")
        cursor = cnx.cursor()

        query_1 = "SELECT supply_id, supply_name, supplier_id, supply_order_date, received_date, lead_time FROM supplies"
        cursor.execute(query_1)
        rows = cursor.fetchall()


        all_columns = ["Supply ID", "Supply Name", "Supplier ID", "Order Date", "Received Date", "Lead Time"]
        all_data = [str(col) for row in rows for col in row]

        column_widths = [max(len(str(col)) for col in col_data) for col_data in zip(*rows)]
        header = "|  ".join(f"{col:<{width}}" for col, width in zip(all_columns, column_widths))

        print("\nThis Report Shows all supply orders:")
        print(header)
        print("-" * len(header))


        for row in rows:
            row_formatted = "        |".join(
                "{:<{width}}".format(str(col), width=width) for col, width in zip(row, column_widths))
            print(row_formatted)

        query_2 = "SELECT supply_id, supply_name, supplier_id, supply_order_date, received_date, lead_time FROM supplies WHERE lead_time >= 30"
        cursor.execute(query_2)
        rows_2 = cursor.fetchall()

        column_widths = [max(len(str(col)) for col in col_data) for col_data in zip(*rows_2)]
        column_widths_combined = [max(width_1, width_2) for width_1, width_2 in zip(column_widths, column_widths)]
        header = "|   ".join(f"{col:<{width}}" for col, width in zip(all_columns, column_widths))

        print("\nThis Report Shows all orders requiring over 30 days from order to delivery date:")
        print(header)
        print("-" * len(header))

        for row in rows_2:
            row_formatted = "         |".join("{:<{width}}".format(str(col), width = width) for col, width in zip(row, column_widths))
            print(row_formatted)


        def get_date_input(prompt):
            while True:
                try:
                    date_str = input(prompt)
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    return date
                except ValueError:
                    print("I am sorry, that is an invalid date format. Please enter the date as 'YYYY-MM-DD' format.")


        start_date = get_date_input("Please enter the date to start the supply_inventory report (YYYY-MM-DD): ")
        end_date = get_date_input("Please enter the date to end the supply_inventory report on (YYYY-MM-DD): ")

        supply_id = input("Please enter the supply_id you are looking to find): ").strip()

        query_3 = ("SELECT supply_id, supply_order_date, received_date, on_hand_quantity FROM supply_inventory WHERE supply_order_date BETWEEN %s AND %s")
        query_3_params = [start_date, end_date]

        if supply_id:
            query_3 += " AND supply_id = %s"
            query_3_params.append(supply_id)

        cursor.execute(query_3, query_3_params)
        rows_3 = cursor.fetchall()

        print(
            "\nThis Report Shows supply orders per month and allowing to see current on hand quantities, with a current total at the bottom:")
        print("supply_id | supply_order_date | received_date | On Hand QTY")
        print("-----------------------------------------------------------")

        monthly_totals = defaultdict(int)
        for row in rows_3:
            supply_id, supply_order_date, received_date, on_hand_quantity = row
            monthly_totals[supply_id] += on_hand_quantity


        print("\nTotal on Hand QTY by supply_id:")
        for supply_id, data in monthly_totals.items():
            supply_order_date_str = " ," .join(str(date) for date in data['supply_order_date'])
            received_dates_str = " ," .join(str(date) for date in data['received_dates'])
            total_quantity_str = " ,".join(str(date) for date in data['total_qty'])
            print(f"Supply_id: {supply_id}, Order_date {supply_order_date}, Received_date {received_date} - Total QTY: {on_hand_quantity}")

except mysql.connector.Error as e:
    print("Error accessing database:", e)

finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'cnx' in locals() and cnx and cnx.is_connected():
        cnx.close()