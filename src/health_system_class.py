from collections import Counter
import csv
import random
from datetime import datetime

## Heath System Class

class Health_System:
  def __init__(self, patients, departments, providers, encounters, procedures, notes): # include all health system objects
    self.patients = patients
    self.departments = departments
    self.providers = providers
    self.encounters = encounters
    self.procedures = procedures
    self.notes = notes
    self.patient_dict = {p.patient_id: p for p in patients}
    self.provider_dict = {p.provider_id: p for p in providers}
    self.department_dict = {d.department_id: d for d in departments}
    self.encounter_dict = {e.encounter_id: e for e in encounters}
    self.notes_dict = {n.note_id: n for n in notes}
  
  def count_visits(self, patient_id, date):
    patient = self.patient_dict.get(patient_id)
    if patient is None:
      return None
    return patient.count_visits_by_date(date)
  
  def view_note(self, patient_id, date):
    patient = self.patient_dict.get(patient_id)
    if patient is None:
      return None
    matching_notes = []
    for encounter in patient.encounters:
      encounter_notes = encounter.get_notes_by_date(date)
      matching_notes.extend(encounter_notes)
    return matching_notes
  
  def retrieve_patient(self, patient_id):
    patient = self.patient_dict.get(patient_id)
    if patient is None:
      return None
    recent_encounter = patient.most_recent_encounter()
    return patient, recent_encounter
  
  def monitor_workload(self):
    workload = {}
    for provider in self.providers:
      workload[provider.name] = len(provider.encounters)
    ranked_workload = dict(
      sorted(
        workload.items(),
        key=lambda item: item[1],
        reverse=True
      )
    )
    return ranked_workload
  
  def monitor_revenue(self):
    revenue = {}
    for department in self.departments:
      total = 0
      for encounter in department.encounters:
        for procedure in encounter.procedures:
          total += float(procedure.cost)
      revenue[department.name] = round(total, 2)
    return revenue


  def is_valid_number(self, value):
    if value is None:
      return False
    if isinstance(value, str) and value.strip() == "":
      return False
    try:
      float(value)
      return True
    except ValueError:
      return False

  
  def gender_statistics(self):
    stats = {}
    for patient in self.patients:
      gender = patient.attributes["gender"]
      age_raw = patient.attributes["age"]
      bmi_raw = patient.attributes["bmi"]
      a1c_raw = patient.attributes["a1c"]
      if not (
        self.is_valid_number(age_raw) and
        self.is_valid_number(bmi_raw) and
        self.is_valid_number(a1c_raw)
      ):
        continue
      age = int(float(age_raw))
      bmi = float(bmi_raw)
      a1c = float(a1c_raw)
      if gender not in stats:
        stats[gender] = {
          "ages": [],
          "bmis": [],
          "a1cs": []
        }
      stats[gender]["ages"].append(age)
      stats[gender]["bmis"].append(bmi)
      stats[gender]["a1cs"].append(a1c)
    summary = {}
    for gender, values in stats.items():
      summary[gender] = {
        "avg_age": round(
          sum(values["ages"]) / len(values["ages"]), 2),
        "avg_bmi": round(
          sum(values["bmis"]) / len(values["bmis"]), 2),
        "avg_a1c": round(sum(values["a1cs"]) / len(values["a1cs"]), 2)
      }
    return summary
  
  
  def remove_patient(self, patient_id):
    found = False
    with open("data/patients.csv", "r") as f:
      reader = csv.DictReader(f)
      patient_rows = csv.DictReader(f)
      patient_rows = [
        row for row in reader
        if row["patient_id"] != patient_id
      ]
      if len(patient_rows) < len(self.patients):
        found = True
      with open("data/patients.csv", "w", newline="") as f:
        writer = csv.DictWriter(
          f,
          fieldnames = [
            "patient_id",
            "age",
            "gender",
            "bmi",
            "a1c",
            "bp_sys",
            "bp_dia",
            "smoking"
            ]
        )
        writer.writeheader()
        writer.writerows(patient_rows)
      with open("data/encounters.csv", "r") as f:
        reader = csv.DictReader(f)
        encounter_rows = [
          row for row in reader
          if row["patient_id"] != patient_id
        ]
      with open("data/encounters.csv", "w", newline = "") as f:
        writer = csv.DictWriter(
          f,
          fieldnames = [
            "encounter_id",
            "patient_id",
            "provider_id",
            "department_id",
            "encounter_date",
            "encounter_type"
          ]
        )
        writer.writeheader()
        writer.writerows(encounter_rows)
      with open("data/procedures.csv", "r") as f:
        reader = csv.DictReader(f)
        procedure_rows = [
          row for row in reader
          if row["patient_id"] != patient_id
        ]
        with open("data/procedures.csv", "w", newline = "") as f:
          writer = csv.DictWriter(
            f,
            fieldnames = [
              "procedure_id",
              "encounter_id",
              "patient_id",
              "procedure_code",
              "procedure_name",
              "cost"
            ]
          )
          writer.writeheader()
          writer.writerows(procedure_rows)
        with open("data/notes.csv", "r") as f:
          reader = csv.DictReader(f)
          note_rows = [
            row for row in reader
            if row["patient_id"] != patient_id
          ]
        with open("data/notes.csv", "w", newline = "") as f:
          writer = csv.DictWriter(
            f,
            fieldnames = [
              "note_id",
              "patient_id",
              "encounter_id",
              "note_date",
              "note_type",
              "note_text"
            ]
          )
          writer.writeheader()
          writer.writerows(note_rows)
        return found
  
  
  def add_patient_visit(self, data):
    patient_exists = (
      data["patient_id"] in self.patient_dict
    )
    if not patient_exists:
      with open("data/patients.csv", "a", newline = "") as f:
        writer = csv.writer(f)
        writer.writerow([
          data["patient_id"],
          data["age"],
          data["gender"],
          data["bmi"],
          data["a1c"],
          data["bp_sys"],
          data["bp_dia"],
          data["smoking"]
        ])
    encounter_id = (f"E{random.randint(10000, 99999)}")
    provider = self.provider_dict.get(data["provider_id"])
    department_id = provider.department.department_id
    with open("data/encounters.csv", "a", newline="") as f:
      writer = csv.writer(f)
      writer.writerow([
        encounter_id,
        data["patient_id"],
        data["provider_id"],
        department_id,
        data["encounter_date"],
        data["encounter_type"]
      ])
    note_id = (f"N{random.randint(10000, 99999)}")
    with open(
      "data/notes.csv", "a", newline = ""
    ) as f:
      writer = csv.writer(f)
      writer.writerow([
        note_id,
        data["patient_id"],
        encounter_id,
        data["encounter_date"],
        data["note_type"],
        data["note_text"]
      ])
    return True
  
  def log_activity(self, username, role, action, success):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
      timestamp,
      username,
      role,
      action,
      success
    ]
    with open("data/activity_log.csv", "a", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(row)
    
    
    
    
          
      
      
      
