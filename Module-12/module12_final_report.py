# Robert Stewart 5/19/2024
# This is the final version of the python report generator. 

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
    """
    Executes a provided SQL query and displays the results in a formatted table.
    
    Args:
        query (str): The SQL query to execute.
        report_title (str): The title of the report.
        headers (list): The headers for the table columns.
    """
    try:
        cursor = conn.cursor()

        # Execute the provided query
        cursor.execute(query)
        rows = cursor.fetchall()

        # Prepare the report data with formatted numbers
        report_data = []
        for row in rows:
            processed_row = [
                f"{value:.2f}%" if isinstance(value, float) and "%" in headers[i] else f"{value:.2f}" if isinstance(value, float) else value
                for i, value in enumerate(row)
            ]
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

def wine_distribution_analysis():
    """
    Generates a report on the total quantity of each wine sold.
    Groups the results by wine name.
    """
    query = """
        SELECT w.wine_name, SUM(ws.quantity_shipped) AS total_quantity_sold
        FROM WineShipments ws
        JOIN Wines w ON ws.wine_id = w.wine_id
        GROUP BY w.wine_name
    """
    headers = ["Wine", "Total Quantity Sold"]
    run_report(query, "Wine Distribution Analysis Report", headers)

def unsold_wines_report():
    """
    Generates a report on unsold wines, including total sold, total shipments,
    unsold quantity, and unsold percentage.
    Groups the results by wine name and filters for wines with unsold quantities.
    """
    query = """
        SELECT
            w.wine_name,
            w.quantity_sold AS total_quantity_sold,
            COUNT(ws.wine_id) AS total_shipments,
            (w.quantity_sold - COALESCE(SUM(ws.quantity_shipped), 0)) AS unsold_quantity,
            ROUND(((w.quantity_sold - COALESCE(SUM(ws.quantity_shipped), 0))
            / w.quantity_sold) * 100, 2) AS unsold_percentage
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
    run_report(query, "Inventory Control Analysis", headers)

def distributor_wine_mapping():
    """
    Maps distributors to the wines they sell and calculates the percentage of
    total sales for each wine.
    Groups the results by distributor name and wine name.
    """
    query = """
        SELECT d.distributor_name, w.wine_name, SUM(ws.quantity_shipped) AS total_quantity_sold,
               CONCAT(FORMAT((SUM(ws.quantity_shipped) / (SELECT SUM(quantity_shipped) FROM WineShipments)) * 100, 2), ' %') AS percentage_of_sales
        FROM Distributors d
        JOIN WineShipments ws ON d.distributor_id = ws.distributor_id
        JOIN Wines w ON ws.wine_id = w.wine_id
        GROUP BY d.distributor_name, w.wine_name
    """
    headers = ["Distributor", "Wine", "Total Quantity Sold", "Percentage of Sales"]
    run_report(query, "Distributor-Wine Mapping Report", headers)

def wine_sales_by_distributor_percentage():
    """
    Similar to distributor_wine_mapping, this function calculates the percentage
    of total sales for each wine by distributor.
    Groups the results by distributor name and wine name.
    """
    query = """
        SELECT d.distributor_name,
               w.wine_name,
               SUM(ws.quantity_shipped) AS total_quantity_sold,
               CONCAT(FORMAT((SUM(ws.quantity_shipped) / (SELECT SUM(quantity_shipped) 
               FROM WineShipments)) * 100, 2), ' %') AS percentage_of_sales
        FROM Distributors d
        JOIN WineShipments ws ON d.distributor_id = ws.distributor_id
        JOIN Wines w ON ws.wine_id = w.wine_id
        GROUP BY d.distributor_name, w.wine_name
    """
    headers = ["Distributor", "Wine", "Total Quantity Sold", "Percentage of Sales"]
    run_report(query, "Wine Sales by Distributor with Percentage", headers)

def inventory_turnover_rate():
    """
    Calculates the inventory turnover rate, showing the total quantity sold,
    total shipments, unsold quantity, and unsold percentage for each wine.
    Groups the results by wine name.
    """
    query = """
      SELECT
            w.wine_name,
            w.quantity_sold AS total_quantity_sold,
            COUNT(ws.wine_id) AS total_shipments,
            (w.quantity_sold - COALESCE(SUM(ws.quantity_shipped), 0)) AS unsold_quantity,
            CONCAT(FORMAT(((w.quantity_sold - COALESCE(SUM(ws.quantity_shipped), 0))
            / w.quantity_sold) * 100, 2), ' %') AS unsold_percentage
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

def sales_trends_over_time():
    """
    Analyzes sales trends over time, showing the total quantity sold for each wine by month.
    Groups the results by wine name and month.
    """
    query = """
        SELECT 
            w.wine_name, 
            DATE_FORMAT(ws.shipment_date, '%Y-%m') AS month, 
            SUM(ws.quantity_shipped) AS total_quantity_sold
        FROM 
            Wines w
        JOIN 
            WineShipments ws ON w.wine_id = ws.wine_id
        GROUP BY 
            w.wine_name, month
        ORDER BY 
            w.wine_name, month;
    """
    headers = ["Wine", "Month", "Total Quantity Sold"]
    run_report(query, "Sales Trends Over Time Report", headers)

def average_order_size_by_distributor():
    """
    Calculates the average order size by distributor.
    Groups the results by distributor name.
    """
    query = """
        SELECT 
            d.distributor_name, 
            FORMAT(AVG(ws.quantity_shipped), 2) AS average_order_size
        FROM 
            Distributors d
        JOIN 
            WineShipments ws ON d.distributor_id = ws.distributor_id
        GROUP BY 
            d.distributor_name;
    """
    headers = ["Distributor", "Average Order Size"]
    run_report(query, "Average Order Size by Distributor Report", headers)

def sales_revenue_by_wine():
    """
    Calculates the annual sales revenue by wine.
    Groups the results by wine name.
    """
    query = """
        SELECT 
            w.wine_name, 
           CONCAT('$', FORMAT(SUM(ws.quantity_shipped * w.price_per_unit * 12), 2)) AS annual_total_sales_revenue
        FROM 
            Wines w
        JOIN 
            WineShipments ws ON w.wine_id = ws.wine_id
        GROUP BY 
            w.wine_name;
    """
    headers = ["Wine", "Annual Net Revenue"]
    run_report(query, "Sales Revenue by Wine Report", headers)

if __name__ == "__main__":
    try:
        # Run each report function
        wine_distribution_analysis()
        unsold_wines_report()
        distributor_wine_mapping()
        wine_sales_by_distributor_percentage()
        # Added functions
        inventory_turnover_rate()
        sales_trends_over_time()
        average_order_size_by_distributor()
        sales_revenue_by_wine()
    except Exception as e:
        print(f"An error occurred: {e}")
