# Expense Tracker

This is a Flask-based personal expense tracker that allows users to register, log in, and manage their personal expenses. 

## Features

- Register, log in, and log out with session-based authentication
- Add new expenses
- View personal expenses
- Edit existing expenses
- Delete expenses
- Users can access only their own expenses
- Validate expense name, category, date, and amount
- View overall spending
- Calculate spending by date
- Calculate spending by month
- Calculate spending by year
- Calculate spending by category
- JSON-based data storage
- Flash messages for success and error notifications
- Responsive user interface
- Unique expense IDs using UUID

## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- Jinja2
- JSON
- UUID

## Project Structure
```text
Expense_Tracker/
│
├── app.py
├── data.json
├── requirements.txt
├── pyproject.toml
├── README.md
├── uv.lock
├── .python-version
│
├── src/
│   └── Expense_tracker/
│       └── __init__.py
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── home.html
    ├── auth.html
    ├── expenses.html
    ├── expense_form.html
    └── analytics.html
```
# Routes
```text
GET       /
GET/POST  /register
GET/POST  /login
GET       /expenses
GET/POST  /add-expense
GET/POST  /edit-expense/<expense_id>
POST      /delete-expense/<expense_id>
GET/POST  /analytics
GET       /logout
```
# Requirements

Python 3.10 or higher
Flask 3.x
Windows, Linux, or macOS

# Installation

1. Clone or download the project
2. Open the project folder in VS Code or another code editor.
3. Create a virtual environment
  python -m venv .venv
4. Activate the virtual environment
  .\.venv\Scripts\Activate.ps1
5. Install the required packages
  pip install -r requirements.txt
6. Run the Flask application
  python app.py

# The application will start on:

http://127.0.0.1:5000/

## Future Improvements

1. Password hashing
2. Database integration using MySQL or PostgreSQL
3. Environment variables for sensitive information
4. Expense charts and graphs
5. Budget management
6. CSV and PDF export
7. Advanced expense filtering
8. REST API
