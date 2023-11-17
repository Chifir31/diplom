from django.test import TestCase
from ..classes.workwithmodels import WorkWithModels as Wwm
from ..models import Profession


# Create your tests here.
class TestCase1(TestCase):
    def test_first(self):
        Profession.objects.create(nameProf="Программист", idProf=1)
        print(Profession.objects.get(idProf=1))
