# Job Application Tracker

A personal job application management system built with Python, SQLite, and Streamlit.

## Features

- Log job applications quickly using CLI
- Interactive dashboard for tracking applications
- Filter by company and status
- Update application status
- Delete applications
- Analytics for application pipeline
- Weekly application trends
- Follow-up detection
- Excel export

## Tech Stack

Python  
Streamlit  
SQLite  
Pandas  
Matplotlib  

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run dashboard.py

## Project Structure

dashboard.py → Streamlit dashboard  
add_application.py → CLI tool to add applications  
database.py → Database setup  
export_excel.py → Excel export utility

## Purpose

This project helps track and analyze job applications with a simple personal dashboard.