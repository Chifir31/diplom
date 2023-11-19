import json
from django.test import TestCase
from ..classes.workwithmodels import WorkWithModels
from ..classes.compofform import ComparisonOfFormulations
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
    """
    Функция заполняет таблицу tblLaborFuncContainsSkill в БД
    """
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
class ComparisonOfFormulationsTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cls_atomics = cls._enter_atomics()
        cls.cof = ComparisonOfFormulations()

    def test_find_similar_formulations_v1(self):
        first_formulations = ["Языки, утилиты и среды программирования, средства пакетного выполнения процедур",
                              "Интерфейсы взаимодействия внутренних модулей программного проекта"]
        second_formulations = ["Языки, утилиты и среды программирования, средства пакетного выполнения процедур",
                               "Интерфейсы взаимодействия внутренних модулей программного продукта"]
        ff = self.cof.get_formulation_with_embedding(first_formulations)
        sf = self.cof.get_formulation_with_embedding(second_formulations)
        s, i = self.cof.find_similar_formulations_v1(ff, sf)
        true_s = [{"form1": "Интерфейсы взаимодействия внутренних модулей программного проекта",
                   "form2": "Интерфейсы взаимодействия внутренних модулей программного продукта"}]
        true_i = ["Языки, утилиты и среды программирования, средства пакетного выполнения процедур"]
        self.assertEqual(s, true_s)
        self.assertEqual(i, true_i)

    def test_find_similar_formulations_v2(self):
        s = self.cof.find_similar_formulations_v2("Методы коммуникаций",
                                                  ["Методы коммуникации и что-то там еще",
                                                   "Средства коммуникаций и что-то там еще"])
        self.assertEqual(s, ["Методы коммуникации и что-то там еще"])


class WorkWithModelsTestCase(TestCase):

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
        cls.wwm = WorkWithModels()

    def test_get_profession_id_by_name(self):
        self.assertEqual(3, self.wwm.get_profession_id_by_name("Программист"))
