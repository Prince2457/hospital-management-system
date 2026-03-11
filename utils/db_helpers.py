from config.db import get_connection, close_connection

def execute_query(query, params=None, fetch='all', commit=False):
    connection = get_connection()
    if not connection:
        return None
    
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute(query, params or ())

        if commit:
            connection.commit()
            return cursor.rowcount
        
        if fetch == "all":
            return cursor.fetchall()
        if fetch =="one":
            return cursor.fetchone()
        
    except Exception as e:
        print(f"Database error: {e}")
        if commit:
            connection.rollback()
        return None
    finally:
        close_connection(connection, cursor)
