import mysql.connector
from tabulate import tabulate

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',  # Update with your MySQL password
    database='bacchus_winery'
)

def run_report(query, report_title, headers):
    try:
        cursor = conn.cursor()

        # Execute the provided query
        cursor.execute(query)
        rows = cursor.fetchall()

        # Prepare the report data with placeholder for empty cells
        report_data = []
        for row in rows:
            processed_row = [value if value is not None else "0 %" for value in row]
            report_data.append(processed_row)

        # Display the report using tabulate
        print(f"\n{report_title}\n")
        if len(report_data) == 0:
            print("No data available.")
        else:
            print(tabulate(report_data, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center"))

    except mysql.connector.Error as e:
        print(f"Error accessing database: {e}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

TOTAL_QUANTITY_SOLD = "Total Quantity Sold"

def wine_distribution_analysis():
    query = """
        SELECT w.wine_name, SUM(ws.quantity_shipped) AS total_quantity_sold
        FROM WineShipments ws
        JOIN Wines w ON ws.wine_id = w.wine_id
        GROUP BY w.wine_name
    """
    headers = ["Wine", TOTAL_QUANTITY_SOLD]
    run_report(query, "Wine Distribution Analysis Report", headers)

def identify_unsold_wines():
    query = """
      SELECT
            w.wine_name,
            w.quantity_sold AS total_quantity_sold,
            COUNT(ws.wine_id) AS total_shipments,
            (w.quantity_sold - COALESCE(SUM(ws.quantity_shipped), 0)) AS unsold_quantity,
            ((w.quantity_sold - COALESCE(SUM(ws.quantity_shipped), 0)) / w.quantity_sold) * 100 AS unsold_percentage
        FROM
            Wines w
        LEFT JOIN
            WineShipments ws ON w.wine_id = ws.wine_id
        GROUP BY
            w.wine_name
        HAVING
            unsold_quantity > 0 OR unsold_quantity IS NULL
    """
    headers = ["Wine", "Total Sold", "Total Shipments", "Unsold Quantity", "Unsold Percentage"]
    run_report(query, "Unsold Wines Report", headers)

def distributor_wine_mapping():
    query = """
        SELECT d.distributor_name, w.wine_name, SUM(ws.quantity_shipped) AS total_quantity_sold,
               (SUM(ws.quantity_shipped) / (SELECT SUM(quantity_shipped) FROM WineShipments)) * 100 AS percentage_of_sales
        FROM Distributors d
        JOIN WineShipments ws ON d.distributor_id = ws.distributor_id
        JOIN Wines w ON ws.wine_id = w.wine_id
        GROUP BY d.distributor_name, w.wine_name
    """
    headers = ["Distributor", "Wine", "Total Quantity Sold", "Percentage of Sales"]
    run_report(query, "Distributor-Wine Mapping Report", headers)

def wines_not_selling_percentage():
    query = """
       SELECT
            w.wine_name,
            SUM(IFNULL(w.quantity_sold, 0)) - IFNULL(SUM(ws.quantity_shipped), 0) AS unsold_quantity,
            ((SUM(IFNULL(w.quantity_sold, 0)) - IFNULL(SUM(ws.quantity_shipped), 0)) / NULLIF(SUM(IFNULL(w.quantity_sold, 0)), 0)) * 100 AS unsold_percentage
        FROM
            Wines w
        LEFT JOIN
            WineShipments ws ON w.wine_id = ws.wine_id
        GROUP BY
            w.wine_name
        HAVING
            unsold_quantity > 0 OR unsold_quantity IS NULL
    """
    headers = ["Wine", "Unsold Quantity", "Unsold Percentage"]
    run_report(query, "Wines Not Selling with Percentage of Unsold", headers)

def wine_sales_by_distributor_percentage():
    query = """
        SELECT d.distributor_name,
               w.wine_name,
               SUM(ws.quantity_shipped) AS total_quantity_sold,
               (SUM(ws.quantity_shipped) / (SELECT SUM(quantity_shipped) FROM WineShipments)) * 100 AS percentage_of_sales
        FROM Distributors d
        JOIN WineShipments ws ON d.distributor_id = ws.distributor_id
        JOIN Wines w ON ws.wine_id = w.wine_id
        GROUP BY d.distributor_name, w.wine_name
    """
    headers = ["Distributor", "Wine", "Total Quantity Sold", "Percentage of Sales"]
    run_report(query, "Wine Sales by Distributor with Percentage", headers)

if __name__ == "__main__":
    try:
        # Run each report function
        wine_distribution_analysis()
        identify_unsold_wines()
        distributor_wine_mapping()
        wines_not_selling_percentage()
        wine_sales_by_distributor_percentage()
    except Exception as e:
        print(f"An error occurred: {e}")
