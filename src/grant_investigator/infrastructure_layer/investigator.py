"""Contains the definition for the Investigator class."""

import json
from grant_investigator.infrastructure_layer.grant import Grant
from typing import List

class Investigator():
    """Implement an Investigator entity."""
    def __init__(self)->None:
        self.id:int = 0
        self.first_name:str = ""
        self.last_name:str = ""
        self.email:str = ""
        self.institution:str = ""
        self.grants:List[Grant] = []

    def __str__(self)->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()


    def to_json(self)->str:
        investigator_dict = {}
        investigator_dict['id'] = self.id
        investigator_dict['first_name'] = self.first_name
        investigator_dict['last_name'] = self.last_name
        investigator_dict['email'] = self.email
        investigator_dict['institution'] = self.institution
        investigator_dict['grants'] = []
        for grant in self.grants:
            investigator_dict['grant'].append(grant.__dict__)
        return json.dumps(investigator_dict)

    def is_valid(self)->bool:
        valid = False
        if len(self.first_name) > 0 \
            and len(self.last_name) > 0 \
            and len(str(self.email)) > 0 \
            and len(self.institution) > 0:
            valid = True
        return valid