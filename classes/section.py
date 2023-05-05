from typing import Dict

from TAScheduler.models import Lab as LabModel
from classes import account, course


def create_section(name: str, course_object: course.Course):
    if LabModel.objects.filter(lab_name=name).exists():
        return None

    new_section_model = LabModel.objects.create(
        course_id=course_object.course_model,
        lab_name=name
    )
    return Section(new_section_model)


def delete_section(lab_id):
    try:
        lab_object = LabModel.objects.get(id=lab_id)
        lab_object.delete()
        return True
    except LabModel.DoesNotExist:
        return False


def __has_required_fields(data: Dict[str, any]):
    required_fields = {"lab_name"}
    return required_fields.issubset(data.keys())


class Section:
    def __init__(self, lab_model: LabModel):
        self.lab_model = lab_model
        self.course_model = self.lab_model.course_id

    def get_course_name(self):
        return self.course_model.course_name

    def get_lab_name(self):
        return self.lab_model.lab_name

    def get_ta(self):
        ta_id = self.course_model.instructor_id
        ta = account.get_account_by_id(ta_id)
        return ta

    def set_ta(self, ta: account.Account):
        self.course_model.instructor_id = ta.get_primary_key()
        self.course_model.save()
