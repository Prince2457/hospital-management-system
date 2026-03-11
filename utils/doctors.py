from config.db import get_connection, close_connection

def get_all_doctors():
    connection = get_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True ,buffered=True)
    try:
        cursor.execute("SELECT * FROM doctors")
        doctors = cursor.fetchall()
        print("Doctors Fetched successfully")
        return doctors
    
    except Exception as e:
        print(f"Failed to fetch doctors{e}")
        return []
    
    finally:
        close_connection(connection, cursor)

def get_doctor_by_id(doctors_id):
    connection = get_connection()
    if not connection:
        return None
    
    cursor = connection.cursor(dictionary=True, buffered=True)

    try:
        cursor.execute("SELECT * FROM doctors WHRERE doctor_id =%s",(doctors_id,))
        doctor = cursor.fetchone()
        print("Doctor fetched successfully")
        return doctor
    
    except Exception as e:
        print(f"Failed to fetch doctor{e}")
        return None
    
    finally:
        close_connection(connection, cursor)

def create_doctor(user_id, specialization, qualification, license_number, department, available_days, consultation_fee):
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()

    try:
        cursor.execute(
            """INSERT INTO doctors 
                (user_id, specialization, qualification, license_number, department, available_days, consultation_fee) 
                VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                    (user_id, specialization, qualification, license_number, department, available_days, consultation_fee ))
        connection.commit()
        print("Doctor created successfully")
        return True
    
    except Exception as e:
        print(f"Failed to create doctor{e}")
        connection.rollback()
        return False
    
    finally:
        close_connection(connection, cursor)

def update_doctor(doctor_id, user_id, specialization, qualification, license_number, department, available_days, consultation_fee):
    connection = get_connection()
    if not connection:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute(
            """UPDATE doctors SET
            user_id =%s,
            specialization=%s,
            qualification=%s,
            license_number=%s,
            department=%s,
            available_days=%s,
            consultation_fee=%s
            WHERE doctor_id =%s
        """,
        (user_id, specialization, qualification, license_number, department, available_days, consultation_fee, doctor_id))

        connection.commit()
        print("Doctor updated successfully")
        return True
    
    except Exception as e:
        print(f"Failed to update doctor details{e}")
        connection.rollback()
        return False
    
    finally:
        close_connection(connection, cursor)

def delete_doctor(doctor_id):
    connection = get_connection()
    if not connection:
        return False
    
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM doctors WHERE doctor_id =%s",(doctor_id,))

        connection.commit()
        if cursor.rowcount == 0:
            print(f"Doctor ID {doctor_id} not found")

        print("Doctor deleted successfully")
        return True
    except Exception as e:
        print(f"Failed to delete doctor{e}")    
        connection.rollback()
        False

    finally:
        close_connection(connection, cursor)    
    