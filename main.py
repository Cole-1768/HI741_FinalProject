from src.ui import HospitalUI
from src.data_loader import load_data
from src.health_system_class import Health_System

def main():

  patient_path = "data/patients.csv"
  department_path = "data/departments.csv"
  provider_path = "data/providers.csv"
  encounter_path = "data/encounters.csv"
  procedure_path = "data/procedures.csv"
  notes_path = "data/notes.csv"

  patients, departments, providers, encounters, procedures, notes = load_data( # load all objects
    patient_path,
    department_path,
    provider_path,
    encounter_path,
    procedure_path,
    notes_path)

  hs = Health_System( # create Health System
    patients, 
    departments, 
    providers, 
    encounters, 
    procedures,
    notes)

  HospitalUI(hs)

if __name__ == "__main__":
    main()
