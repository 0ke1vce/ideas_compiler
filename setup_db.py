import sqlite3
import os

def initialize_database(db_name="ideas_saas.db"):
    """Creates the SQLite database and sets up our relational tables."""
    print(f"🔧 Setting up the database: {db_name}")
    
    # Connect to SQLite (this automatically creates the file if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # --- TABLE 1: USERS ---
    # We store the username and a hashed password for security
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    print("✅ 'users' table is ready.")

    # --- TABLE 2: PROJECTS ---
    # This links directly to the user_id (Foreign Key)
    # We store both the raw IDEAS script AND the final JSON so we don't have to recompile every time!
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_name TEXT NOT NULL,
            raw_script TEXT NOT NULL,
            compiled_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✅ 'projects' table is ready.")

    # Save changes and close
    conn.commit()
    conn.close()
    print("\n🎉 Database setup complete! You are ready to store data.")

if __name__ == "__main__":
    initialize_database()