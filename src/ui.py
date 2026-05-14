import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import random
from src.user_class import User

class HospitalUI:

  def __init__(self, health_system):
    self.hs = health_system
    self.root = tk.Tk()
    self.root.title("Hospital System")
    self.root.geometry("400x300")
    tk.Label(self.root, text="Username").pack(pady=5)
    self.username_entry = tk.Entry(self.root)
    self.username_entry.pack()
    tk.Label(self.root, text="Password").pack(pady=5)
    self.password_entry = tk.Entry(self.root, show="*")
    self.password_entry.pack()
    tk.Button(
      self.root,
      text="Login",
      command=self.login
    ).pack(pady=20)
    self.root.mainloop()
    
  def login(self):
    username = self.username_entry.get()
    password = self.password_entry.get()
    with open("data/credentials.csv") as file:
      reader = csv.DictReader(file)
      for row in reader:
        if row["username"] == username and row["password"] == password:
          role = row["role"]
          self.current_user = User(username, role)
          self.hs.log_activity(username, role, "LOGIN", "SUCCESS")
          self.show_menu()
          return
    self.hs.log_activity(username, "UNKNOWN", "LOGIN", "FAIL")  
    messagebox.showerror(
      "Login Failed",
      "Invalid username or password"
    )
  
  def show_menu(self):
    for widget in self.root.winfo_children():
      widget.destroy()
    tk.Label(
      self.root,
      text=f"Logged in as: {self.current_user.username} ({self.current_user.role})",
    ).pack(pady=10)
    # Nurse or clinician interface
    if self.current_user.role in ["nurse", "clinician"]:
      tk.Button(
        self.root,
        text="Retrieve Patient",
        command=self.retrieve_patient_ui
      ).pack(pady=5)
      tk.Button(
        self.root,
        text = "Add Patient",
        command=self.add_patient_ui
      ).pack(pady=5)
      tk.Button(
        self.root,
        text = "Remove Patient",
        command=self.remove_patient_ui
      ).pack(pady=5)
      tk.Button(
        self.root,
        text = "Count Visits",
        command = self.count_visits_ui
      ).pack(pady=5)
      tk.Button(
        self.root,
        text = "View Note",
        command = self.view_note_ui
      ).pack(pady=5)
    # Admin inferace
    elif self.current_user.role == "admin":
      tk.Button(
        self.root,
        text="Count Visits",
        command=self.count_visits_ui
      ).pack(pady=5)
      tk.Button(
        self.root,
        text="Monitor Workload",
        command=self.monitor_workload_ui
      ).pack(pady=5)
    # Management interface
    elif self.current_user.role == "management":
      tk.Button(
        self.root,
        text="Generate Statistics",
        command=self.generate_statistics_ui
      ).pack(pady=5)
      tk.Button(
        self.root,
        text="Monitor Revenue",
        command=self.monitor_revenue_ui
      ).pack(pady=5)
    # Exit button
    tk.Button(
      self.root,
      text="Exit",
      command=self.root.destroy
    ).pack(pady=20)
  
  
  def count_visits_ui(self):
    patient_id = simpledialog.askstring(
      "Patient ID",
      "Enter Patient ID:"
    )
    if patient_id is None:
      return
    date_str = simpledialog.askstring("Visit Date", "Enter date (YYYY-MM-DD):")
    if date_str is None:
      return
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    count = self.hs.count_visits(patient_id, date)
    # invalid patient
    if count is None:
      messagebox.showerror(
        "Error",
        "Patient ID not found."
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "COUNT_VISITS",
        "FAIL"
      )
      return
    messagebox.showinfo(
      "Visit Count",
      f"Patient {patient_id} had {count} visit(s) on {date}."
    )
    self.hs.log_activity(
      self.current_user.username,
      self.current_user.role,
      "COUNT_VISITS",
      "SUCCESS"
    )
    
    
  def view_note_ui(self):
    patient_id = simpledialog.askstring(
      "Patient ID",
      "Enter Patient ID:"
    )
    if patient_id is None:
      return
    date_str = simpledialog.askstring(
      "Date",
      "Enter Date (YYYY-MM-DD):"
    )
    if date_str is None:
      return
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    notes = self.hs.view_note(patient_id, date)
    if notes is None:
      messagebox.showerror(
        "Error",
        "Patient not found"
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "VIEW_NOTE",
        "FAIL"
      )
      return
    if len(notes) == 0:
      messagebox.showinfo(
        "No Notes",
        "No notes for that date"
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "VIEW_NOTE",
        "FAIL"
      )
      return
    note_text = ""
    for note in notes:
      note_text += (
        f"Note ID: {note.note_id}\n"
        f"{note.text}\n"
      )
    messagebox.showinfo(
      "Clinical Note",
      note_text
    )
    self.hs.log_activity(
      self.current_user.username,
      self.current_user.role,
      "VIEW_NOTE",
      "SUCCESS"
    )


  def retrieve_patient_ui(self):
    patient_id = simpledialog.askstring(
      "Retrieve Patient",
      "Enter Patient ID:"
    )
    if patient_id is None:
      return
    result = self.hs.retrieve_patient(patient_id)
    if result is None:
      messagebox.showerror(
        "Error",
        "Patient not found"
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "RETRIEVE_PATIENT",
        "FAIL"
      )
      return
    patient, encounter = result
    if encounter is None:
      messagebox.showinfo(
        "Patient Found",
        "Patient has no encounters"
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "RETRIEVE_PATIENT",
        "FAIL"
      )
      return
    patient_info = (
      f"Patient Information\n"
      f"Patient ID: {patient.patient_id}\n"
      f"Age: {patient.attributes['age']}\n"
      f"Gender: {patient.attributes['gender']}\n"
      f"BMI: {patient.attributes['bmi']}\n"
      f"A1C: {patient.attributes['a1c']}\n\n"
      f"Most Recent Encounter\n"
      f"Encounter ID: {encounter.encounter_id}\n"
      f"Date: {encounter.date}\n"
      f"Type: {encounter.encounter_type}\n"
      f"Provider: {encounter.provider.name}\n"
      f"Department: {encounter.department.name}"
    )
    messagebox.showinfo(
      "Patient Information",
      patient_info
    )
    self.hs.log_activity(
      self.current_user.username,
      self.current_user.role,
      "RETRIEVE_PATIENT",
      "SUCCESS"
    )
  
  def monitor_workload_ui(self):
    workload = self.hs.monitor_workload()
    output = ""
    for provider, count in workload.items():
      output += (
        f"{provider}: {count} encounters\n"
      )
    messagebox.showinfo(
      "Provider Workload",
      output
    )
    self.hs.log_activity(
      self.current_user.username,
      self.current_user.role,
      "MONITOR_WORKLOAD",
      "SUCCESS"
    )
    
    
  def monitor_revenue_ui(self):
    revenue = self.hs.monitor_revenue()
    output = ""
    for department, total in revenue.items():
      output += (
        f"{department}: ${total}\n"
      )
    messagebox.showinfo(
      "Department Revenue",
      output
    )
    self.hs.log_activity(
      self.current_user.username,
      self.current_user.role,
      "MONITOR_REVENUE",
      "SUCCESS"
    )
  
  
  def generate_statistics_ui(self):
    stats = self.hs.gender_statistics()
    genders = list(stats.keys())
    avg_ages = [
      stats[gender]["avg_age"]
      for gender in genders
    ]
    plt.figure(figsize=(6, 4))
    plt.bar(genders, avg_ages)
    plt.xlabel("Gender")
    plt.ylabel("Average Age")
    plt.title("Average Patient Age by Gender")
    plt.show()
    stats_text = ""
    for gender in genders:
      stats_text += (
        f"{gender}\n"
        f"Average BMI: "
        f"{stats[gender]['avg_bmi']}\n"
        f"Average A1C: "
        f"{stats[gender]['avg_a1c']}\n\n"
      )
    messagebox.showinfo(
      "Additional Statistics",
      stats_text
    )
    self.hs.log_activity(
      self.current_user.username,
      self.current_user.role,
      "GENERATE_STATISTICS",
      "SUCCESS"
    )
  
  
  def remove_patient_ui(self):
    patient_id = simpledialog.askstring(
      "Remove Patient",
      "Enter Patient ID:"
    )
    if patient_id is None:
      return
    success = self.hs.remove_patient(patient_id)
    if success:
      messagebox.showinfo(
        "Success",
        f"Patient {patient_id} removed"
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "REMOVE_PATIENT",
        "SUCCESS"
      )
    else:
      messagebox.showerror(
        "Error",
        "Patient ID not found"
      )
      self.hs.log_activity(
        self.current_user.username,
        self.current_user.role,
        "REMOVE_PATIENT",
        "FAIL"
      )
    

  def add_patient_ui(self):
    window = tk.Toplevel(self.root)
    window.title("Add Patient / Add Visit")
    window.geometry("400x700")
    tk.Label(window, text="Patient ID").pack()
    patient_id_entry = tk.Entry(window)
    patient_id_entry.pack()
    # Demographics
    tk.Label(window, text="Age").pack()
    age_entry = tk.Entry(window)
    age_entry.pack()
    tk.Label(window, text="Gender").pack()
    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(
        window,
        textvariable=gender_var,
        values=["Male", "Female", "Non-binary"]
    )
    gender_dropdown.pack()
    tk.Label(window, text="BMI").pack()
    bmi_entry = tk.Entry(window)
    bmi_entry.pack()
    tk.Label(window, text="A1C").pack()
    a1c_entry = tk.Entry(window)
    a1c_entry.pack()
    tk.Label(window, text="BP Systolic").pack()
    bp_sys_entry = tk.Entry(window)
    bp_sys_entry.pack()
    tk.Label(window, text="BP Diastolic").pack()
    bp_dia_entry = tk.Entry(window)
    bp_dia_entry.pack()
    smoking_var = tk.BooleanVar()
    tk.Checkbutton(
        window,
        text="Smoker",
        variable=smoking_var
    ).pack()
    # Encounter
    tk.Label(window, text="Encounter Date (YYYY-MM-DD)").pack()
    date_entry = tk.Entry(window)
    date_entry.pack()
    tk.Label(window, text="Encounter Type").pack()
    encounter_type_var = tk.StringVar()
    encounter_dropdown = ttk.Combobox(
        window,
        textvariable=encounter_type_var,
        values=["Outpatient", "Inpatient", "Emergency"]
    )
    encounter_dropdown.pack()
    tk.Label(window, text="Provider ID").pack()
    provider_var = tk.StringVar()
    provider_dropdown = ttk.Combobox(
        window,
        textvariable=provider_var,
        values=["PR1", "PR2", "PR3", "PR4", "PR5", "PR6", "PR7", "PR8", "PR9", "PR10",
        "PR11", "PR12", "PR13", "PR14", "PR15", "PR16", "PR17", "PR18", "PR19", "PR20"]
    )
    provider_dropdown.pack()
    # Note
    tk.Label(window, text="Clinical Note").pack()
    note_entry = tk.Entry(window, width=40)
    note_entry.pack()
    tk.Label(window, text="Note Type").pack()
    note_type_var = tk.StringVar()
    note_type_dropdown = ttk.Combobox(
      window,
      textvariable = note_type_var,
      values = ["Progress", "Discharge", "Consult", "Emergency", "Oncology", "Nursing"]
    )
    note_type_dropdown.pack()
    def submit():
      data = {
        "patient_id": patient_id_entry.get().strip(),
        "age": age_entry.get().strip(),
        "gender": gender_var.get().strip(),
        "bmi": bmi_entry.get().strip(),
        "a1c": a1c_entry.get().strip(),
        "bp_sys": bp_sys_entry.get().strip(),
        "bp_dia": bp_dia_entry.get().strip(),
        "smoking": smoking_var.get(),
        "encounter_date": date_entry.get().strip(),
        "encounter_type": encounter_type_var.get().strip(),
        "provider_id": provider_var.get().strip(),
        "note_type": note_type_var.get().strip(),
        "note_text": note_entry.get().strip()
      }
      success = self.hs.add_patient_visit(data)
      if success:
        messagebox.showinfo(
          "Success",
          f"Patient visit added successfully\n Restart program if you wish to update"
        )
        window.destroy()
        self.hs.log_activity(
          self.current_user.username,
          self.current_user.role,
          "ADD_PATIENT",
          "SUCCESS"
        )
      else:
        messagebox.showerror(
          "Error",
          "Patient can not be added"
        )
        self.hs.log_activity(
          self.current_user.username,
          self.current_user.role,
          "ADD_PATIENT",
          "FAIL"
        )
    tk.Button(
      window,
      text="Submit",
      command=submit
    ).pack(pady=15)
