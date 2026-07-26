"""Contains the definition for the Grant class."""

import json

class Grant():
    """Implements a Grant entity."""

    def __init__(self)->None:
        self.id:int = 0
        self.grant_name:str = ""
        self.grant_number:str = ""
        self.funding_agency:str = ""
        self.funding_amount:str = ""
        self.start_date:str = ""
        self.end_date:str = ""

    def __str__(self)->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()

    def to_json(self)->str:
        grant_dict = {}
        grant_dict['id'] = self.id
        grant_dict['grant_name'] = self.grant_name
        grant_dict['grant_number'] = self.grant_number
        grant_dict['funding_agency'] = self.funding_agency
        grant_dict['funding_amount'] = self.funding_amount
        grant_dict['start_date'] = self.start_date
        grant_dict['end_date'] = self.end_date
        grant_dict['investigators'] = []
        for investigator in self.investigators:
            grant_dict['investigator'].append(investigator.__dict__)
        return json.dumps(grant_dict)

    def is_valid(self)->bool:
        valid = False
        if len(self.grant_name) > 0 \
            and len(self.grant_number) > 0 \
            and len(self.funding_agency) > 0 \
            and len(self.funding_amount) > 0 \
            and len(str(self.start_date)) > 0 \
            and len(str(self.end_date)) > 0:
            valid = True
        return valid