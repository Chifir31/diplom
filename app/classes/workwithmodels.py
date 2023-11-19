from torch import Tensor

from ..models import Profession as Prof, GenFuncContainsFunc as GFContainsF,\
    GenLaborFuncContainsProf as GLFContainsP, LaborFuncContainsKnowledge as LFContainsK, \
    LaborFuncContainsSkill as LFContainsS, NecessarySkill as NecS, NecessaryKnowledge as NecK


class WorkWithModels:

    @staticmethod
    def get_profession_id_by_name(profession_name: str):
        return Prof.objects.get(professionName=profession_name).idProfession

    @staticmethod
    def getSkillsKnowledge(id_profession: int):
        idsGenLaborFunc = [p.idGenLaborFunc for p in GLFContainsP.objects.filter(idProfession=id_profession)]
        idsLaborFunc = [p.idLaborFunc for p in GFContainsF.objects.filter(idGenLaborFunc__in=idsGenLaborFunc)]

        idsNecKnowledge = [p.idNecKnowledge for p in LFContainsK.objects.filter(idLaborFunc__in=idsLaborFunc)]
        FromNecKnowledge = NecK.objects.filter(idNecKnowledge__in=idsNecKnowledge).order_by('necKnowledgeName')
        necKnowledge = {p.necKnowledgeName: WorkWithModels.__get_embedding(p.embeddingKnowledge) for p in FromNecKnowledge}

        idsNecSkill = [p.idNecSkill for p in LFContainsS.objects.filter(idLaborFunc__in=idsLaborFunc)]
        FromNecSkill = NecS.objects.filter(idNecSkill__in=idsNecSkill).order_by('necSkillName')
        necSkills = {p.necSkillName: WorkWithModels.__get_embedding(p.embeddingSkill) for p in FromNecSkill}

        return necKnowledge, necSkills

    @staticmethod
    def get_professions(id_necessary: int, is_find_skills: bool) -> list[str]:
        if is_find_skills:
            idsLaborFunc = [kos.idLaborFunc for kos in LFContainsS.objects.filter(idNecSkill=id_necessary)]
        else:
            idsLaborFunc = [kos.idLaborFunc for kos in LFContainsK.objects.filter(idNecKnowledge=id_necessary)]

        idsGenLaborFunc = [fr.idGenLaborFunc for fr in GFContainsF.objects.filter(idLaborFunc__in=idsLaborFunc)]
        idsProfession = [fr.idProfession for fr in GLFContainsP.objects.filter(idGenLaborFunc__in=idsGenLaborFunc)]
        professions = [fr.professionName for fr in Prof.objects.filter(idProfession__in=idsProfession).order_by(
            "professionName")]

        return professions

    @staticmethod
    def __get_embedding(embedding_string: str):
        embedding = [float(e) for e in embedding_string.split(" ")]
        return Tensor(embedding)

    @staticmethod
    def build_dict_prof_nec(similar_necessary: str, is_for_skills: bool) -> dict[str, list[str]]:
        if is_for_skills:
            profs = WorkWithModels.get_professions(int(NecS.objects.get(necSkillName=similar_necessary)),
                                                   is_for_skills)
        else:
            profs = WorkWithModels.get_professions(int(NecK.objects.get(necKnowledgeName=similar_necessary)),
                                                   is_for_skills)
        return {"form": similar_necessary, "profs": profs}
