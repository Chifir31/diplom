import json
from django.test import TestCase
from ..classes.workwithmodels import WorkWithModels as Wwm
from ..models import Profession, GenLaborFuncContainsProf, GenFuncContainsFunc, LaborFuncContainsKnowledge, \
    LaborFuncContainsSkill, NecessarySkill, NecessaryKnowledge


def add_professions():
    with open('app/tests/data/tblprofession.json', 'rb') as f:
        for d in json.load(f):
            Profession(idProfession=d['idProfession'], professionName=d['professionName']).save()


def add_glf_contains_prof():
    with open('app/tests/data/tblgenfunccontainsprof.json', 'rb') as f:
        for d in json.load(f):
            GenLaborFuncContainsProf(idContainsProf=d['idContainsProf'], idGenLaborFunc=d['idGenLaborFunc'],
                                     idProfession=d['idProfession']).save()


def add_glf_contains_func():
    with open('app/tests/data/tblgenfunccontainsfunc.json', 'rb') as f:
        for d in json.load(f):
            GenFuncContainsFunc(idContainsFunc=d['idContainsFunc'], idGenLaborFunc=d['idGenLaborFunc'],
                                idLaborFunc=d['idLaborFunc']).save()


def add_lf_contains_knowledge():
    with open('app/tests/data/tbllaborfunccontainsknowledge.json', 'rb') as f:
        for d in json.load(f):
            LaborFuncContainsKnowledge(idContainsKnowledge=d['idContainsKnowledge'], idNecKnowledge=d['idNecKnowledge'],
                                       idLaborFunc=d['idLaborFunc']).save()


def add_lf_contains_skill():
    with open('app/tests/data/tbllaborfunccontainsskill.json', 'rb') as f:
        for d in json.load(f):
            LaborFuncContainsSkill(idContainsSkill=d['idContainsSkill'], idNecSkill=d['idNecSkill'],
                                   idLaborFunc=d['idLaborFunc']).save()


def add_nec_knowledge():
    with open('app/tests/data/tblnecessaryknowledge.json', 'rb') as f:
        for d in json.load(f):
            NecessaryKnowledge(idNecKnowledge=d['idNecKnowledge'], necKnowledgeName=d['necKnowledgeName'],
                               embeddingKnowledge=d['embeddingKnowledge']).save()


def add_nec_skill():
    with open('app/tests/data/tblnecessaryskill.json', 'rb') as f:
        for d in json.load(f):
            NecessarySkill(idNecSkill=d['idNecSkill'], necSkillName=d['necSkillName'],
                               embeddingSkill=d['embeddingSkill']).save()


# Create your tests here.
class TestCase1(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cls_atomics = cls._enter_atomics()
        add_professions()
        add_glf_contains_prof()
        add_glf_contains_func()
        add_lf_contains_knowledge()
        add_lf_contains_skill()
        add_nec_knowledge()
        add_nec_skill()

    def test_first(self):
        print(Profession.objects.filter())
        print(GenLaborFuncContainsProf.objects.filter())
        print(GenFuncContainsFunc.objects.filter())
        print(LaborFuncContainsKnowledge.objects.filter())
        print(LaborFuncContainsSkill.objects.filter())
        print(NecessaryKnowledge.objects.filter())
        print(NecessarySkill.objects.filter())
