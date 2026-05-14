from datetime import datetime

### Notes class

class Note:
  
  def __init__(self, note_id, encounter, date, text):
    self.note_id = note_id
    self.encounter = encounter
    self.date = datetime.strptime(date, "%Y-%m-%d").date()
    self.text = text
    
