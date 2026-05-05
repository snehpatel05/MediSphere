import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


APPOINTMENT_CHARGE = 100
EMERGENCY_FEE = 2000


class Person:
    def __init__(self, name, age, gender, phone):
        self.name = name
        self.age = int(age)
        self.gender = gender
        self.phone = phone


class Patient(Person):
    count = 1

    def __init__(self, name, age, gender, phone, patient_type):
        super().__init__(name, age, gender, phone)
        self.patient_id = "PAT" + str(Patient.count).zfill(3)
        Patient.count += 1
        self.patient_type = patient_type

    def room_charge(self):
        if self.patient_type == "Inpatient":
            return 1000
        return 0


class Doctor(Person):
    count = 1

    def __init__(self, name, age, gender, phone, illness, specialization, fee, doctor_type, slots):
        super().__init__(name, age, gender, phone)
        self.doctor_id = "DOC" + str(Doctor.count).zfill(3)
        Doctor.count += 1
        self.illness = illness
        self.specialization = specialization
        self.fee = float(fee)
        self.doctor_type = doctor_type
        self.slots = slots

    def calculate_fee(self):
        if self.doctor_type == "Specialist":
            return self.fee + 300
        return self.fee

    def availability(self):
        return ", ".join(self.slots)


class Appointment:
    count = 1

    def __init__(self, patient, doctor, illness, slot, date_time, reason):
        self.appointment_id = "APT" + str(Appointment.count).zfill(3)
        Appointment.count += 1
        self.patient = patient
        self.doctor = doctor
        self.illness = illness
        self.slot = slot
        self.date_time = date_time
        self.reason = reason
        self.status = "Booked"


class Bill:
    count = 1

    def __init__(self, patient, doctor, illness, slot, service_charge):
        self.bill_id = "BIL" + str(Bill.count).zfill(3)
        Bill.count += 1
        self.patient = patient
        self.doctor = doctor
        self.illness = illness
        self.slot = slot
        self.date = datetime.now().strftime("%d-%m-%Y")
        self.appointment_charge = APPOINTMENT_CHARGE
        self.doctor_fee = doctor.calculate_fee()
        self.room_charge = patient.room_charge()
        self.service_charge = float(service_charge)
        self.payment_status = "Paid"

    def total_amount(self):
        return self.appointment_charge + self.doctor_fee + self.room_charge + self.service_charge


class Hospital:
    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = []
        self.bills = []
        self.emergencies = []

    def add_patient(self, patient):
        self.patients[patient.patient_id] = patient

    def add_doctor(self, doctor):
        self.doctors[doctor.doctor_id] = doctor


class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MediSphere")
        self.root.geometry("1000x600")
        self.root.configure(bg="#e8f5f2")

        self.hospital = Hospital()
        self.set_style()
        self.create_gui()
        self.load_sample_data()

    def set_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10), padding=5, background="#26a69a")
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"), background="#b2dfdb")
        style.configure("TNotebook", background="#e8f5f2")
        style.configure("TNotebook.Tab", font=("Arial", 10), padding=6)

    def create_gui(self):
        title = tk.Label(
            self.root,
            text="MediSphere",
            font=("Arial", 22, "bold"),
            bg="#00796b",
            fg="white",
            pady=12
        )
        title.pack(fill="x")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=12)

        self.patient_tab = ttk.Frame(self.tabs)
        self.doctor_tab = ttk.Frame(self.tabs)
        self.bill_tab = ttk.Frame(self.tabs)
        self.emergency_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.patient_tab, text="Patients")
        self.tabs.add(self.doctor_tab, text="Doctors")
        self.tabs.add(self.bill_tab, text="Appointments and Bills")
        self.tabs.add(self.emergency_tab, text="Emergency Need")

        self.patient_page()
        self.doctor_page()
        self.bill_page()
        self.emergency_page()

    def input_box(self, parent, text, row):
        tk.Label(parent, text=text, bg="white").grid(row=row, column=0, padx=8, pady=6, sticky="w")
        entry = ttk.Entry(parent, width=32)
        entry.grid(row=row, column=1, padx=8, pady=6)
        return entry

    def combo_box(self, parent, text, row):
        tk.Label(parent, text=text, bg="white").grid(row=row, column=0, padx=8, pady=6, sticky="w")
        combo = ttk.Combobox(parent, state="readonly", width=30)
        combo.grid(row=row, column=1, padx=8, pady=6)
        return combo

    def patient_page(self):
        form = tk.Frame(self.patient_tab, bg="white", padx=12, pady=12)
        form.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form, text="Add Patient", bg="white", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=8)

        self.p_name = self.input_box(form, "Name", 1)
        self.p_age = self.input_box(form, "Age", 2)
        self.p_phone = self.input_box(form, "Phone", 3)

        self.p_gender = self.combo_box(form, "Gender", 4)
        self.p_gender["values"] = ["Male", "Female", "Other"]
        self.p_gender.set("Male")

        self.p_type = self.combo_box(form, "Type", 5)
        self.p_type["values"] = ["Outpatient", "Inpatient"]
        self.p_type.set("Outpatient")

        ttk.Button(form, text="Add Patient", command=self.add_patient).grid(row=6, column=0, columnspan=2, pady=12)

        columns = ("ID", "Name", "Age", "Gender", "Type", "Phone")
        self.patient_table = ttk.Treeview(self.patient_tab, columns=columns, show="headings")

        for col in columns:
            self.patient_table.heading(col, text=col)
            self.patient_table.column(col, width=110, anchor="center")

        self.patient_table.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def doctor_page(self):
        tk.Label(self.doctor_tab, text="Available Doctors", font=("Arial", 14, "bold")).pack(pady=10)

        columns = ("ID", "Name", "Illness", "Specialization", "Fee", "Slots", "Phone")
        self.doctor_table = ttk.Treeview(self.doctor_tab, columns=columns, show="headings")

        for col in columns:
            self.doctor_table.heading(col, text=col)
            self.doctor_table.column(col, width=130, anchor="center")

        self.doctor_table.pack(fill="both", expand=True, padx=10, pady=10)

    def bill_page(self):
        form = tk.Frame(self.bill_tab, bg="white", padx=12, pady=12)
        form.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form, text="Appointment / Bill", bg="white", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=8)

        self.patient_combo = self.combo_box(form, "Patient", 1)
        self.illness_combo = self.combo_box(form, "Illness", 2)
        self.doctor_combo = self.combo_box(form, "Doctor", 3)
        self.slot_combo = self.combo_box(form, "Select Slot", 4)

        self.illness_combo.bind("<<ComboboxSelected>>", self.update_doctor_combo)
        self.doctor_combo.bind("<<ComboboxSelected>>", self.update_slot_combo)

        self.date_entry = self.input_box(form, "Date", 5)
        self.date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))

        self.reason_entry = self.input_box(form, "Reason", 6)

        ttk.Button(form, text="Book Appointment", command=self.book_appointment).grid(row=7, column=0, columnspan=2, pady=10)

        self.service_entry = self.input_box(form, "Service Charge", 8)
        self.service_entry.insert(0, "0")

        ttk.Button(form, text="Generate Bill", command=self.generate_bill).grid(row=9, column=0, columnspan=2, pady=10)

        middle = tk.Frame(self.bill_tab)
        middle.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.output = tk.Text(middle, font=("Consolas", 10), width=55)
        self.output.pack(fill="both", expand=True)

        qr_frame = tk.Frame(self.bill_tab, bg="white", padx=10, pady=10)
        qr_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(qr_frame, text="Appointment Payment", bg="white", font=("Arial", 12, "bold")).pack(pady=5)

        self.qr_canvas = tk.Canvas(qr_frame, width=150, height=150, bg="white")
        self.qr_canvas.pack(pady=5)
        self.draw_qr_code()

        tk.Label(qr_frame, text="Scan to Pay\nAppointment Fee\n100 RUPEES", bg="white", font=("Arial", 10, "bold"), justify="center").pack(pady=8)

    def emergency_page(self):
        form = tk.Frame(self.emergency_tab, bg="white", padx=15, pady=15)
        form.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form, text="Emergency Need", bg="white", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=8)

        self.e_patient_combo = self.combo_box(form, "Patient", 1)
        self.e_illness_combo = self.combo_box(form, "Emergency", 2)
        self.e_doctor_combo = self.combo_box(form, "Doctor", 3)

        self.e_ambulance_combo = self.combo_box(form, "Ambulance", 4)
        self.e_ambulance_combo["values"] = ["No", "Yes"]
        self.e_ambulance_combo.set("No")

        self.e_illness_combo.bind("<<ComboboxSelected>>", self.update_emergency_doctors)

        ttk.Button(form, text="Confirm Emergency", command=self.confirm_emergency).grid(row=5, column=0, columnspan=2, pady=12)

        self.emergency_output = tk.Text(self.emergency_tab, font=("Consolas", 10), width=65)
        self.emergency_output.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.emergency_output.insert(tk.END, "Emergency service is available 24 x 7.\n")
        self.emergency_output.insert(tk.END, "Emergency Fee: Rs. " + str(EMERGENCY_FEE) + "\n")

    def draw_qr_code(self):
        size = 10
        pattern = [
            "111111100101111", "100000101001001", "101110101111101",
            "101110100010101", "101110111010101", "100000101010001",
            "111111101010111", "000000001100000", "110101111011101",
            "010011001000101", "111001111110111", "100100010010001",
            "101111011011101", "100001001000101", "111111101111111"
        ]
    
        for row in range(len(pattern)):
            for col in range(len(pattern[row])):
                if pattern[row][col] == "1":
                    x = col * size
                    y = row * size
                    self.qr_canvas.create_rectangle(x, y, x + size, y + size, fill="black", outline="black")

    def load_sample_data(self):
        patients = [
            Patient("Rahul Sharma", 21, "Male", "9876543210", "Outpatient"),
            Patient("Ananya Verma", 19, "Female", "9123456780", "Outpatient"),
            Patient("Amit Kumar", 45, "Male", "9988776655", "Inpatient"),
            Patient("Priya Singh", 32, "Female", "9090909090", "Inpatient")
        ]

        doctors = [
            Doctor("Ramesh Mehta", 50, "Male", "9000011111", "Fever", "General Medicine", 500, "General", ["9 AM", "10 AM", "11 AM"]),
            Doctor("Pooja Nair", 36, "Female", "9000066666", "Fever", "General Medicine", 550, "General", ["12 PM", "1 PM", "2 PM"]),
            Doctor("Neha Kapoor", 38, "Female", "9000022222", "Cold", "ENT", 600, "General", ["10 AM", "11 AM", "12 PM"]),
            Doctor("Farhan Ali", 47, "Male", "9000099999", "Cold", "ENT", 650, "General", ["3 PM", "4 PM", "5 PM"]),
            Doctor("Arjun Rao", 46, "Male", "9000033333", "Heart Problem", "Cardiology", 1000, "Specialist", ["2 PM", "3 PM", "4 PM"]),
            Doctor("Meera Shah", 39, "Female", "9000088888", "Heart Problem", "Cardiology", 1100, "Specialist", ["5 PM", "6 PM", "7 PM"]),
            Doctor("Sneha Iyer", 41, "Female", "9000044444", "Fracture", "Orthopedic", 900, "Specialist", ["11 AM", "12 PM", "1 PM"]),
            Doctor("Amit Batra", 48, "Male", "9000044445", "Fracture", "Orthopedic", 850, "Specialist", ["3 PM", "4 PM", "5 PM"]),
            Doctor("Karan Malhotra", 44, "Male", "9000055555", "Skin Problem", "Dermatology", 700, "Specialist", ["4 PM", "5 PM", "6 PM"]),
            Doctor("Isha Menon", 35, "Female", "9000000001", "Body Pain", "Physiotherapy", 500, "General", ["8 AM", "9 AM", "10 AM"]),
            Doctor("Vikram Joshi", 52, "Male", "9000077777", "Nerve Problem", "Neurology", 1200, "Specialist", ["3 PM", "4 PM", "5 PM"]),
            Doctor("Ritu Sharma", 34, "Female", "9000000002", "Child Care", "Pediatrics", 650, "General", ["9 AM", "10 AM", "11 AM"]),
            Doctor("Sanjay Gupta", 45, "Male", "9000000003", "Dental Problem", "Dental", 550, "General", ["5 PM", "6 PM", "7 PM"]),
            Doctor("Asha Jain", 40, "Female", "9000000004", "Pregnancy", "Gynecology", 800, "Specialist", ["12 PM", "1 PM", "2 PM"]),
            Doctor("Manish Roy", 43, "Male", "9000000005", "Dengue", "General Medicine", 600, "General", ["10 AM", "2 PM", "6 PM"]),
            Doctor("Divya Sethi", 37, "Female", "9000000006", "Dengue", "General Medicine", 650, "General", ["11 AM", "3 PM", "7 PM"])
        ]

        for p in patients:
            self.save_patient(p)

        for d in doctors:
            self.save_doctor(d)

        self.update_combos()

    def save_patient(self, patient):
        self.hospital.add_patient(patient)
        self.patient_table.insert("", tk.END, values=(
            patient.patient_id, patient.name, patient.age,
            patient.gender, patient.patient_type, patient.phone
        ))

    def save_doctor(self, doctor):
        self.hospital.add_doctor(doctor)
        self.doctor_table.insert("", tk.END, values=(
            doctor.doctor_id, "Dr. " + doctor.name, doctor.illness,
            doctor.specialization, doctor.calculate_fee(),
            doctor.availability(), doctor.phone
        ))

    def selected_id(self, combo):
        if combo.get() == "":
            return ""
        return combo.get().split(" - ")[0]

    def update_combos(self):
        patient_list = [p.patient_id + " - " + p.name for p in self.hospital.patients.values()]
        self.patient_combo["values"] = patient_list
        self.e_patient_combo["values"] = patient_list

        illnesses = []
        for d in self.hospital.doctors.values():
            if d.illness not in illnesses:
                illnesses.append(d.illness)

        self.illness_combo["values"] = illnesses
        self.e_illness_combo["values"] = illnesses

    def update_doctor_combo(self, event=None):
        illness = self.illness_combo.get()
        doctor_list = []

        for d in self.hospital.doctors.values():
            if d.illness == illness:
                doctor_list.append(d.doctor_id + " - Dr. " + d.name + " - Rs. " + str(d.calculate_fee()))

        self.doctor_combo["values"] = doctor_list
        self.doctor_combo.set("")
        self.slot_combo.set("")
        self.slot_combo["values"] = []

    def update_slot_combo(self, event=None):
        doctor_id = self.selected_id(self.doctor_combo)

        if doctor_id != "":
            self.slot_combo["values"] = self.hospital.doctors[doctor_id].slots
            self.slot_combo.set("")

    def update_emergency_doctors(self, event=None):
        illness = self.e_illness_combo.get()
        doctor_list = []

        for d in self.hospital.doctors.values():
            if d.illness == illness:
                doctor_list.append(d.doctor_id + " - Dr. " + d.name + " - Rs. " + str(d.calculate_fee()))

        self.e_doctor_combo["values"] = doctor_list
        self.e_doctor_combo.set("")

    def clear_boxes(self, boxes):
        for box in boxes:
            box.delete(0, tk.END)

    def add_patient(self):
        try:
            patient = Patient(
                self.p_name.get(), self.p_age.get(), self.p_gender.get(),
                self.p_phone.get(), self.p_type.get()
            )

            self.save_patient(patient)
            self.update_combos()
            self.clear_boxes([self.p_name, self.p_age, self.p_phone])

            messagebox.showinfo("Success", "Patient added successfully")

        except:
            messagebox.showerror("Error", "Please enter correct patient details")

    def book_appointment(self):
        patient_id = self.selected_id(self.patient_combo)
        doctor_id = self.selected_id(self.doctor_combo)
        illness = self.illness_combo.get()
        slot = self.slot_combo.get()

        if patient_id == "" or illness == "" or doctor_id == "" or slot == "":
            messagebox.showwarning("Missing", "Select patient, illness, doctor and slot")
            return

        patient = self.hospital.patients[patient_id]
        doctor = self.hospital.doctors[doctor_id]
        appointment = Appointment(patient, doctor, illness, slot, self.date_entry.get(), self.reason_entry.get())
        self.hospital.appointments.append(appointment)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "APPOINTMENT BOOKED\n")
        self.output.insert(tk.END, "-" * 40 + "\n")
        self.output.insert(tk.END, "Appointment ID : " + appointment.appointment_id + "\n")
        self.output.insert(tk.END, "Patient        : " + patient.name + "\n")
        self.output.insert(tk.END, "Illness        : " + illness + "\n")
        self.output.insert(tk.END, "Doctor         : Dr. " + doctor.name + "\n")
        self.output.insert(tk.END, "Doctor Fee     : Rs. " + str(doctor.calculate_fee()) + "\n")
        self.output.insert(tk.END, "Date           : " + appointment.date_time + "\n")
        self.output.insert(tk.END, "Slot           : " + slot + "\n")
        self.output.insert(tk.END, "Status         : " + appointment.status + "\n")
        self.output.insert(tk.END, "Appointment Fee: Rs. " + str(APPOINTMENT_CHARGE) + "\n")
        self.output.insert(tk.END, "Payment Status : Paid\n")

        messagebox.showinfo(
            "Appointment Successful",
            "Appointment booked successfully!\n\n"
            "Appointment ID: " + appointment.appointment_id + "\n"
            "Patient: " + patient.name + "\n"
            "Doctor: Dr. " + doctor.name + "\n"
            "Slot: " + slot
        )

    def make_bill_text(self, bill):
        return f"""
========================================
              MEDISPHERE
========================================

Bill ID        : {bill.bill_id}
Date           : {bill.date}

Patient ID     : {bill.patient.patient_id}
Patient Name   : {bill.patient.name}
Patient Type   : {bill.patient.patient_type}
Phone          : {bill.patient.phone}

Illness        : {bill.illness}
Doctor Name    : Dr. {bill.doctor.name}
Specialization : {bill.doctor.specialization}
Slot           : {bill.slot}

----------------------------------------
CHARGES
----------------------------------------
Appointment Fee: Rs. {bill.appointment_charge:.2f}
Doctor Fee     : Rs. {bill.doctor_fee:.2f}
Room Charge    : Rs. {bill.room_charge:.2f}
Service Charge : Rs. {bill.service_charge:.2f}
----------------------------------------
Total Amount   : Rs. {bill.total_amount():.2f}
Payment Status : {bill.payment_status}
----------------------------------------

Thank you for visiting MediSphere.
"""

    def generate_bill(self):
        patient_id = self.selected_id(self.patient_combo)
        doctor_id = self.selected_id(self.doctor_combo)
        illness = self.illness_combo.get()
        slot = self.slot_combo.get()

        if patient_id == "" or illness == "" or doctor_id == "" or slot == "":
            messagebox.showwarning("Missing", "Select patient, illness, doctor and slot")
            return

        try:
            patient = self.hospital.patients[patient_id]
            doctor = self.hospital.doctors[doctor_id]
            bill = Bill(patient, doctor, illness, slot, self.service_entry.get())
            self.hospital.bills.append(bill)

            bill_text = self.make_bill_text(bill)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, bill_text)

            file_name = bill.bill_id + "_" + patient.name.replace(" ", "_") + ".txt"
            path = filedialog.asksaveasfilename(
                title="Download Bill",
                defaultextension=".txt",
                initialfile=file_name,
                filetypes=[("Text Files", "*.txt")]
            )

            if path != "":
                file = open(path, "w")
                file.write(bill_text)
                file.close()
                messagebox.showinfo("Downloaded", "Bill downloaded successfully")

        except:
            messagebox.showerror("Error", "Please enter correct service charge")

    def confirm_emergency(self):
        patient_id = self.selected_id(self.e_patient_combo)
        doctor_id = self.selected_id(self.e_doctor_combo)
        illness = self.e_illness_combo.get()
        ambulance = self.e_ambulance_combo.get()

        if patient_id == "" or illness == "" or doctor_id == "":
            messagebox.showwarning("Missing", "Select patient, emergency and doctor")
            return

        patient = self.hospital.patients[patient_id]
        doctor = self.hospital.doctors[doctor_id]
        total = EMERGENCY_FEE + doctor.calculate_fee()

        self.hospital.emergencies.append([patient.name, illness, doctor.name, ambulance, total])

        self.emergency_output.delete("1.0", tk.END)
        self.emergency_output.insert(tk.END, "EMERGENCY REQUEST CONFIRMED\n")
        self.emergency_output.insert(tk.END, "-" * 40 + "\n")
        self.emergency_output.insert(tk.END, "Patient       : " + patient.name + "\n")
        self.emergency_output.insert(tk.END, "Emergency     : " + illness + "\n")
        self.emergency_output.insert(tk.END, "Doctor        : Dr. " + doctor.name + "\n")
        self.emergency_output.insert(tk.END, "Ambulance     : " + ambulance + "\n")
        self.emergency_output.insert(tk.END, "Emergency Fee : Rs. " + str(EMERGENCY_FEE) + "\n")
        self.emergency_output.insert(tk.END, "Doctor Fee    : Rs. " + str(doctor.calculate_fee()) + "\n")
        self.emergency_output.insert(tk.END, "Total Amount  : Rs. " + str(total) + "\n")
        self.emergency_output.insert(tk.END, "Status        : Urgent\n")

        messagebox.showinfo(
            "Emergency Confirmed",
            "Emergency request confirmed!\n\n"
            "Patient: " + patient.name + "\n"
            "Doctor: Dr. " + doctor.name + "\n"
            "Emergency Fee: Rs. " + str(EMERGENCY_FEE)
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()
