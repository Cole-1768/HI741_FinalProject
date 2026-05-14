### Procedure Class

class Procedure:
    def __init__(self, procedure_id, procedure_code, procedure_name,
                 cost, encounter, provider):
        self.procedure_id = procedure_id
        self.procedure_code = procedure_code
        self.procedure_name = procedure_name
        self.cost = cost
        self.encounter = encounter
        self.provider = provider

        
