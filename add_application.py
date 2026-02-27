import sqlite3
from datetime import datetime

def add_application():
    # Connect to the correct database file
    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()

    print("\n--- Add New Job Application ---\n")

    # Take user inputs
    company = input("Enter Company Name: ")
    role = input("Enter Role: ")
    location = input("Enter Location: ")
    link = input("Application Link: ")
    source = input("Source (LinkedIn / Referral / Website): ")
    notes = input("Notes (optional): ")

    # Auto-generate date and default status
    date_applied = datetime.today().strftime("%Y-%m-%d")
    status = "Applied"

    # Insert data into applications table
    cursor.execute("""
    INSERT INTO applications
    (company, role, location, link, source, status, notes, date_applied)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, role, location, link, source, status, notes, date_applied))

    # Save and close
    conn.commit()
    conn.close()

    print("\n✅ Application Saved Successfully!\n")


# Run function only when file is executed directly
if __name__ == '__main__':
    add_application()