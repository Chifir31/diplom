from re import findall
from sentence_transformers import util, SentenceTransformer
from pymorphy2 import MorphAnalyzer
from torch import Tensor
from flashtext import KeywordProcessor
from nltk import snowball


Synonyms = {
    "испытание": ["тестирование", "проведение испытание", "натурные испытания"],
    "сбор данные": ["сбор информация"],
    "управление": ["управлять"],
    "метод": ["методика", "способ", "методология", "технология", "средство"],
    "бд": ["субд"],
    "программный продукт": ["программный обеспечение", "программный проект"],
    "программный система": ["интегрированный программный обеспечение"],
    "проверка": ["верификация"],
    "тестирование по": ["тестирование разработать по"],
    "ведение переговоры": ["проведение переговоры"],
    "управление проект": ["проектный управление", "менеджмент проект"],
    "правовой акт": ["локальный правовой акт", "нормативный правовой акт"],
    "отношение": ["взаимоотношение"],

    "использовать": ["применять"],
    "оценивать": ["производить оценка", "проводить оценка"],
    "анализировать риск": ["оценивать риск"],
    "проводить ": ["выполнять", "осуществлять", "производить", "осуществление"],
    "проводить интервью": ["проводить интервьюирование"],
    "входной дать": ["входной информация"],
    "составлять": ["подготавливать", "pазрабатывать", "документировать"],
    "документ": ["документация"],
    "выполнение": ["исполнение"],
    "строить прогноз": ["составлять прогноз"],
    "опрашивать": ["проводить опрос"],
    "контроль": ["контролировать"],
    "система управление версия": ["система контроль версия"],
    "безопасность информация": ["информационный безопасность"],
    "по": [" программного обеспечения"],
    "инфокоммуникационный": ["информационно коммуникационный"],
    "автоматизированный система": ["ИАС"],
    "понятие": ["содержание понятие"],
    "к файл и папка": ["на файл и папка"],
    "действовать стандарт": ["современный стандарт"],
    "локализовать": ["локализовывать"],
    "на основа": ["с использование"],
    "находить": ["вести поиск"]
}


class ComparisonOfFormulations:
    def __init__(self):
        self._cos_const = 0.95
        self._keyword_processor = KeywordProcessor()
        self._keyword_processor.add_keywords_from_dict(Synonyms)
        self._morph = MorphAnalyzer()
        self._snow_ball_stemmer = snowball.SnowballStemmer("russian")

    def _is_similar(self, lemmas_formulations1: list[str], lemmas_formulations2: list[str]) -> bool:
        if self._subset_check_v1(lemmas_formulations1, lemmas_formulations2):
            return True
        _formulation1 = self.__use_replace_keywords(lemmas_formulations1)
        _formulation2 = self.__use_replace_keywords(lemmas_formulations2)
        if self._subset_check_v1(_formulation1, _formulation2):
            return True
        return False

    def find_similar_formulations_v1(self, formulations1: dict[str, Tensor],
                                     formulations2: dict[str, Tensor]) -> [list[dict[str, str], list[str]]]:
        similar_formulations: list[tuple[str, str]] = []
        identical_formulations: list[str] = []
        for f1 in formulations1.items():
            _lemmas_formulation1 = self._preprocessing_with_pymorphy2(f1[0])
            for f2 in formulations2.items():
                if f1[0] != f2[0]:
                    if round(util.cos_sim(a=f1[1], b=f2[1]).item(), 2) >= self._cos_const:
                        lemmas_formulation1 = _lemmas_formulation1
                        lemmas_formulation2 = self._preprocessing_with_pymorphy2(f2[0])
                        if len(lemmas_formulation1) > len(lemmas_formulation2):
                            lemmas_formulation1 = lemmas_formulation2
                            lemmas_formulation2 = _lemmas_formulation1
                        if self._is_similar(lemmas_formulation1, lemmas_formulation2):
                            similar_formulations.append((f1[0], f2[0]))
                else:
                    if f1[0] not in identical_formulations:
                        identical_formulations.append(f1[0])
        update_similar_formulations = self.__get_similar_formulations(similar_formulations, identical_formulations)
        return update_similar_formulations, identical_formulations

    def find_similar_formulations_v2(self, formulation: str, formulations: list[str]) -> list[str]:
        similar_formulations = []
        lemmas_formulation_v1 = self._preprocessing_with_snowball(formulation)
        lemmas_formulation_v2 = self.__get_synonym(formulation)
        for formulation2 in formulations:
            _formulation2 = formulation2.lower()
            if self._subset_check_v2(lemmas_formulation_v1, _formulation2):
                similar_formulations.append(formulation2)
            else:
                if len(lemmas_formulation_v2) != 0:
                    if self._subset_check_v2(lemmas_formulation_v2, _formulation2) and \
                            formulation2 not in similar_formulations:
                        similar_formulations.append(formulation2)
        return similar_formulations

    def __get_synonym(self, formulation: str) -> list[str]:
        lemmas_formulation = self._preprocessing_with_pymorphy2(formulation)
        synonym = " ".join(self.__use_replace_keywords(lemmas_formulation))
        if synonym == " ".join(lemmas_formulation):
            return []
        return self._preprocessing_with_snowball(synonym)

    def __use_replace_keywords(self, lemmas_formulation: list[str]) -> list[str]:
        new_formulation: str = self._keyword_processor.replace_keywords(' '.join(lemmas_formulation))
        return new_formulation.split(" ")

    def _preprocessing_with_pymorphy2(self, formulation: str) -> list[str]:
        return [self._morph.normal_forms(word[0:len(word)])[0] for word in findall(r'\w+|\d+', formulation)]

    def _preprocessing_with_snowball(self, formulation: str) -> list[str]:
        return [self._snow_ball_stemmer.stem(word[0:len(word)]) for word in findall(r'\w+|\d+', formulation)]

    @staticmethod
    def _subset_check_v2(words: list[str], formulation: str) -> bool:
        for word in words:
            if formulation.find(word) == -1:
                return False
        return True

    @staticmethod
    def _subset_check_v1(short_formulation, long_formulation) -> bool:
        for formulation in short_formulation:
            if formulation not in long_formulation:
                return False
        return True

    @staticmethod
    def __get_similar_formulations(formulations: list[tuple[str, str]],
                                   identical_formulations: list[str]) -> list[dict[str, str]]:
        new_formulations = [{"form1": formulation12[0], "form2": formulation12[1]} for formulation12 in formulations
                            if formulation12[0] not in identical_formulations
                            and formulation12[1] not in identical_formulations]
        return new_formulations

    @staticmethod
    def get_formulation_with_embedding(formulations: list[str]):
        model = SentenceTransformer('cointegrated/rubert-tiny2')
        embeddings = model.encode(formulations)
        return {formulation: embedding for formulation, embedding in zip(formulations, embeddings)}

