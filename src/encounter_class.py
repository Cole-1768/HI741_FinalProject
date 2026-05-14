from datetime import datetime

### Encounter Class

class Encounter:
    def __init__(self, encounter_id, date, encounter_type,
                 patient, provider, department):
        self.encounter_id = encounter_id
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.encounter_type = encounter_type
        self.patient = patient
        self.provider = provider
        self.department = department
        self.notes = []
        self.procedures = []
    
    def get_notes_by_date(self, date):
        matching_notes = []
        for note in self.notes:
            if note.date == date:
                matching_notes.append(note)
        return matching_notes
