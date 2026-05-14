### Provider Class

class Provider:
    def __init__(self, provider_id, name, specialty, department=None):
        self.provider_id = provider_id
        self.name = name
        self.specialty = specialty
        self.department = department
        self.encounters = []
        self.procedures = []
    def count_encounters(self):
        return len(self.encounters)
