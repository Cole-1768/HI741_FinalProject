import csv
from src.patient_class import Patient
from src.provider_class import Provider
from src.department_class import Department
from src.encounter_class import Encounter
from src.procedure_class import Procedure
from src.note_class import Note

def load_data(patient_path, department_path, provider_path, encounter_path, procedure_path, note_path):
  
  ## Load patient data
  patient_lst = []
  with open(patient_path) as patient_f:
    reader = csv.DictReader(patient_f)
    for row in reader:
      patient = Patient( 
        row["patient_id"], 
        row) 
      patient_lst.append(patient) 
  patient_dict = {i.patient_id: i for i in patient_lst} 

  ## Load department data
  department_lst = []
  with open(department_path) as department_f:
    reader = csv.DictReader(department_f) 
    for row in reader:
      department = Department( 
        row["department_id"], 
        row["name"], 
        row["location"]) 
      department_lst.append(department) 
  department_dict = {i.department_id: i for i in department_lst} 
  
  ## Load provider data
  provider_lst = []
  with open(provider_path) as provider_f:
    reader = csv.DictReader(provider_f) 
    for row in reader:
      department = department_dict[row["department_id"]] 
      provider = Provider( 
        row["provider_id"], 
        row["name"], 
        row["specialty"], 
        department) 
      provider_lst.append(provider) 
      department.providers.append(provider) 
  provider_dict = {i.provider_id: i for i in provider_lst} 
  
  ## Load encounter data
  encounter_lst = []
  with open(encounter_path) as encounter_f:
    reader = csv.DictReader(encounter_f) 
    for row in reader:
      patient = patient_dict[row["patient_id"]] 
      provider = provider_dict[row["provider_id"]] 
      encounter = Encounter( 
        row["encounter_id"], 
        row["encounter_date"], 
        row["encounter_type"],
        patient, provider, provider.department)
      encounter_lst.append(encounter) 
      patient.encounters.append(encounter) 
      provider.encounters.append(encounter) 
      provider.department.encounters.append(encounter) 
  encounter_dict = {i.encounter_id: i for i in encounter_lst} 
    
  ## Load procedure data
  procedure_lst = []
  with open(procedure_path) as procedure_f:
    reader = csv.DictReader(procedure_f) 
    for row in reader:
      encounter = encounter_dict[row["encounter_id"]] 
      procedure = Procedure( 
        row["procedure_id"],
        row["procedure_code"],
        row["procedure_name"],
        row["cost"],
        encounter, encounter.provider)
      procedure_lst.append(procedure) 
      encounter.procedures.append(procedure) 
      encounter.provider.procedures.append(procedure) 
  procedure_dict = {i.procedure_id: i for i in procedure_lst} 
  
  ## Load notes data
  note_lst = []
  with open(note_path) as note_f:
    reader = csv.DictReader(note_f)
    for row in reader:
      encounter = encounter_dict[row["encounter_id"]]
      note = Note(
        row["note_id"],
        encounter,
        row["note_date"],
        row["note_text"]
      )
      note_lst.append(note)
      encounter.notes.append(note)
    
  ## Return all lists
  return patient_lst, department_lst, provider_lst, encounter_lst, procedure_lst, note_lst
      
