from utils.auth import create_user, login

"""result = create_user(
    username="nkansah_admin",
    password="Admin123",
    role="admin",
    full_name="Prince Nkansah",
    email="nkansahp476@gmail.com")

print(f"user cretaed- ID: {result}")"""

user = login("nkansah_admin", "Admin123")
if user:
    print(f"LOGIN SUCCESFUL- Welcome {user['full_name']} | Role: {user['role']}")
else:
    print("failed to login")    