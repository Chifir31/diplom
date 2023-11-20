from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe

from .classes.compofform import ComparisonOfFormulations
from .classes.workwithmodels import WorkWithModels as Wwm
from .models import Profession, NecessarySkill as NecS, NecessaryKnowledge as NecK
from django.core.exceptions import ObjectDoesNotExist


@require_safe
def index(request):
    return render(request, 'main/index.html')


@require_safe
def all_professions(request):
    profs = Profession.objects.order_by('professionName')
    return render(request, 'main/all_professions.html', {'profs': profs})


@require_safe
def profession(request):
    nameProf = request.GET.get('prof')
    current_profession = Wwm.get_profession_id_by_name(nameProf)
    necKnowledge, necSkills = Wwm.getKnowledgeSkills(current_profession)

    return render(request, 'main/profession.html', {'prof': nameProf, 'skills': necSkills, 'knowledges': necKnowledge})


@require_safe
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

        necKnowledge1, necSkill1 = Wwm.getKnowledgeSkills(qs1)
        necKnowledge2, necSkill2 = Wwm.getKnowledgeSkills(qs2)

        compOfForm = ComparisonOfFormulations()
        similarKnowledge, identicalKnowledge = compOfForm.find_similar_formulations_v1(necKnowledge1, necKnowledge2)

        similarSkills, identicalSkills = compOfForm.find_similar_formulations_v1(necSkill1, necSkill2)
        return render(request, 'main/result_comparison.html',
                      {"prof1": first_profession, "prof2": second_profession,
                       "identicalK": identicalKnowledge, "identicalS": identicalSkills,
                       "similarK": similarKnowledge, "similarS": similarSkills})

    if 'term' in request.GET:
        qs = Profession.objects.filter(professionName__icontains=request.GET.get('term'))
        professions = [prof.professionName for prof in qs]
        return JsonResponse(professions, safe=False)
    return render(request, 'main/comparison.html')


@require_safe
def find_similar(request):
    if 'similar' in request.GET and request.GET != "":
        compOfForm = ComparisonOfFormulations()
        current_formulation: str = request.GET.get('similar')

        formulations = [knowledge.necKnowledgeName for knowledge in Wwm.get_all_knowledge()]
        similar_knowledge = compOfForm.find_similar_formulations_v2(current_formulation, formulations)
        all_prof_for_knowledge = [Wwm.build_dict_prof_nec(sk, False) for sk in similar_knowledge]

        formulations = [skill.necSkillName for skill in Wwm.get_all_skills()]
        similar_skill = compOfForm.find_similar_formulations_v2(current_formulation, formulations)
        all_prof_for_skills = [Wwm.build_dict_prof_nec(ss, True) for ss in similar_skill]

        return render(request, 'main/result_find_similar.html',
                      {"similar": current_formulation.capitalize(), "similarS": all_prof_for_skills,
                       'similarK': all_prof_for_knowledge})

    return render(request, 'main/find_similar.html')
