### Patient Class

class Patient:
  def __init__(self, patient_id, attributes):
    self.patient_id = patient_id
    self.attributes = attributes
    self.encounters = []
  
  def count_visits_by_date(self, date):
    count = 0
    for encounter in self.encounters:
      if encounter.date == date:
        count += 1
    return count

  def most_recent_encounter(self):
    if len(self.encounters) == 0:
      return None
    return max(
      self.encounters,
      key = lambda encounter: encounter.date    
    )
