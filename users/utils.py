from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def paginateProfiles(request, profiles,result):

    page = request.GET.get('page')

    paginator = Paginator(profiles, result)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    left_index = (int(page) - 4)

    if left_index < 1:
            left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages +1

    custom_page = range(left_index,right_index)
    
    return custom_page, profiles 

def searchProfiles(request):

    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_info__icontains=search_query)|
         Q(skill__in=skills)   
         )
    return profiles , search_query