from torch import Tensor

from ..models import Profession as Prof, GenFuncContainsFunc as GFContainsF,\
    GenLaborFuncContainsProf as GLFContainsP, LaborFuncContainsKnowledge as LFContainsK, \
    LaborFuncContainsSkill as LFContainsS, NecessarySkill as NecS, NecessaryKnowledge as NecK


class WorkWithModels:

    @staticmethod
    def get_profession_id_by_name(profession_name: str):
        return Prof.objects.get(nameProf=profession_name)

    @staticmethod
    def getSkillsKnowledge(idProf):
        idsGenLaborFunc = [p.idGenLaborFunc for p in GLFContainsP.objects.filter(idProfession=idProf)]
        idsLaborFunc = [p.idLaborFunc for p in GFContainsF.objects.filter(idGenLaborFunc__in=idsGenLaborFunc)]

        idsNecKnowledge = [p.idNecKnowledge for p in LFContainsK.objects.filter(idLaborFunc__in=idsLaborFunc)]
        FromNecKnowledge = NecK.objects.filter(idNecKnowledge__in=idsNecKnowledge).order_by('necKnowledgeName')
        necKnowledge = {p.necKnowledgeName: WorkWithModels.__get_embedding(p.embeddingKnowledge) for p in FromNecKnowledge}

        idsNecSkill = [p.idNecSkill for p in LFContainsS.objects.filter(idLaborFunc__in=idsLaborFunc)]
        FromNecSkill = NecS.objects.filter(idNecSkill__in=idsNecSkill).order_by('necSkillName')
        necSkills = {p.necSkillName: WorkWithModels.__get_embedding(p.embeddingSkill) for p in FromNecSkill}

        return necKnowledge, necSkills

    @staticmethod
    def get_professions(id_nec: int, isSkill: bool):
        if isSkill:
            idsLaborFunc = [kos.idLaborFunc for kos in LFContainsS.objects.filter(idNecSkill=id_nec)]
        else:
            idsLaborFunc = [kos.idLaborFunc for kos in LFContainsK.objects.filter(idNecKnowledge=id_nec)]

        idsGenLaborFunc = [fr.idGenLaborFunc for fr in GFContainsF.objects.filter(idLaborFunc__in=idsLaborFunc)]
        idsProfession = [fr.idProfession for fr in GLFContainsP.objects.filter(idGenLaborFunc__in=idsGenLaborFunc)]
        professions = [fr.nameProf for fr in Prof.objects.filter(idProf__in=idsProfession).order_by("nameProf")]

        return professions

    @staticmethod
    def __get_embedding(embedding_string: str):
        embedding = [float(e) for e in embedding_string.split(" ")]
        return Tensor(embedding)

    @staticmethod
    def get_dict_prof_nec(similar_nec, flag):
        if flag:
            profs = WorkWithModels.get_professions(int(NecS.objects.get(necSkillName=similar_nec)), flag)
        else:
            profs = WorkWithModels.get_professions(int(NecK.objects.get(necKnowledgeName=similar_nec)), flag)
        return {"form": similar_nec, "profs": profs}
