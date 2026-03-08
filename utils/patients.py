from config.db import get_connection
from config.db import close_connection

def get_all_patients():
    connection = get_connection()
    
    if not connection :
        return []
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchmany()
        return patients
    
    except Exception as e:
        print(f"❌ Error fetching patients: {e}")
        return []
    finally:
        close_connection(connection, cursor)   
