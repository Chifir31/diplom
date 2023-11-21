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


def add_data():
    add_professions()
    add_glf_contains_prof()
    add_glf_contains_func()
    add_lf_contains_knowledge()
    add_lf_contains_skill()
    add_nec_knowledge()
    add_nec_skill()


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
        add_data()
        cls.wwm = WorkWithModels()

    def test_get_profession_id_by_name(self):
        self.assertEqual(3, self.wwm.get_profession_id_by_name("Программист"))

    def test_get_all_knowledge(self):
        k = self.wwm.get_all_knowledge()
        self.assertTrue(len(k) == 1898)

    def test_get_all_skills(self):
        s = self.wwm.get_all_skills()
        self.assertTrue(len(s) == 1860)

    def test_getSkillsKnowledge(self):
        k, s = self.wwm.getKnowledgeSkills(27)
        self.assertTrue(len(k) == 12)
        self.assertTrue(len(s) == 10)

    def test_build_dict_prof_nec(self):
        dk1 = self.wwm.build_dict_prof_nec("Методики анализа рисков", False)
        self.assertEqual(dk1['form'], "Методики анализа рисков")
        self.assertTrue(len(dk1['profs']) > 0)

        ds1 = self.wwm.build_dict_prof_nec("Анализировать риски", True)
        self.assertEqual(ds1['form'], "Анализировать риски")
        self.assertTrue(len(ds1['profs']) > 0)


class IntegrationTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cls_atomics = cls._enter_atomics()
        add_data()
        cls.wwm = WorkWithModels()
        cls.cof = ComparisonOfFormulations()

    def test_find_similar_formulations_v1(self):
        k1, s1 = self.wwm.getKnowledgeSkills(2)
        k2, s2 = self.wwm.getKnowledgeSkills(3)
        sf, iff = self.cof.find_similar_formulations_v1(k1, k2)
        self.assertFalse(len(sf) == 0)
        self.assertFalse(len(iff) == 0)

        sf, iff = self.cof.find_similar_formulations_v1(s1, s2)
        self.assertFalse(len(sf) == 0)
        self.assertFalse(len(iff) == 0)

    def test_find_similar_formulations_v2(self):
        f = [knowledge.necKnowledgeName for knowledge in self.wwm.get_all_knowledge()]
        k = self.cof.find_similar_formulations_v2('СУБД', f)

        f = [skill.necSkillName for skill in self.wwm.get_all_skills()]
        s = self.cof.find_similar_formulations_v2('СУБД', f)

        self.assertFalse(len(k) == 0)
        self.assertFalse(len(s) == 0)


class ViewsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cls_atomics = cls._enter_atomics()
        add_data()

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_all_professions(self):
        response = self.client.get('/all_professions')
        self.assertEqual(response.status_code, 200)

    def test_profession(self):
        response = self.client.get('/profession?prof=Администратор%20БД')
        self.assertEqual(response.status_code, 200)

    def test_comparison(self):
        response = self.client.get('/comparison')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/comparison?term=пр')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/comparison?prof1=Программист&prof2=Техник-программист')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/comparison?prof1=Абракадабра&prof2=Потерялся')
        self.assertEqual(response.status_code, 200)

    def test_find_similar(self):
        response = self.client.get('/find_similar')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/find_similar?similar=Языки+программирования')
        self.assertEqual(response.status_code, 200)
