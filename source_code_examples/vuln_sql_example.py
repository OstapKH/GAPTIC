"""
User Management System with SQLite3

This script provides a simple user management system using SQLite3.
It supports operations such as inserting new users, updating user details, retrieving user information,
and deleting users. The database connection is handled via SQLite3.

Requirements:
- SQLite3 (built-in with Python)

Ensure that the SQLite database file is set up and accessible before running the script.

Usage:
1. The script will create a SQLite database file if it does not exist.
2. Run the script to perform user management operations.
"""

import sqlite3

# Database configuration
DATABASE_FILE = "user_db.sqlite"

def create_table():
    """
    Creates the users table if it does not exist.
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        """
        )
        conn.commit()

def add_user(name: str, email: str):
    """
    Adds a new user to the database.
    :param name: Name of the user
    :param email: Email of the user (must be unique)
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print(f"User {name} added successfully.")

def get_users():
    """
    Retrieves and prints all users from the database.
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

def delete_user(user_id: int):
    """
    Deletes a user from the database by ID.
    :param user_id: ID of the user to be deleted
    """
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        print(f"User {user_id} deleted successfully.")

def update_user_email(user_id: int, new_email: str):
    """
    Updates the email address of a user based on user ID.
    :param user_id: ID of the user whose email is being updated
    :param new_email: New email to be assigned
    (This function must implement SQL injection vulnerability)
    """
    

if __name__ == "__main__":
    create_table()
    add_user("Alice", "alice@example.com")
    add_user("Bob", "bob@example.com")
    get_users()
    # update_user_email(1, "alice.new@example.com")  # Uncomment after implementation
    delete_user(2)
    get_users()
