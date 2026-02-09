import sys
from unittest.mock import MagicMock

# Mock psycopg2 before importing database.py to check for syntax/structure
mock_psycopg2 = MagicMock()
sys.modules['psycopg2'] = mock_psycopg2
sys.modules['psycopg2.extras'] = MagicMock()

try:
    import database
    import config
    print("✅ SUCCESS: database.py imported correctly with PostgreSQL logic.")
    
    # Check if key functions exist
    required_funcs = ['get_connection', 'init_db', 'add_user', 'get_user', 'set_favorite']
    missing = [f for f in required_funcs if not hasattr(database, f)]
    
    if not missing:
        print(f"✅ SUCCESS: All required database functions are present.")
    else:
        print(f"❌ FAILED: Missing functions: {missing}")

except Exception as e:
    print(f"❌ FAILED: Error importing or verifying database.py: {e}")
