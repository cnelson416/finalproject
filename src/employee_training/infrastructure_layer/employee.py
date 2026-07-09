"""Contains the definition for the Employee class."""

import json
from employee_training.infrastructure_layer.training import Training
from typing import List

class Employee():
    """Implements an Employee entity."""
    def __init__(self)->None:
        self.id:int = 0
        self.first_name:str = ""
        self.middle_name:str = ""
        self.last_name:str = ""
        self.birthday:str = ""
        self.gender:str = ""
        self.training:List[Training] = []


    def __str__(self)->str:
        return self.to_json()


    def __repr__(self)->str:
        return self.to_json()


    def to_json(self)->str:
        employee_dict = {}
        employee_dict['id'] = self.id
        employee_dict['first_name'] = self.first_name
        employee_dict['middle_name'] = self.middle_name
        employee_dict['last_name'] = self.last_name
        employee_dict['birthday'] = self.birthday
        employee_dict['gender'] = self.gender
        employee_dict['training'] = []

        for item in self.training:
            employee_dict['training'].append(item.__dict__)

        return json.dumps(employee_dict)