from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .models import Profile, Skill


def paginate_profiles(request, profiles, page_kwarg, paginate_by, page_range):
    paginator = Paginator(profiles, paginate_by)
    page_number = request.GET.get(page_kwarg)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = paginator.num_pages
    page = paginator.page(page_number)
            
    left_index = int(page_number) - page_range
    if left_index < 1:
        left_index = 1
    right_index = int(page_number) + page_range
    if right_index > paginator.num_pages + 1:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    prev_url = f'?{page_kwarg}={page.previous_page_number()}' if page.has_previous() else None
    next_url = f'?{page_kwarg}={page.next_page_number()}' if page.has_next() else None

    return paginator, page, custom_range, prev_url, next_url


def search_profiles(request):
    search_query = request.GET.get('search_query') or ''
    if search_query:
        skills = Skill.objects.filter(name__icontains=search_query)
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skills__in=skills))
    else:
        profiles = Profile.objects.all()
    return profiles, search_query