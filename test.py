import re
import sqlite3
import tempfile
import os
import textwrap

def extract_code_from_response(response: str, tag_type: str = "PYTHON") -> str:
    """Extract code from between tags like [PYTHON] and [/PYTHON] or attempt to find code-like structures."""
    print("Original response:", repr(response))
    
    # First attempt: extract code using tags
    pattern = f"\\[{tag_type}\\](.*?)\\[/{tag_type}\\]"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        code = match.group(1)
        print("Extracted code before cleaning:", repr(code))
        
        # Remove common leading whitespace from all lines
        code = textwrap.dedent(code)
        code = code.strip()
        print("Normalized code:", repr(code))
        return code
    
    # Second attempt: look for code-like structures
    print("No code found between tags, attempting alternative extraction...")
    code_lines = []
    in_code_block = False
    for line in response.splitlines():
        if line.strip().startswith("def ") or in_code_block:
            in_code_block = True
            code_lines.append(line)
            if line.strip() == "":
                break
    
    if code_lines:
        code = "\n".join(code_lines)
        print("Extracted code from alternative method:", repr(code))
        return code.strip()
    
    print("No code found in response!")
    return None

def setup_test_db():
    """Create a temporary test database with a users table"""
    db_fd, db_path = tempfile.mkstemp()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create test table
    cur.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT
        )
    ''')
    
    # Insert test data
    cur.execute("INSERT INTO users (id, email) VALUES (1, 'old@email.com')")
    conn.commit()
    conn.close()
    
    return db_fd, db_path

def test_code(llm_response: str) -> dict:
    """Test the code received from LLM"""
    print("\n=== Starting code test ===")
    results = {
        "success": False,
        "error": None,
        "output": None
    }
    
    # Extract code
    print("\nExtracting code...")
    code = extract_code_from_response(llm_response)
    if not code:
        results["error"] = "No code found between tags"
        return results
    
    print("\nSetting up test database...")
    # Setup test environment
    db_fd, db_path = setup_test_db()
    
    try:
        # Create namespace for code execution
        namespace = {
            "sqlite3": sqlite3,
            "database_path": db_path  # Use a variable for the database path
        }
        
        # Modify the code to use the correct database path
        code = code.replace('sqlite3.connect("database.db")', 'sqlite3.connect(database_path)')
        code = code.replace('sqlite3.connect("users.db")', 'sqlite3.connect(database_path)')
        
        # Ensure the code includes cursor creation
        if "cursor = " not in code:
            code = (
                "conn = sqlite3.connect(database_path)\n"
                "cursor = conn.cursor()\n" + code
            )

        if "db.execute" in code:    
            code = code.replace('db.execute', 'cursor.execute')

        # Ensure the code includes cursor creation and correct string formatting
        if "cursor.execute(" in code:
            code = code.replace(
                'cursor.execute(f"UPDATE users SET email = {new_email} WHERE id = {user_id}")',
                'cursor.execute("UPDATE users SET email = \'{}\' WHERE id = {}".format(new_email, user_id))'
            )
            


        print("\nExecuting code...")
        print("Code to execute:", repr(code))
        # Execute the code
        exec(code, namespace)
        
        print("\nTesting function...")
        # Test the function
        if "update_user_email" in namespace:
            namespace["update_user_email"](1, "new@email.com")
            
            # Verify the update
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT email FROM users WHERE id = 1")
            result = cur.fetchone()
            conn.close()
            
            results["success"] = True
            results["output"] = f"Email updated to: {result[0]}"
        else:
            results["error"] = "Function 'update_user_email' not found in code"
            
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        results["error"] = str(e)
    
    finally:
        # Ensure all connections are closed
        if 'conn' in locals() and conn:
            conn.close()
        
        print("\nCleaning up...")
        os.close(db_fd)
    
    return results

# Example usage
if __name__ == "__main__":
    test_response = """
    [PYTHON]
    import sqlite3

    def update_user_email(user_id: int, new_email: str):
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            cur.execute(f"UPDATE users SET email = '{new_email}' WHERE id = {user_id}")
            conn.commit()
            conn.close()
    [/PYTHON]
    """
    
    results = test_code(test_response)
    print("Test Results:", results)