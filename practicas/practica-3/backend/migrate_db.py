"""
Migration script to add copilot_profile and model columns to existing database.
Run this script once to update your existing chatbot.db
"""
import sqlite3
import os

DB_PATH = "./chatbot.db"

def migrate_database():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} does not exist. No migration needed.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(conversations)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add copilot_profile column if it doesn't exist
        if 'copilot_profile' not in columns:
            print("Adding copilot_profile column...")
            cursor.execute("""
                ALTER TABLE conversations
                ADD COLUMN copilot_profile VARCHAR(50) DEFAULT 'generico'
            """)
            print("✓ copilot_profile column added")
        else:
            print("✓ copilot_profile column already exists")

        # Add model column if it doesn't exist
        if 'model' not in columns:
            print("Adding model column...")
            cursor.execute("""
                ALTER TABLE conversations
                ADD COLUMN model VARCHAR(100) DEFAULT 'llama3.2:3b'
            """)
            print("✓ model column added")
        else:
            print("✓ model column already exists")

        conn.commit()
        print("\n✅ Migration completed successfully!")

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting database migration...")
    print(f"Database path: {DB_PATH}\n")
    migrate_database()
