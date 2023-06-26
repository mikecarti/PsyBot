from src.therapist import Therapist
from typing import List


class TherapistDB:
    def __init__(self):
        # TherapistDB:
        # { full_name1: Therapist1, full_name2: Therapist2,... }
        self.therapists = {}

    def add_therapist(self, therapist: Therapist):
        if self.therapists.get(therapist.full_name) is not None:
            raise Exception(f"Therapist {therapist.full_name} already exists")
        self.therapists[therapist.full_name] = therapist

    def update_therapist(self, therapist: Therapist):
        if self.therapists.get(therapist.full_name) is None:
            raise Exception(f"Therapist {therapist.full_name} does not exist")
        self.therapists[therapist.full_name] = therapist

    def delete_therapist(self, therapist: Therapist):
        if self.therapists.get(therapist.full_name) is None:
            raise Exception(f"Therapist {therapist.full_name} does not exist")
        del self.therapists[therapist.full_name]

    def get_therapist_list(self) -> List[str]:
        return list(self.therapists.keys())

    def get_therapist_list_as_text(self):
        return "\n".join(self.get_therapist_list())

    def get_therapist_info(self, full_name):
        return self._get(full_name).description

    def _get(self, full_name):
        return self.therapists.get(full_name)