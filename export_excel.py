import sqlite3
import pandas as pd

def export_to_excel():

    conn = sqlite3.connect("applications.db")

    query = "SELECT * FROM applications ORDER BY date_applied DESC"

    df = pd.read_sql_query(query, conn)

    conn.close()

    file_name = "job_applications_export.xlsx"

    df.to_excel(file_name, index=False)

    print(f"Data exported successfully to {file_name}")


if __name__ == "__main__":
    export_to_excel()