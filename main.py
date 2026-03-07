from config.db import get_connection, close_connection

def main():
    print("🏥 Hospital Management System")
    print("=" * 40)
    
    # Test the connection
    connection = get_connection()
    
    if connection:
        close_connection(connection)

if __name__ == "__main__":
    main()