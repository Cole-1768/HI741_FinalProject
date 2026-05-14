### Department Class

class Department:
    def __init__(self, department_id, name, location):
        self.department_id = department_id
        self.name = name
        self.location = location
        self.providers = []
        self.encounters = []
    def count_encounters(self):
        return len(self.encounters)
      
