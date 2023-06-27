from src.therapist import Therapist
from typing import List


class TherapistDB:
    def __init__(self):
        # TherapistDB:
        # { full_name_url1: Therapist1, full_name_url2: Therapist2,... }
        self.therapists = {}

    def add_therapist(self, therapist: Therapist):
        if self.therapists.get(therapist.full_name_url) is not None:
            raise Exception(f"Therapist {therapist.full_name} already exists")
        self.therapists[therapist.full_name_url] = therapist

    def update_therapist(self, therapist: Therapist):
        if self.therapists.get(therapist.full_name_url) is None:
            raise Exception(f"Therapist {therapist.full_name} does not exist")
        self.therapists[therapist.full_name_url] = therapist

    def delete_therapist(self, therapist: Therapist):
        if self.therapists.get(therapist.full_name_url) is None:
            raise Exception(f"Therapist {therapist.full_name} does not exist")
        del self.therapists[therapist.full_name_url]

    def get_therapist_list(self) -> List[str]:
        return [t.full_name for t in self.therapists.values()]

    def get_therapist_list_as_text(self):
        return "\n".join(self.get_therapist_list())

    def get_therapist_info(self, full_name_url):
        therapist = self.therapists.get(full_name_url)
        if therapist is None:
            raise Exception(f"Therapist {full_name_url} does not exist")
        return therapist.description

    def _get(self, full_name_url) -> Therapist:
        return self.therapists.get(full_name_url)

    def get_booking_available_time_single_day(self, full_name_url, day_of_week) -> List[str]:
        return self._get(full_name_url).get_booking_available_dates(day_of_week)