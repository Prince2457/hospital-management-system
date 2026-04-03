def confirm_delete(details=""):
    if details:
        print(details)
    user_input = input("Enter yes to confirm delete. no to cancel delete: ")
    if user_input.lower() =="yes":
        return True
    return False
