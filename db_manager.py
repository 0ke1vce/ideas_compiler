import sqlite3
import hashlib
import json

DB_NAME = "ideas_saas.db"

def hash_password(password):
    """Creates a secure hash of the password so it isn't stored as plain text."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Registers a new user in the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True, "User created successfully!"
    except sqlite3.IntegrityError:
        # The database throws an IntegrityError because we set 'username UNIQUE' in Step 1
        return False, "Username already exists. Please choose another."
    finally:
        conn.close()

def verify_user(username, password):
    """Checks if the username and password match. Returns (Success, User_ID)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return True, user[0]  # user[0] is their unique ID number
    return False, None

def save_project(user_id, project_name, raw_script, compiled_json_file):
    """Saves a project timeline for a specific user."""
    # First, read the JSON data from the file our compiler generated
    with open(compiled_json_file, 'r') as f:
        json_data = f.read()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if a project with this name already exists for this user
    cursor.execute("SELECT id FROM projects WHERE user_id = ? AND project_name = ?", (user_id, project_name))
    existing_project = cursor.fetchone()

    if existing_project:
        # Update the existing project
        cursor.execute('''
            UPDATE projects 
            SET raw_script = ?, compiled_json = ? 
            WHERE id = ?
        ''', (raw_script, json_data, existing_project[0]))
    else:
        # Create a brand new project record
        cursor.execute('''
            INSERT INTO projects (user_id, project_name, raw_script, compiled_json)
            VALUES (?, ?, ?, ?)
        ''', (user_id, project_name, raw_script, json_data))
    
    conn.commit()
    conn.close()
    return True

def get_user_projects(user_id):
    """Retrieves all saved projects for a specific user to display in the UI."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT project_name, raw_script, compiled_json, created_at FROM projects WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    projects = cursor.fetchall()
    conn.close()
    
    # Format the SQL data into a clean Python list of dictionaries
    project_list = []
    for p in projects:
        project_list.append({
            "name": p[0],
            "script": p[1],
            "json_data": p[2],  # We store the raw JSON string
            "date": p[3]
        })
    return project_list