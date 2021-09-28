from django.views import View
from django.http.response import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import paginate_projects, search_projects


class ProjectList(View):
    page_kwarg = 'page'
    paginate_by = 6
    page_range = 2
    template_name = 'projects/project_list.html'

    def get(self, request):
        projects, search_query = search_projects(request)
        paginator, page, custom_range, prev_url, next_url = paginate_projects(
            request, projects, self.page_kwarg, self.paginate_by, self.page_range) 

        return render(request, self.template_name, {
            'search_query': search_query,
            'paginator': paginator,
            'project_list': page,
            'is_paginated': page.has_other_pages(),
            'next_page_url': next_url,
            'previous_page_url': prev_url,
            'custom_range': custom_range
        })


class ProjectDetail(View):
    model = Project
    form_class = ReviewForm
    template_name = 'projects/project_detail.html'

    def get(self, request, id):
        project = get_object_or_404(self.model, id=id)
        form = self.form_class()
        return render(request, self.template_name, {
            'project': project,
            'form': form
        })

    def post(self, request, id):
        project = get_object_or_404(self.model, id=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.update_vote_count()
            messages.success(request, 'Review has been submitted')
            return redirect(project)


class CreateProject(LoginRequiredMixin, View):
    login_url = 'users:login'
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    create_flag = True
    
    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'create_flag': self.create_flag
        })

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        profile = request.user.profile
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project has been created')
            return redirect(project)
        
        return render(request, self.template_name, {
            'form': form,
            'create_flag': self.create_flag
        })


class UpdateProject(LoginRequiredMixin, View):
    login_url = 'users:login'
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    
    def get(self, request, id):
        profile = request.user.profile
        queryset = profile.projects.filter(id=id)
        if queryset:
            project = queryset[0]
        else:
            return HttpResponseForbidden()
        return render(request, self.template_name, {
            'project': project,
            'form': self.form_class(instance=project)
        })

    def post(self, request, id):
        project = get_object_or_404(self.model, id=id)
        form = self.form_class(request.POST, request.FILES, instance=project)        
        if form.is_valid():
            project = form.save()
            messages.success(request, 'Project has been updated')
            return redirect(project)
        
        return render(request, self.template_name, {
            'project': project,
            'form': form
        })


class DeleteProject(LoginRequiredMixin, View):
    login_url = 'users:login'
    model = Project
    success_url = reverse_lazy('projects:projects')
    template_name = 'projects/project_confirm_delete.html'
    
    def get(self, request, id):
        profile = request.user.profile
        queryset = profile.projects.filter(id=id)
        if queryset:
            project = queryset[0]
        else:
            return HttpResponseForbidden()
        return render(request, self.template_name, {
            'project': project
        })

    def post(self, request, id):
        profile = request.user.profile
        project = profile.projects.get(id=id)
        project.delete()
        messages.success(request, 'Project has been deleted')
        return redirect(self.success_url)