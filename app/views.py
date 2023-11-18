from django.http import JsonResponse
from django.shortcuts import render
from .classes.compofform import Comparison_Of_Formulations
from .classes.workwithmodels import WorkWithModels as Wwm
from .models import Profession, NecessarySkill as NecS, NecessaryKnowledge as NecK
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return render(request, 'main/index.html')


def all_professions(request):
    profs = Profession.objects.order_by('professionName')
    return render(request, 'main/all_professions.html', {'profs': profs})


def profession(request):
    nameProf = request.GET.get('prof')
    current_profession = Wwm.get_profession_id_by_name(nameProf)
    necKnowledge, necSkills = Wwm.getSkillsKnowledge(current_profession.idProfession)

    return render(request, 'main/profession.html', {'prof': nameProf, 'skills': necSkills, 'knowledges': necKnowledge})


def comparison(request):
    if 'prof1' in request.GET and request.GET.get('prof1') != '' and 'prof2' in request.GET and request.GET.get(
            'prof2') != '':
        first_profession = request.GET.get('prof1')
        second_profession = request.GET.get('prof2')
        try:
            qs1 = Wwm.get_profession_id_by_name(first_profession)
            qs2 = Wwm.get_profession_id_by_name(second_profession)
        except ObjectDoesNotExist:
            return render(request, 'main/comparison.html',
                          {'error': True, 'prof1': first_profession, 'prof2': second_profession})

        necKnowledge1, necSkill1 = Wwm.getSkillsKnowledge(qs1.idProfession)
        necKnowledge2, necSkill2 = Wwm.getSkillsKnowledge(qs2.idProfession)

        compOfForm = Comparison_Of_Formulations()
        similarKnowledge, identicalKnowledge = compOfForm.find_similar_formulationsV1(necKnowledge1, necKnowledge2)

        similarSkills, identicalSkills = compOfForm.find_similar_formulationsV1(necSkill1, necSkill2)
        return render(request, 'main/result_comparison.html',
                      {"prof1": first_profession, "prof2": second_profession,
                       "identicalK": identicalKnowledge, "identicalS": identicalSkills,
                       "similarK": similarKnowledge, "similarS": similarSkills})

    if 'term' in request.GET:
        qs = Profession.objects.filter(professionName__icontains=request.GET.get('term'))
        professions = [prof.professionName for prof in qs]
        return JsonResponse(professions, safe=False)
    return render(request, 'main/comparison.html')


def find_similar(request):
    if 'similar' in request.GET and request.GET != "":
        compOfForm = Comparison_Of_Formulations()
        current_formulation: str = request.GET.get('similar')

        formulations = [knowledge.necKnowledgeName for knowledge in NecK.objects.all().order_by('necKnowledgeName')]
        similar_knowledge = compOfForm.find_similar_formulationsV2(current_formulation, formulations)
        all_prof_for_knowledge = [Wwm.get_dict_prof_nec(sk, False) for sk in similar_knowledge]

        formulations = [skill.necSkillName for skill in NecS.objects.all().order_by('necSkillName')]
        similar_skill = compOfForm.find_similar_formulationsV2(current_formulation, formulations)
        all_prof_for_skills = [Wwm.get_dict_prof_nec(ss, True) for ss in similar_skill]

        return render(request, 'main/result_find_similar.html',
                      {"similar": current_formulation.capitalize(), "similarS": all_prof_for_skills,
                       'similarK': all_prof_for_knowledge})

    return render(request, 'main/find_similar.html')
