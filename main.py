from colorama import init, Fore , Style
from utils.patients import get_all_patients, get_patient_by_id, create_patient, update_patient, delete_patient
from utils.doctors import get_all_doctors, get_doctor_by_id, create_doctor, update_doctor, delete_doctor
from utils.billing import get_all_billing, get_billing_by_id, create_bill, update_bill, delete_bill, mark_bill_paid, get_outstanding_bill, get_financial_summary, flag_overdue_bills
from utils.appointments import get_all_appointments, get_appointment_by_id, create_appointment, update_appointment, delete_appointment, check_doctor_availability,cancel_appointment, get_patient_appointments, generate_bill_from_appointment
from utils.inventory import get_all_inventory, get_inventory_by_id, create_inventory, update_inventory, delete_inventory, get_low_stock_items
from utils.medical_records import get_all_medical_records, get_medical_record_by_id, create_record, update_medical_record, delete_medical_record
from utils.auth import login, create_user
from utils.reports import get_appointment_report, get_financial_report, get_patient_report, export_to_csv
from utils.menu_helpers import confirm_delete
from datetime import datetime
import getpass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import sys
init(autoreset=True)

console = Console()
def print_header():
    console.print(Panel(Text("HOSPITAL    MANAGEMENT    SYSTEM", justify="center" , style="bold cyan"), border_style="cyan", padding=(1,2), width=50))

def main_menu():
    print(Fore.YELLOW + "\n MAIN MENU")
    print(Fore.WHITE + "  1. Patients")
    print(Fore.WHITE + "  2. Doctors")
    print(Fore.WHITE + "  3. Appointments")
    print(Fore.WHITE + "  4. Billing")
    print(Fore.WHITE + "  5. Inventory")
    print(Fore.WHITE + "  6. Medical Records")
    print(Fore.WHITE + "  7. Reports")
    print(Fore.RED +   "  8. Log Out")
    print(Fore.CYAN + "-"*45)

def reports_menu():
    while True:
        print(Fore.CYAN + "\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "     REPORTS MODULE")
        print(Fore.CYAN + "\n" + "="*45)
        print(Fore.WHITE + " 1. Financial Report")
        print(Fore.WHITE + " 2. Appointment Report")
        print(Fore.WHITE + " 3. Patient Report")
        print(Fore.RED +   " 4. Go Back")
        print(Fore.CYAN + "-"*45)

        choice = input(Fore.YELLOW + "Enter choice(1-4): ")

        if choice == "1":
            print(Fore.CYAN + "\n=== Financial Report ===")
            try:
                data = get_financial_report()
                if data:
                    print(Fore.CYAN + f"\n  {len(data)} bill(s) found:")
                    print(Fore.CYAN + "-"*41)
                    for b in data:
                        print(Fore.YELLOW + f"  {b['bill_id']} | {b['full_name']} | {b['bill_item']} | GHS {b['amount']} | {b['payment_status']}")
                    print(Fore.CYAN + "-"*41)
                    export = input(Fore.YELLOW + "\n  Export to CSV? (yes/no): ")
                    if export.strip().lower() == 'yes':
                        filepath = export_to_csv(data, "financial_report.csv")
                        print(Fore.GREEN + f"  ✅ Exported to: {filepath}")
                else:
                    print(Fore.RED + "  No billing data found.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "2":
            print(Fore.CYAN + "\n=== Appointment Report ===")
            try:
                data = get_appointment_report()
                if data:
                    print(Fore.CYAN + f"\n  {len(data)} appointment(s) found:")
                    print(Fore.CYAN + "-"*41)
                    for a in data:
                        print(Fore.YELLOW + f"  {a['appointment_id']} | {a['patient_name']} | {a['specialization']} | {a['appointment_date']} | {a['status']}")
                    print(Fore.CYAN + "-"*41)
                    export = input(Fore.YELLOW + "\n  Export to CSV? (yes/no): ")
                    if export.strip().lower() == 'yes':
                        filepath = export_to_csv(data, "appointment_report.csv")
                        print(Fore.GREEN + f"  ✅ Exported to: {filepath}")
                else:
                    print(Fore.RED + "  No appointment data found.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "3":
            print(Fore.CYAN + "\n=== Patient Report ===")
            try:
                data = get_patient_report()
                if data:
                    print(Fore.CYAN + f"\n  {len(data)} patient(s) found:")
                    print(Fore.CYAN + "-"*41)
                    for p in data:
                        print(Fore.YELLOW + f"  {p['patient_id']} | {p['full_name']} | {p['phone']} | {p['region']}")
                    print(Fore.CYAN + "-"*41)
                    export = input(Fore.YELLOW + "\n  Export to CSV? (yes/no): ")
                    if export.strip().lower() == 'yes':
                        filepath = export_to_csv(data, "patient_report.csv")
                        print(Fore.GREEN + f"  ✅ Exported to: {filepath}")
                else:
                    print(Fore.RED + "  No patient data found.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "4":
            break
        else:
            print(Fore.RED + "Invalid choice. Enter 1-4.")




def patient_menu():
    while True:
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "      PATIENT MODULE")
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.WHITE +" 1. View all patients")
        print(Fore.WHITE +" 2. View patient by ID")
        print(Fore.WHITE +" 3. Add patient ")    
        print(Fore.WHITE +" 4. Update patient ") 
        print(Fore.WHITE +" 5. Delete patient ")  
        print(Fore.WHITE +" 6. View patient appointments")    
        print(Fore.RED +  " 7. Go Back")    
        print(Fore.CYAN + "-"*45)

        choice = input(Fore.YELLOW + "  Enter choice (1-6): ")

        if choice == "1":
            patients = get_all_patients()
            if patients:
                table = Table(title=f"Patients ({len(patients)} found)", border_style="cyan")
                table.add_column("ID",style="cyan", justify="center")
                table.add_column("Name",style="white")
                table.add_column("Phone", style="green")
                table.add_column("Blood Group", style="yellow", justify="center")
                table.add_column("Region", style="blue")
                for p in patients:
                    table.add_row(
                    str(p['patient_id']),
                    p['full_name'],
                    p['phone'],
                    str(p['blood_group'] or 'N/A'),
                    p['region']
            )
                console.print(table)
            else:
                console.print("[red]No patients found.[/red]")        
        elif choice == "2":
            patient_id = input("  Patient ID: ")
            try:
                patient_id = int(patient_id)
                patient = get_patient_by_id(patient_id)
                if patient:
                    print(Fore.GREEN + f"  Patient ID: {patient_id} found.")
                    print(Fore.CYAN +"-"*41)
                    print(Fore.YELLOW + f" Patient ID:{patient['patient_id']} | {patient['full_name']} | {patient['phone']} | {patient['blood_group']} | {patient['region']}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.RED + f"  ❌ Paient ID-{patient_id} Not Found")
            except ValueError:
                print(Fore.RED + "  ❌ Invalid input. Enter a number.")         
        elif choice == "3":
            print(Fore.CYAN + "  \n=== Add New Patient ===")
            try:
                full_name = input(Fore.YELLOW + "  Full name: ").strip()
                ghana_card = input(Fore.YELLOW + "  Ghana Card Number: ").strip()

                date_of_birth = input(Fore.YELLOW + "  Date of Birth (YYYY-MM-DD): ").strip()
                datetime.strptime(date_of_birth, "%Y-%M-%d")

                gender = input(Fore.YELLOW + "  Gender (male/female/other): ").strip().lower()
                if gender not in ["male", "female", "other"]:
                    print(Fore.RED + "Gender must be male, female, or other.")
                    continue

                phone = input(Fore.YELLOW + "  Phone: ").strip()
                email = input(Fore.YELLOW + "  Email (press Enter to skip): ").strip() or None
                address = input(Fore.YELLOW + "  Address: ").strip() 
                region = input(Fore.YELLOW + "  Region: ").strip()
                blood_group = input(Fore.YELLOW + "  Blood group (press Enter to skip): ").strip() or None
                nhis_number = input(Fore.YELLOW + "  NHIS Number (press Enter to skip): ").strip() or None

                nhis_expiry_input = input(Fore.YELLOW + "  NHIS Expiry (YYY-MM-DD, press Enter to skip): ").strip()
                if nhis_expiry_input:
                    datetime.strptime(nhis_expiry_input, "%Y-%M-%d")
                    nhis_expiry = nhis_expiry_input
                else:
                    nhis_expiry = None


                emergency_contact_name =input(Fore.YELLOW + "  Emergency Contact Name: ").strip() 
                emergency_contact_phone = input(Fore.YELLOW + "  Emergency Contact Phone: ").strip() 
                registered_by = 1


                result_p = create_patient(
                    full_name, ghana_card, date_of_birth, gender,
                    phone, email, address, region, blood_group,
                    nhis_number, nhis_expiry, emergency_contact_name, emergency_contact_phone,
                    registered_by
                )
                if result_p:
                    print(Fore.GREEN + f"\n Patient added successfullyID: {result_p}.")
                else:
                    print(Fore.RED + "  ❌ Failed to add patient.")
            except Exception as e:
                print(Fore.RED + f" ❌ Error: {e}")            
        elif choice == "4":
            print(Fore.CYAN + "\n=== Update Patient Info ===")
            try:
                patient_id = input(Fore.YELLOW + "  Patient ID: ").strip()
                patient_id = int(patient_id)
                existing = get_patient_by_id(patient_id)
                if not existing:
                    print(Fore.RED + f"  ❌ Patient ID-{patient_id} not found")
                    continue
                full_name = input(Fore.YELLOW + f"  Full name ({existing['full_name']}): ").strip() or existing['full_name']
                phone = input(Fore.YELLOW + f"  Phone ({existing['phone']}): ").strip() or existing['phone']
                email = input(Fore.YELLOW + f"  Email ({existing['email']}) (press enter to skip): ").strip() or existing['email']
                address = input(Fore.YELLOW + f"  Address ({existing['region']}): ").strip() or existing['address']
                region = input(Fore.YELLOW + f"  Region ({existing['region']}): ").strip() or existing['region']
                blood_group =input(Fore.YELLOW + f"  Blood Group ({existing['blood_group']}) (press enter to skip):").strip() or existing['blood_group']
                nhis_number = input(Fore.YELLOW + f"  NHIS Number ({existing['nhis_number']}) (press Enter to skip): ").strip() or existing['nhis_number']

                nhis_expiry_input = input(Fore.YELLOW + f"  NHIS Expiry ({existing['nhis_expiry']}) (YYY-MM-DD, press Enter to skip): ").strip() 
                if nhis_expiry_input:
                    datetime.strptime(nhis_expiry_input, "%Y-%m-%d")
                    nhis_expiry = nhis_expiry_input
                else:
                    nhis_expiry = existing['nhis_expiry']

                emergency_contact_name =input(Fore.YELLOW + f"  Emergency Contact Name({existing['emergency_contact_name']}) : ").strip() or existing['emergency_contact_name']
                emergency_contact_phone = input(Fore.YELLOW + f"  Emergency Contact Phone({existing['emergency_contact_phone']}) : ").strip() or existing['emergency_contact_phone']

                result_p_1 = update_patient(patient_id, full_name, phone, email, address,
                            region, blood_group, nhis_number, nhis_expiry, emergency_contact_name,
                            emergency_contact_phone)
                
                if result_p_1:
                    print(Fore.GREEN + f"  Patient ID-{patient_id} updated successfully")
                else:
                    print(Fore.RED + "  ❌ Failed to update patient") 
            except ValueError:
                print(Fore.RED + "  Invalid input. please enter a number. ")
            except Exception as e:
                print(Fore.RED + f" ❌ Error: {e}")
        elif choice == "5":
            print(Fore.CYAN + "\n=== Delete Patient ===")
            try:
                patient_id_1 = input(Fore.YELLOW + "  Patient ID: ")
                patient_id_1 = int(patient_id_1)
                existing_1 = get_patient_by_id(patient_id_1)
                if not existing_1:
                    print(Fore.RED + f"  ❌Patient ID {patient_id_1} not found.")
                    continue
                details = Fore.BLUE + f" Patient ID: {existing_1['patient_id']} | {existing_1['full_name']} | {existing_1['phone']} | {existing_1['blood_group']} | {existing_1['region']}"
                if confirm_delete(details):
                    delete_patient(patient_id_1)
                    no_of_patients = len(get_all_patients())
                    print(Fore.CYAN + "\n"+"-"*41)
                    print(Fore.BLUE +f"  Total Number Of Patients left: {no_of_patients}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.YELLOW + "  ❌ Cancelled.")   
            except ValueError:
                print(Fore.RED + "  ❌ Invalid input. Please enter a number")
            except Exception as e:
                print(Fore.RED + f" ❌ Error: {e}")    
        elif choice == "6":
            print(Fore.CYAN + "===  Patients Appointments History ===")
            try:
                patient_id = int(input(Fore.YELLOW + "   Patient ID:  "))
                existing = get_patient_by_id(patient_id)
                if not existing:
                    print(Fore.RED + f"  Patient ID : {patient_id} not found.")
                    continue
                appointments = get_patient_appointments(patient_id)
                if appointments:
                    print(Fore.CYAN + f"\n  {len(appointments)} appointment")
                    print(Fore.CYAN + "-"*41)
                    for a in appointments:
                        print(Fore.YELLOW + f"  ID:{a['appointment_id']} | {a['appointment_date']} | {a['appointment_time']} | {a['status']} | {a['specialization']} | {a['department']}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.RED + f"  No appointments found for {existing['full_name']}.")
            except ValueError:
                print(Fore.RED + "  Invalid input. Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")
        elif choice == "7":
            break
        else:
            print("  ❌ Invalid choice. Enter 1-6.")            

def doctor_menu():
    while True:
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "      DOCTOR MODULE")
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.WHITE + " 1. View all doctors")
        print(Fore.WHITE + " 2. View doctor by ID")
        print(Fore.WHITE + " 3. Add doctor")
        print(Fore.WHITE + " 4. Update doctor")
        print(Fore.WHITE + " 5. Delete doctor")
        print(Fore.RED +   " 6. Go Back")
        print(Fore.CYAN + "-"*45)

        choice = input(Fore.YELLOW + "Enter choice (1-6): ")

        if choice == "1":
            try:
                doctors = get_all_doctors()
                if doctors:
                    table = Table(title=f"Doctor {len(doctors)} found",border_style="cyan")
                    table.add_column("ID", justify="center", style="white")
                    table.add_column("Specialization", style="yellow")
                    table.add_column("Available Days", style="white")
                    table.add_column("Consultation Fee (GHS)",style="green", justify="center")
                    for d in doctors:
                        table.add_row(
                            str(d['doctor_id']),
                            d['specialization'] ,
                            str(d['available_days'] or 'N/A'),
                            f"{float(d['consultation_fee'] or 0):.2f}")
                    console.print(table)
                else:
                    console.print("[red]No doctor found.[red/]")  
            except Exception as e:
                console.print(f"[red]Error: {e}[red/]")              

        elif choice == "2":
            print(Fore.CYAN + "\n=== Fetch Doctor By ID ===")
            doctor_id = input(Text("Patient ID: ",style="bold cyan"))
            try:
                doctor_id = int(doctor_id)
                doctor = get_doctor_by_id(doctor_id)
                if doctor:
                    print(Fore.GREEN + f"  Doctor ID: {doctor_id} found.")
                    print(Fore.CYAN + "\n"+"-"*41)
                    print(Fore.YELLOW + f"  Doctor ID: {doctor['doctor_id']} | {doctor['specialization']} | {doctor['department']} | {doctor['available_days']} | {doctor['consultation_fee']}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.RED + f"  ❌ Doctor ID:{doctor_id} not found.")
            except ValueError :
                print(Fore.RED + "  ❌ Invalid input. Enter a number.")            
        elif choice == "3":
            print(Fore.GREEN + "\n=== Add New Doctor ===")
            try: 
                user_id = 1
                specialization = input(Fore.YELLOW + "  Specialization: ").strip().title()
                qualification = input(Fore.YELLOW + "  Qualification: ").strip().title()
                license_number = input(Fore.YELLOW + "  License Number: ").strip().title()
                department = input(Fore.YELLOW + "  Department: ").strip().title()
                available_days = input(Fore.YELLOW + "  Available Days (Enter to skip.): ").strip() or None

                consultation_fee = input(Fore.YELLOW + "  Consultation Fee: ").strip()
                consultation_fee = float(consultation_fee)

                result_d = create_doctor(user_id, specialization,qualification, license_number,
                            department, available_days, consultation_fee)
                if result_d:
                    print(Fore.GREEN + f"  Doctor added successfully ID: {result_d}.")
                else:
                    print(Fore.RED + "  ❌ Failed to add doactor.")
            except ValueError:
                print(Fore.RED + "  ❌ Invalid input. Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  ❌ Error: {e}")                
        elif choice == "4":
            print(Fore.GREEN + "\n=== Update Doctor Info ===")  
            try:
                doctor_id = input(Fore.YELLOW + "  Doctor ID: ")
                doctor_id = int(doctor_id)
                existing = get_doctor_by_id(doctor_id)
                if not existing:
                    print(Fore.RED + f"  ❌ Doctor ID-{doctor_id} not found.")
                    continue

                user_id = input(Fore.YELLOW + f"  User ID ({existing['user_id']}): ").strip() or existing['user_id']
                user_id = int(user_id)

                specialization = input(Fore.YELLOW + f"  Specialization ({existing['specialization']}): ").strip().title() or existing['specialization']
                qualification = input(Fore.YELLOW + f"  Qualification ({existing['qualification']}): ").strip().title() or existing['qualification']
                license_number = input(Fore.YELLOW + f"  License Number ({existing['license_number']}): ").strip().title() or existing['license_number']
                department = input(Fore.YELLOW + f"  Departmnet ({existing['department']}): ").strip().title() or existing['department']
                available_days = input(Fore.YELLOW + f"  Available Days ({existing['available_days']}): ").strip().title() or existing['available_days']

                consultation_fee = input(Fore.YELLOW + f"  Consultation Fee ({existing['consultation_fee']}):").strip() or existing['consultation_fee']
                consultation_fee = float(consultation_fee)

                result_d_1 = update_doctor(doctor_id, user_id, specialization, qualification, 
                            license_number,department, available_days, consultation_fee)
                if result_d_1:
                    print(Fore.GREEN + f"  Doctor ID- {doctor_id} updated successfully.")
                else:
                    print(Fore.RED + f"  ❌ Failed to update doctor ID-{doctor_id}") 
            except ValueError:
                print(Fore.RED + "  ❌ Invalid input. Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  ❌ Error: {e}")               
        elif choice == "5":
            print(Fore.CYAN + "\n=== Delete Doctor Info ===")
            try:
                doctor_id_1 = input(Fore.YELLOW + "  Doctor ID: ")
                doctor_id_1 = int(doctor_id_1)
                existing_1 = get_doctor_by_id(doctor_id_1)
                if not existing_1:
                    print(Fore.RED + f"  ❌ Doctor ID: {doctor_id_1} not found")
                    continue
                details = Fore.BLUE + f" {existing_1['doctor_id']} | {existing_1['specialization']} | {existing_1['department']} | {existing_1['available_days']} | {existing_1['consultation_fee']}"
                if confirm_delete(details):
                    delete_doctor(doctor_id_1)
                    no_of_doctors = len(get_all_doctors())
                    print(Fore.GREEN + f"  Doctor ID:{doctor_id_1} successfully deleted.")
                    print(Fore.CYAN + "\n"+"-"*41)
                    print(Fore.BLUE + f"  Total number of doctors left: {no_of_doctors}")
                    print(Fore.CYAN + "\n"+"-"*41)
                else:
                    print(Fore.YELLOW + "  ❌ cancelled")
            except ValueError:
                print(Fore.RED + "  ❌ Invalid input. Enter a number:")
            except Exception as e:
                print(Fore.RED + f"  ❌ Error: {e}")            
        elif choice == "6":
            break
        else:
            print(Fore.RED + "  ❌ Invalid choice. Enter 1-6.")             
        
def appointment_menu():
    while True:    
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "     APPOINTMENT MODULE")
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.WHITE + " 1. View all appointment")
        print(Fore.WHITE + " 2. View appointment by ID")
        print(Fore.WHITE + " 3. Add Appointment")
        print(Fore.WHITE + " 4. Update Appointment")
        print(Fore.WHITE + " 5. Delete Appointment")
        print(Fore.WHITE + " 6. cancel Appointment")
        print(Fore.WHITE + " 7. Check doctor availability")
        print(Fore.RED +   " 8. GO Back")
        print(Fore.CYAN + "-"*45)

        choice = input(Fore.YELLOW + "Enter choice(1-8): ")

        if choice == "1":
            try:
                appointments = get_all_appointments()
                if appointments:
                    table = Table(title=f"Apponitments({len(appointments)}) found(s) ", title_justify="center", title_style="bold cyan")
                    table.add_column("ID", justify="center", header_style="bold cyan")
                    table.add_column("Patient ID", justify="center",header_style="bold cyan")
                    table.add_column("Doctor ID", justify="center",header_style="bold cyan")
                    table.add_column("Appointment Date", justify="center",header_style="bold cyan")
                    table.add_column("Appointment Time", justify="center",header_style="bold cyan")
                    table.add_column("Appointment Status", justify="center",header_style="bold cyan")
                    for a in appointments:
                        table.add_row(
                            str(a['appointment_id']),
                            str(a['patient_id']),
                            str(a['doctor_id']),
                            str(a['appointment_date']),
                            str(a['appointment_time']),
                            a['status'], style="red" if a['status'] == "cancelled" else "yellow" if a['status'] == "scheduled" else "green"
                        )   
                        
                    console.print(table)    
                else:
                    console.print("[red]No appointment found.[red/]")    
            except Exception as e:
                console.print(f"[red]Error: {e}[red/]")        
                
            
        elif choice == "2":
            print(Fore.GREEN + "\n=== Fetch Appointment By ID ===")
            appointment_id = input(Fore.YELLOW + "  Patient ID: ")
            try:
                appointment_id = int(appointment_id)
                appointment = get_appointment_by_id(appointment_id)
                if appointment:
                    print(Fore.GREEN + f"  Appointment ID: {appointment_id} found")
                    print(Fore.CYAN + "\n"+"-"*41)
                    print(Fore.YELLOW + f"Appointment ID:{appointment['appointment_id']} | Patient ID:{appointment['patient_id']} | Doctor ID:{appointment['doctor_id']} | {appointment['appointment_date']} | {appointment['appointment_time']} | {appointment['status']}")
                    print(Fore.CYAN + "\n"+"-"*41)
                else:
                    print(Fore.RED + f"  ❌ Appointment ID: {appointment_id} not found")
            except ValueError:
                print(Fore.RED +"\n  ❌ Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"\n  ❌ Error: {e}")                
        elif choice == "3":
            print(Fore.GREEN + "\n === Add New Appointment ===")
            try:
                patient_id = input(Fore.YELLOW + "  Patient ID: ").strip()
                patient_id = int(patient_id)

                doctor_id = input(Fore.YELLOW + "  Doctor Id: ").strip()
                doctor_id = int(doctor_id)

                appointment_date = input(Fore.YELLOW + "  Appointment Date: ").strip()
                datetime.strptime(appointment_date, "%Y-%m-%d")

                appointment_time = input(Fore.YELLOW + "  Appointment Time: ").strip()
                datetime.strptime(appointment_time, "%H:%M")

                status = input(Fore.YELLOW + "  Status: ").strip() or 'scheduled'
                if status not in ['scheduled', 'completed', 'cancelled']:
                    print(Fore.BLUE + "  Status must be scheduled/completed/cancelled.")
                    continue
                notes = input(Fore.YELLOW + "  Notes: ").strip() or None

                available = check_doctor_availability(doctor_id, appointment_date, appointment_time)
                if not available:
                    print(Fore.RED + f"\n Doctor ID {doctor_id} is already booked on {appointment_date} at {appointment_time}.")
                    print(Fore.YELLOW + "  Please choose a different date, time, or doctor.")
                    continue

                result_a = create_appointment(patient_id, doctor_id, appointment_date,
                            appointment_time, status, notes)
                if result_a:
                    print(Fore.GREEN +f" Appointment successfully booked. ID: {result_a}")
                else:
                    print(Fore.RED + "  ❌ Failed to book appointment.")
            except ValueError:
                print(Fore.RED +"\n  ❌ Inavlid input.Enter a number")
            except Exception as e:
                print(Fore.RED + f"  ❌ Error: {e}")                
        elif choice == "4":
            print(Fore.GREEN + "\n=== Update Appointment ===")
            try:
                appointment_id_1 = input(Fore.YELLOW + "  Appointment ID: ")
                appointment_id_1 = int(appointment_id_1)
                existing_a = get_appointment_by_id(appointment_id_1)
                if not existing_a:
                    print(Fore.RED + f"  Appointment ID: {appointment_id_1} not found.")
                    continue

                patient_id_a = input(Fore.YELLOW + f" Patient ID ({existing_a['patient_id']}): ").strip() or existing_a['patient_id']
                patient_id_a = int(patient_id_a)

                doctor_id_1 = input(Fore.YELLOW + f"  Doctor ID ({existing_a['doctor_id']}):").strip() or existing_a['doctor_id']
                doctor_id_1 = int(doctor_id_1)

                appointment_date_input = input(Fore.YELLOW + f"  Appointment Date ({existing_a['appointment_date']}): ").strip()
                if appointment_date_input:
                    datetime.strptime(appointment_date_input, "%Y-%m-%d")
                    appointment_date_1 = appointment_date_input
                else:
                    appointment_date_1 = existing_a['appointment_date']  

                appointment_time_input = input(Fore.YELLOW + f"  Appointment Time ({existing_a['appointment_time']}): ")
                if appointment_time_input:
                    datetime.strptime(appointment_time_input, "%H:%M")
                    appointment_time_1 = appointment_time_input
                else:
                    appointment_time_1 = existing_a['appointment_time'] 

                status_input = input(Fore.YELLOW + f"  Status ({existing_a['status']}): ")
                if status_input:
                    status_1 = status_input
                    if status_1 not in ['scheduled', 'completed', 'cancelled']:
                        print(Fore.RED + "  Status must be scheduled/completed/cancelled.") 
                        continue
                else:
                    status_1 = existing_a['status']

                notes_1 = input(Fore.YELLOW + f"  Notes ({existing_a['notes']}): ").strip() or existing_a['notes']

                result_a_1 = update_appointment(appointment_id_1, patient_id_a, doctor_id_1,appointment_date_1,
                            appointment_time_1, status_1, notes_1)  
                if result_a_1 is not None:
                    print(Fore.GREEN + f"\n  Appointment ID: {appointment_id_1} updated successfully.")
                else:
                    print(Fore.RED + f"\n  Failed to update Appointment ID: {appointment_id_1}")  
            except ValueError:
                print(Fore.RED + "\n  Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")               
        elif choice == "5":
            print(Fore.GREEN + "\n=== Delete Appointment ===")
            try:
                appointment_id_2 = input(Fore.YELLOW + "  Appointment ID: ").strip()
                appointment_id_2 = int(appointment_id_2)
                existing_1 = get_appointment_by_id(appointment_id_2)
                if not existing_1:
                    print(Fore.RED + f"\n  Appointment ID: {appointment_id_2} not found.")
                    continue
                details = Fore.BLUE + f"Appointment ID:{existing_1['appointment_id']} | Patient ID:{existing_1['patient_id']} | Doctor ID:{existing_1['doctor_id']} | {existing_1['appointment_date']} | {existing_1['appointment_time']} | {existing_1['status']}"
                if confirm_delete(details):
                    delete_appointment(appointment_id_2)
                    no_of_appointments = len(get_all_appointments())
                    print(Fore.GREEN + f"\n  Appointment ID: {appointment_id_2} deleted sucessfully.")
                    print(Fore.CYAN + "\n" +"-"*41)
                    print(Fore.WHITE + f"\n  Total number of appointments left: {no_of_appointments}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.YELLOW + "  cancelled.")    
            except ValueError:
                print(Fore.RED + "\n  Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"\n  Error: {e}")            
        elif choice == "6":
            print(Fore.CYAN + "\n=== Cancel Appointment ===")
            try:
                appointment_id = int(input(Fore.YELLOW + "  Appointment ID: "))
                existing = get_appointment_by_id(appointment_id)
                if not existing:
                    print(Fore.RED + f"  Appointment ID: {appointment_id} does not exist.")
                    continue
                if existing['status'] != 'scheduled':
                    print(Fore.RED + f"  cannot cancel - status is already '{existing['status']}'")
                    continue
                print(Fore.CYAN + f"  Appointment ID: {appointment_id}") 
                print(Fore.WHITE + f"  Patient: {existing['patient_id']} | Doctor: {existing['doctor_id']} | {existing['appointment_date']} | {existing['appointment_time']}") 
                confirm = input(Fore.RED + "\n  Confirm cancel? (yes/no): ")
                if confirm.strip().lower() == 'yes':
                    result = cancel_appointment(appointment_id)
                    
                    if result:
                        print(Fore.GREEN + f"\n  ✅ Appointment {appointment_id} cancelled successfully.")
                        print(result)
                    else:
                        print(Fore.RED + "  ❌ Failed to cancel appointment.")
                elif confirm.lower() == 'no': 
                    print(Fore.YELLOW + "  Cancelled.")      
                else:
                    print(Fore.RED + "  Enter the right choice yes/no.")
            except ValueError:
                print(Fore.RED + "  Invalid input. Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")  
        elif choice == "7":
            print(Fore.CYAN + "\n=== Check Doctor Availability ===")
            try:
                doctor_id = int(input(Fore.YELLOW + "  Doctor ID: "))
                date = input(Fore.YELLOW + "  Date (YYYY-MM-DD): ").strip()
                datetime.strptime(date, "%Y-%m-%d")
                time = input(Fore.YELLOW + "  Time (HH:MM): ").strip()
                datetime.strptime(time, "%H:%M")

                available = check_doctor_availability(doctor_id, date, time)
                if available:
                    print(Fore.GREEN + f"\n  ✅ Doctor ID {doctor_id} is AVAILABLE on {date} at {time}.")
                else:
                    print(Fore.RED + f"\n  ❌ Doctor ID {doctor_id} is NOT AVAILABLE on {date} at {time}.")
            except ValueError:
                print(Fore.RED + "  Invalid input. Check date and time format.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")
        elif choice == "8":
            break
        else:
            print(Fore.RED + "Invalid choice. Enter choice 1-8.")                   
            
def billing_menu():
    while True:
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "     BILLING MODULE")
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.WHITE + " 1. View all billing")
        print(Fore.WHITE + " 2. View billing by ID")
        print(Fore.WHITE + " 3. Add billing")
        print(Fore.WHITE + " 4. Update billing")
        print(Fore.WHITE + " 5. Delete billing")
        print(Fore.WHITE +   " 6. Mark bill as paid")
        print(Fore.RED +   " 7. View outstanding bills")
        print(Fore.YELLOW +   " 8. Financial summary")
        print(Fore.WHITE +   " 9. Generate Bill From Appointment.")
        print(Fore.WHITE +   " 10. Flag Overdue Bills.")
        print(Fore.RED +   " 11. GO Back")
        print(Fore.CYAN + "-"*45)
        
        choice = input(Fore.YELLOW + "Enter choice(1-11): ")

        if choice == "1":
            try:
                billing = get_all_billing()
                if billing:
                    table = Table(title=f"Billing ({len(billing)} found)",title_justify="center", title_style="bold cyan")
                    table.add_column("ID", justify="center")
                    table.add_column("Patient ID", justify="center")
                    table.add_column("Appointment ID", justify="center")
                    table.add_column("Bill Item", justify="center")
                    table.add_column("Amount", justify="center")
                    table.add_column("Payment Status", justify="center")
                    for b in billing:
                        table.add_row(
                        str(b['bill_id']),
                        str(b['patient_id']),
                        str(b['appointment_id']),    
                        b['bill_item'],    
                        f"{float(b['amount']):.2f}",    
                        b['payment_status'], style="red" if b['payment_status'] == "overdue" else "yellow" if b['payment_status'] =="pending" else "green"   
                        )
                    console.print(table)
                else:
                    console.print("[red]No bill found[red/]")
            except Exception as e:
                console.print(f"[red]Error: {e}red/]")     
        elif choice == "2":
            print(Fore.GREEN + "\n=== Fetch Billing By ID ===")
            bill_id = input(Fore.YELLOW + "  Bill ID: ")
            try:
                bill_id = int(bill_id)
                bill = get_billing_by_id(bill_id)
                if bill:
                    print(Fore.GREEN + f"\n  Bill ID: {bill_id} found")
                    print(Fore.CYAN + "-"*41)
                    print(Fore.YELLOW + f"Bill ID:{bill['bill_id']} | Patient ID:{bill['patient_id']} | Appointment ID:{bill['appointment_id']} | {bill['bill_item']} | {bill['amount']} | {bill['payment_status']}")
                    print(Fore.CYAN + "-"*41) 
                else:
                    print(Fore.RED + f"  Bill ID: {bill_id} doesn\'t exist.")
            except ValueError:
                print(Fore.RED + "  Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")
        elif choice == "3":
            print(Fore.GREEN + "\n=== Add New Bill ===")
            try:
                patient_id_b = int(input(Fore.YELLOW + "  Patient ID: "))
                appointment_id_b = int(input(Fore.YELLOW + "  Appointment ID: "))
                bill_item = input(Fore.YELLOW + "  Bill Item:  ").strip()
                amount = float(input(Fore.YELLOW + "  Amount: "))

                payment_status = input(Fore.YELLOW + "  Payment Status: ") or 'pending' 
                if payment_status not in ['pending', 'paid', 'overdue']:
                    print(Fore.RED + "  Payment status must be pending/paid/overdue.")
                    continue

                payment_date_input = input(Fore.YELLOW + "  Payment Date: ")
                if payment_date_input:
                    datetime.strptime(payment_date_input, "%Y-%m-%d")
                    payment_date = payment_date_input
                else:
                    payment_date = None

                result = create_bill(patient_id_b, appointment_id_b, bill_item,
                            amount, payment_status, payment_date)

                if result:
                    print(Fore.GREEN + f"  Bill successfully added ID: {result}")
                else:
                    print(Fore.RED + "  Failed to add  bill.")
            except ValueError:
                print(Fore.RED + " Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")                
        elif choice == "4":
            print(Fore.GREEN + "\n === Update Billing ===")
            try:
                bill_id = int(input(Fore.YELLOW + "  Bill ID: "))
                existing  = get_billing_by_id(bill_id)
                if not existing:
                    print(Fore.RED + f"  Bill ID: {bill_id} not found.")
                    continue

                patient_id_b = (input(Fore.YELLOW + f"  Patient ID({existing['patient_id']}): ")) or existing['patient_id']
                patient_id_b = int(patient_id_b)

                appointment_id_b = (input(Fore.YELLOW + f"  Appointment ID({existing['appointment_id']}): ")) or existing['appointment_id']
                appointment_id_b = int(appointment_id_b)

                bill_item = input(Fore.YELLOW + f"  Bill Item({existing['bill_item']}): ").strip() or existing['bill_item']

                amount = input(Fore.YELLOW + f"  Amount({existing['amount']}): ") or existing['amount']
                amount = float(amount)

                payment_status_input = input(Fore.YELLOW + f"  Payment Status({existing['payment_status']}): ")
                if payment_status_input:
                    payment_status = payment_status_input 
                    if payment_status not in ['pending', 'paid', 'overdue']:
                        print(Fore.RED + "  Payment status must be pending/paid/overdue.")
                        continue
                else:
                    payment_status = existing['payment_status']

                payment_date_input = input(Fore.YELLOW + f"  Payment Date({existing['payment_date']}): ")
                if payment_date_input:
                    datetime.strptime(payment_date_input, "%Y-%m-%d")
                    payment_date = payment_date_input
                else:
                    payment_date = existing['payment_date']   

                result = update_bill(bill_id, patient_id_b, appointment_id_b, bill_item, amount, payment_status, payment_date)
                if result is not None:
                    print(Fore.GREEN + f"  Bill updated successfully ID: {bill_id}")
                else:
                    print(Fore.RED + f"  Failed update bill ID: {bill_id}")                            
            except ValueError:
                print(Fore.RED + " Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")     
        elif choice == "5":
            print(Fore.GREEN + "\n=== Delete Billing ===")
            try:
                bill_id = int(input(Fore.YELLOW + "  Bill ID: "))
                existing  = get_billing_by_id(bill_id)
                if not existing:
                    print(Fore.RED + f"  Bill ID: {bill_id} not found.")
                    continue
                details = Fore.BLUE + f"Bill ID:{existing['bill_id']} | Patient ID:{existing['patient_id']} | Appointment ID:{existing['appointment_id']} | {existing['bill_item']} | {existing['amount']} | {existing['payment_status']}"
                if confirm_delete(details):
                    delete_bill(bill_id)
                    no_of_billings = len(get_all_billing())
                    print(Fore.GREEN + f"\n  Bill ID: {bill_id} deleted successfully.")
                    print(Fore.CYAN + "\n" +"-"*41)
                    print(Fore.WHITE + f"\n  Total number of Billings left: {no_of_billings}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.YELLOW + "  cancelled.")    
            except ValueError:
                print(Fore.RED + " Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")      
        elif choice == "6":
            print(Fore.CYAN + "===  Mark Bill As Paid ===")
            try:
                bill_id = int(input(Fore.YELLOW + "  Bill ID: "))
                result = mark_bill_paid(bill_id)
                if result == 'not found':
                    print(Fore.RED+ f"  ❌ Bill ID {bill_id} not found.")
                if result == 'already paid' :
                    print(Fore.RED + f"  ❌ Bill ID {bill_id} is already paid.")
                else:
                    print(Fore.GREEN + f"  ✅ Bill ID {bill_id} marked as paid.")
            except ValueError:   
                print(Fore.RED + "  Invalid input. Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")    
        elif choice == "7":
            print(Fore.CYAN + "\n === Outstanding Bills ===")
            bills = get_outstanding_bill()
            if bills :
                print(Fore.GREEN + f"   {len(bills)} outstanding bill (s) ")
                print(Fore.CYAN + "\n"+"-"*41)
                for b in bills:
                    print(Fore.YELLOW + f"Bill ID:{b['bill_id']} | Patient ID:{b['patient_id']}  | {b['bill_item']} | GHS{b['amount']} | {b['payment_status']}")
                print(Fore.CYAN + "-"*41) 
            else:
                print(Fore.RED + "\n  No outstanding bill found.")
      
        elif choice == "8":
            print(Fore.CYAN + "\n=== Financial Summary ===")
            try:
                summary = get_financial_summary()
                if summary:
                    table = Table(title="Financial Summary", border_style="green")
                    table.add_column("Category", style="white")
                    table.add_column("Count", style="cyan", justify="center")
                    table.add_column("Amount (GHS)", style="green", justify="right")

                    table.add_row(
                        "✅ Paid",
                        str(summary['paid_count']),
                        f"{summary['total_revenue'] or 0:.2f}"
                    )
                    table.add_row(
                        "⏳ Pending",
                        str(summary['pending_count']),
                        f"{summary['total_pending'] or 0:.2f}"
                    )
                    table.add_row(
                        "🚨 Overdue",
                        "-",
                        f"{summary['total_overdue'] or 0:.2f}"
                    )
                    table.add_section()
                    table.add_row(
                        "[bold]Total Bills[/bold]",
                        str(summary['total_bills']),
                        f"[bold]{(summary['total_revenue'] or 0) + (summary['total_pending'] or 0) + (summary['total_overdue'] or 0):.2f}[/bold]"
                    )
                    console.print(table)
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        elif choice == "9":
            try:
                appointment_id = int(input(Fore.YELLOW + "  Appointment ID: "))
                result = generate_bill_from_appointment(appointment_id)
                if result == "not found":
                    print(Fore.RED + f"  Appointment ID {appointment_id} not found")
                elif result :
                    print(Fore.GREEN + f" Bill Generated successfully.Bill ID: {result}") 
                else:
                    print(Fore.RED + "  Failed to generate bill.")
            except ValueError:
                print(Fore.RED + "  Failed to generate bill.")
            except Exception as e:
                print(Fore.RED + f"  Error:{e}")                   
        elif choice == "10":
            print(Fore.CYAN + "===  Flag Overdue Bills ===")
            try:
                result = flag_overdue_bills()
                if result:
                    print(Fore.GREEN + f"  🚨{result} bill(s) as overdue.")
                else:
                    print(Fore.RED +  "  ✅  No bills to flag.All pending bills are within 7 days.") 
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")          
        elif choice == "11":
            break
        else:
            print(Fore.RED + "Invalid choice. Enter choice (1-11)")  

def inventory_menu():
    while True:
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "     INVENTORY MODULE")
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.WHITE + " 1. View all inventory.")
        print(Fore.WHITE + " 2. View inventory. by ID")
        print(Fore.WHITE + " 3. Add inventory.")
        print(Fore.WHITE + " 4. Update inventory.")
        print(Fore.WHITE + " 5. Delete inventory")
        print(Fore.WHITE + " 6. low stock alert 🚨")
        print(Fore.RED +   " 7. GO Back")
        print(Fore.CYAN + "-"*45)
        
        choice = input(Fore.YELLOW + "Enter choice(1-7): ")
        
        if choice == "1":
            try:
                inventory = get_all_inventory()
                if inventory:
                    table = Table(title=f"Inventory({len(inventory)})", title_style="bold cyan", title_justify="center")
                    table.add_column("ID", justify="center")
                    table.add_column("Item Name", justify="center")
                    table.add_column("Item Category", justify="center")
                    table.add_column("Quantity", justify="center")
                    table.add_column("Reorder Level", justify="center")
                    table.add_column("Item Cost", justify="center")
                    for i in inventory:
                        table.add_row(
                            str(i['item_id']),
                            str(i['item_name']),
                            str(i['item_category']),
                            str(i['quantity']),
                            str(i['reorder_level']),
                            f"{float(i['item_cost']):.2f}"
                        )
                    console.print(table)    
                else:
                    console.print("[red]No inventory Found.[red/]")   
            except Exception as e:
                console.print(f"[red]Error: {e}.[red/]")            
        elif choice == "2":
            item_id = input("  Item ID: ")
            try:
                item_id = int(item_id)
                inventory = get_inventory_by_id(item_id)
                if inventory:
                    print(Fore.CYAN + f"  Inventory ID: {item_id} found")
                    print(Fore.CYAN + "-"*45)
                    print(Fore.YELLOW + f"Item ID:{inventory['item_id']} | {inventory['item_name']} | {inventory['item_category']} | {inventory['quantity']} | {inventory['reorder_level']} | {inventory['item_cost']}")
                    print(Fore.CYAN + "-"*45)
                else:
                    print(Fore.RED + "No iventory found with the ID")
            except ValueError:
                print(Fore.RED + "  Invalid input. Enter a number.")
            except Exception as e:    
                print(Fore.RED+ f"  Error: {e}")        
        elif choice == "3":
            print(Fore.GREEN + "\n === Add New Inventory ===")
            try:
                item_name = input(Fore.YELLOW + "  Item Name: ").strip()

                item_category = input(Fore.YELLOW + "  Item Category (medicine/equipment/supplies): ").strip()
                if item_category not in ['medicine', 'equipment', 'supplies']:
                    print(Fore.RED + " Item category must be medicine/equipment/supplies")
                    continue

                quantity =  input(Fore.YELLOW + "  Quantity: ").strip()
                quantity = int(quantity) 

                reorder_level = input(Fore.YELLOW + "  Reorder Level: ").strip()
                reorder_level = int(reorder_level)

                item_cost = input(Fore.YELLOW + "  Item Cost: ").strip()
                item_cost = float(item_cost)

                result = create_inventory(item_name, item_category, quantity, reorder_level,
                            item_cost)    
                if result:
                    print(Fore.GREEN + f"  Inventory added successfull ID: {result}")
                else:
                    print(Fore.RED + "  Failed to add inventory.")
            except ValueError:
                print(Fore.RED + "  Invalid input. Enter a number.")
            except Exception as e:    
                print(Fore.RED+ f"  Error: {e}")                
        elif choice == "4":
            print(Fore.GREEN + "\n=== Update Inventory ===")
            try:
                item_id = input(Fore.YELLOW + "  Item ID: ")
                item_id = int(item_id)
                existing = get_inventory_by_id(item_id)
                if not existing:
                    print(Fore.RED + f"  Item ID: {item_id} not found.")
                    continue
                item_name = input(Fore.YELLOW + f"  Item Name({existing['item_name']}): ") or existing['item_name']

                item_category_input = input(Fore.YELLOW + f" Item Category({existing['item_category']}): ")
                if item_category_input:
                    item_category = item_category_input
                    if item_category not in ['medicine', 'equipment', 'supplies']:
                        print(Fore.RED + " Item category must be medicine/equipment/supplies")
                        continue
                else:
                    item_category = existing['item_category']

                quantity = input(Fore.YELLOW + f"  Quantity({existing['quantity']}): ") or existing['quantity']
                quantity = int(quantity)

                reorder_level = input(Fore.YELLOW + f"  Reorder Level ({existing['reorder_level']}):") or existing['reorder_level']
                reorder_level = int(reorder_level)

                item_cost = input(Fore.YELLOW + f"  Item Cost ({existing['item_cost']}): ").strip() or existing['item_cost']
                item_cost = float(item_cost)

                result = update_inventory(item_id, item_name, item_category, quantity,
                            reorder_level, item_cost)
                if result is not None:
                    print(Fore.GREEN + f"  Inventory updated successfully ID: {item_id}")
                else:
                    print(Fore.RED + "  Failed to Update inventory.")
            except ValueError:
                print(Fore.RED + "  Invalid input. Enter a number.")
            except Exception as e:    
                print(Fore.RED+ f"  Error: {e}")              
        elif choice == "5":
            print(Fore.GREEN + "\n=== Delete Inventory ===")
            try:
                item_id = input(Fore.YELLOW + "  Item ID: ")
                item_id = int(item_id)
                existing = get_inventory_by_id(item_id)
                if not existing:
                    print(Fore.RED + f"  Item ID: {item_id} not found.")
                    continue
                details = Fore.BLUE + f"Item ID:{existing['item_id']} | {existing['item_name']} | {existing['item_category']} | {existing['quantity']} | {existing['reorder_level']} | {existing['item_cost']}"
                if confirm_delete(details):
                    delete_inventory(item_id)
                    no_of_inventory = len(get_all_inventory())
                    print(Fore.GREEN + f"\n  Item ID: {item_id} deleted successfully.")
                    print(Fore.CYAN + "\n" +"-"*41)
                    print(Fore.WHITE + f"\n  Total number of Inventory left: {no_of_inventory}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.YELLOW + "  cancelled.")    
            except ValueError:
                print(Fore.RED + " Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")    
        elif choice == "6":
            print(Fore.CYAN + "\n===  Low Stock Alert === ")
            low_stock = get_low_stock_items()
            if low_stock:
                print(Fore.RED + f"\n  ⚠️  {len(low_stock)} item(s) below reorder level:")
                print(Fore.CYAN + "-"*41)
                for item in low_stock:
                    print(Fore.RED + f"  🚨 {item['item_name']} | Stock: {item['quantity']} | Reorder at: {item['reorder_level']}")
                print(Fore.CYAN + "-"*41)
            else:
                print(Fore.GREEN + "\n  ✅ All items are sufficiently stocked.")

        elif choice == "7":
            break
        else:
            print(Fore.RED + "Invalid choice. Enter choice 1-7.")  


def medical_records_menu():
    while True:
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.YELLOW + Style.BRIGHT + "     MEDICAL RECORD MODULE")
        print(Fore.CYAN +"\n" + "="*45)
        print(Fore.WHITE + " 1. View all medical records")
        print(Fore.WHITE + " 2. View medical record ID")
        print(Fore.WHITE + " 3. Add medical record")
        print(Fore.WHITE + " 4. Update medical record")
        print(Fore.WHITE + " 5. Delete medical record")
        print(Fore.RED +   " 6. GO Back")
        print(Fore.CYAN + "-"*45)
        
        choice = input(Fore.YELLOW + "Enter choice(1-6): ")
        
        if choice == "1":
            print(Fore.GREEN + "\n=== Fetch all Medical Records ===")
            try:
                medical_records = get_all_medical_records()
                if medical_records:
                    table = Table(title=f"Medical Records ({len(medical_records)}) found", title_style="bold cyan", title_justify="center")
                    table.add_column("ID", style="bold cyan", justify="center")
                    table.add_column("Patient ID", style="bold cyan", justify="center")
                    table.add_column("Doctor ID", style="bold cyan", justify="center")
                    table.add_column("Appointment ID", style="bold cyan", justify="center")
                    table.add_column("Diagnosis", style="yellow", justify="center")
                    table.add_column("Treatment", style="green", justify="center")
                    table.add_column("Lab Test", style="bold cyan", justify="center")
                    table.add_column("Notes", style="white", justify="center")
                    for m_r in medical_records:
                        table.add_row(
                            str(m_r['record_id']),
                            str(m_r['doctor_id']),
                            str(m_r['patient_id']),
                            str(m_r['appointment_id']),
                            str(m_r['diagnosis']),
                            str(m_r['treatment']),
                            str(m_r['lab_tests']),
                            str(m_r['notes'] or 'N/A')
                        )
                    console.print(table)    
                else:
                    console.print("[red] No Medical Record  found.red/]")
            except Exception as e:
                console.print(f"[red]Error: {e}.[red/]") 
        elif choice == "2":
            print(Fore.GREEN + "\n === Fetch Medical Record By ID ===")
            try:
                record_id = input(Fore.YELLOW + "  Record ID: ")
                record_id = int(record_id)

                medical_record = get_medical_record_by_id(record_id)
                if medical_record:
                    print(Fore.CYAN + "\n"+"-"*41)
                    print(Fore.YELLOW +  f"  Record ID: {medical_record['record_id']} | {medical_record['patient_id']} | {medical_record['doctor_id']} | {medical_record['appointment_id']} | {medical_record['diagnosis']} | {medical_record['treatment']} | {medical_record['lab_tests']} | {medical_record['notes']} ")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.RED + "  No Medical Record  found")
            except ValueError:
                print(Fore.RED + "  Invalid input.Enter a number.")        
            except Exception as e:
                print(Fore.RED + f"  Error: {e}") 
        elif choice == "3":
            print(Fore.GREEN + "\n === Add New  Medical Record ===")
            try:
                patient_id_mr = input(Fore.YELLOW + "  Patient ID: ").strip()
                patient_id_mr = int(patient_id_mr)

                doctor_id_mr = input(Fore.YELLOW + "  Doctor ID: ").strip()
                doctor_id_mr = int(doctor_id_mr)

                appointment_id_mr = input(Fore.YELLOW + "  Appointment ID: ").strip()
                appointment_id_mr= int(appointment_id_mr)

                diagnosis = input(Fore.YELLOW + " Diagnosis: ").strip()
                treatment = input(Fore.YELLOW + " Treatment: ").strip() or None
                lab_tests = input(Fore.YELLOW + " Lab Test: ").strip() or None
                notes = input(Fore.YELLOW + " Notes: ").strip() or None
                
                result = create_record(patient_id_mr, doctor_id_mr,appointment_id_mr,diagnosis,
                            treatment,lab_tests,notes)
                
                if result :
                    print(Fore.GREEN + f"  Medical Record Added Successfully ID: {result}")
                else:
                    print(Fore.RED + "  Failed to add Medical Record.")    
            except ValueError:
                print(Fore.RED + "  Invalid input.Enter a number.")        
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")         
        elif choice == "4":
            print(Fore.GREEN + "\n=== Update Medical Record ===")
            try:
                record_id = input(Fore.YELLOW + "  Record ID: ")
                record_id = int(record_id)
                existing = get_medical_record_by_id(record_id)
                if not existing:
                    print(Fore.RED + f"  Record ID: {record_id} not found.")
                    continue
                print(Fore.GREEN + f"  Record ID: {record_id} found.")
                patient_id_mr = input(Fore.YELLOW + f"  Patient ID({ existing['patient_id']}): ").strip() or existing['patient_id']
                patient_id_mr = int(patient_id_mr)

                doctor_id_mr = input(Fore.YELLOW + f"  Doctor ID(): ").strip() or  existing['doctor_id']
                doctor_id_mr = int(doctor_id_mr)

                appointment_id_mr = input(Fore.YELLOW + f"  Appointment ID({existing['appointment_id']}): ").strip() or existing['appointment_id']
                appointment_id_mr= int(appointment_id_mr)

                diagnosis = input(Fore.YELLOW + f"  Diagnosis({existing['diagnosis']}): ").strip() or  existing['diagnosis']
                treatment = input(Fore.YELLOW + f"  Treatment({existing['treatment']}): ").strip() or  existing['treatment']
                lab_tests = input(Fore.YELLOW + f"  Lab Test({existing['lab_tests']}): ").strip() or  existing['lab_tests']
                notes = input(Fore.YELLOW + f"  Notes({existing['notes']}): ").strip() or existing['notes']

                result = update_medical_record(record_id, patient_id_mr, doctor_id_mr, appointment_id_mr,
                            diagnosis, treatment, lab_tests, notes)
                if result is not None:
                    print(Fore.GREEN + f"  Medical Record Updated Successfully ID: {record_id}")
                else:
                    print(Fore.RED + "  Failed to update Medical Record.")    
            except ValueError:
                print(Fore.RED + "  Invalid Input.Enter a number.")        
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")         
                
        elif choice == "5":
            print(Fore.GREEN + "\n=== Delete Medical Record ===") 
            try:
                record_id = input(Fore.YELLOW + "  Record ID: ")
                record_id = int(record_id)
                existing = get_medical_record_by_id(record_id)
                if not existing:
                    print(Fore.RED + f"  Record ID: {record_id} not found.")
                    continue
                print(Fore.GREEN + f"  Record ID: {record_id} found.")
                details = Fore.YELLOW +  f"  Record ID: {existing['record_id']} | {existing['patient_id']} | {existing['doctor_id']} | {existing['appointment_id']} | {existing['diagnosis']} | {existing['treatment']} | {existing['lab_tests']} | {existing['notes']} "
                if confirm_delete(details):
                    delete_medical_record(record_id)
                    no_of_records = len(get_all_medical_records())
                    print(Fore.GREEN + f"\n  Item ID: {record_id} deleted successfully.")
                    print(Fore.CYAN + "\n" +"-"*41)
                    print(Fore.WHITE + f"\n  Total number of Medical Records left: {no_of_records}")
                    print(Fore.CYAN + "-"*41)
                else:
                    print(Fore.YELLOW + "  cancelled.")    
            except ValueError:
                print(Fore.RED + " Invalid input.Enter a number.")
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")    
        elif choice == "6":
            break
        else:
            print(Fore.RED + "Invalid choice. Enter choice 1-6.")  

if __name__=="__main__":
    while True:
        print_header()
        print(Fore.WHITE + "\n1. Register User")
        print(Fore.WHITE + "2. Login User")
        print(Fore.WHITE + "3. Quit")
        
        choice = input(Fore.YELLOW + "\n  Enter choice (1-3):")

        if choice == "1":
            print(Fore.GREEN + "===  Register User ===")
            try:
                username = input(Fore.YELLOW + "  Username: ").strip()
                if len(username) < 3 :
                    print(Fore.RED + "  username must be at least 3 characters.")
                    continue

                password = getpass.getpass(Fore.YELLOW + "  Password: ").strip()
                if  len(password) < 6:
                    print(Fore.RED + "  password must be at least 6 characters.")
                    continue

                role = input(Fore.YELLOW + "  Role: ").strip()
                if role not in ['admin', 'medical_superintendent', 'hospital_administrator', 'doctor', 'nurse', 'lab_technician', 'cashier', 'accountant',
                            'auditor', 'pharmacist', 'record_manager', 'storekeeper', 'procurement_officer'] :
                    print(Fore.RED + """ role must be (admin/medical superintendent/hospital administrator/doctor/nurse/lab technician/cashier/accountant/
                            auditor/pharmacist/record_manager/storekeeper/procurement_officer).""")
                    continue  
                    
                full_name = input(Fore.YELLOW + "  Full Name: ").title().strip()
                if not full_name:
                    print(Fore.RED + "  enter full name.")
                    continue    
                    
                email = input(Fore.YELLOW + "  Email: ").strip() or None
                phone_input = input(Fore.YELLOW + "  Phone: ").strip()
                if phone_input:
                    phone = phone_input
                    if len(phone) != 10 :
                        print(Fore.RED + "  phone must be at least 10 characters.")
                        continue
                else:
                    phone = None

                result = create_user(username, password, role, full_name, email, phone )

                if result:
                    print(Fore.GREEN + f"  User Registered Successfully ID: {result}.")
                else:
                    print(Fore.RED + "  Failed to register user.")       
            except Exception as e:
                print(Fore.RED + f"  Error: {e}")

        elif choice == "2":
            print(Fore.LIGHTGREEN_EX+ "=== LOGIN USER ===")
            try:
                login_username = input(Fore.LIGHTYELLOW_EX+ " Username: ")
                if len(login_username) < 3:
                    print(Fore.RED + "  Username must be at least 3 characters" )
                    continue
                login_password = getpass.getpass(Fore.LIGHTYELLOW_EX + " Password: ")    
                if len(login_password) < 6:
                    print(Fore.RED + "  Password must be at least 6 characters")
                    continue      

                user_login = login(login_username, login_password)
                if user_login is not None :
                    print(Fore.GREEN + f"\n  ✅ Welcome, {user_login['full_name']} | Role: {user_login['role'].upper()}")
                    while True:
                        print(Fore.CYAN + "  " + "-"*41)
                        main_menu()
                        choice = input(Fore.YELLOW + " Enter choice (1-7): ")

                        if choice == "1":
                            patient_menu()
                        elif choice == "2":
                            doctor_menu()  
                        elif choice == "3":
                            appointment_menu()
                        elif choice == "4":
                            billing_menu()
                        elif choice == "5":
                            inventory_menu()
                        elif choice == "6":
                            medical_records_menu()  
                        elif choice == "7":
                            reports_menu()                    
                        elif choice == "8":
                            break
                        else :
                            print(Fore.RED + "  coming soon....")
                else:
                    print(Fore.RED + " Username or password dosen't exist.")
            except Exception as e:
                print(Fore.CYAN +f"  Error: {e}")        
        elif choice == "3":
            print(Fore.GREEN + "\n Goodbye! Stay Healty. 👋")
            sys.exit(0)
        else: 
            print(Fore.RED + "  enter the right choice (1-3).")