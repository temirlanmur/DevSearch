from django.views import View
from django.http.response import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from .models import Message, Profile, User
from .forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm
from .utils import paginate_profiles, search_profiles


def login_user(request):
    if request.user.is_authenticated:
        return redirect('users:account')
    redirect_to = request.GET.get('next', '')
    redirect_url = request.POST.get('redirect_url', '')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, f'Logged in as {user.profile.name}')
            if redirect_url:
                return redirect(redirect_url)
            return redirect('users:account')
        else:
            messages.error(request, 'Username or password is incorrect')
        
    return render(request, 'users/login.html', {
        'redirect_to': redirect_to
    })


def logout_user(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('users:profiles')


def register_user(request):
    form = CustomUserCreationForm()

    if request.user.is_authenticated:
        return redirect('users:account')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Registration has been successful')
            login(request, user)
            return redirect('users:account')
        else:
            messages.error(request, 'An error has occurred during registration')

    return render(request, 'users/register.html', {
        'form': form
    })


class ProfileList(View):
    page_kwarg = 'page'
    paginate_by = 6
    page_range = 2
    template_name = 'users/profile_list.html'

    def get(self, request):
        profiles, search_query = search_profiles(request)
        paginator, page, custom_range, prev_url, next_url = paginate_profiles(
            request, profiles, self.page_kwarg, self.paginate_by, self.page_range) 
        return render(request, self.template_name, {
            'search_query': search_query,
            'paginator': paginator,
            'profile_list': page,
            'is_paginated': page.has_other_pages(),
            'next_page_url': next_url,
            'previous_page_url': prev_url,
            'custom_range': custom_range
        })


class ProfileDetail(View):
    model = Profile
    template_name = 'users/profile_detail.html'

    def get(self, request, id):
        profile = get_object_or_404(self.model, id=id)
        top_skills = profile.skills.exclude(description__iexact='')
        other_skills = profile.skills.filter(description__iexact='')        
        context = {
            'profile': profile,
            'top_skills': top_skills,
            'other_skills': other_skills            
        }
        return render(request, self.template_name, context)


class ProfileAccount(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/account.html'

    def get(self, request):
        profile = request.user.profile
        return render(request, self.template_name, {
            'profile': profile
        })


class UpdateProfile(LoginRequiredMixin, View):
    login_url = 'users:login'
    form_class = ProfileForm
    template_name = 'users/profile_update.html'

    def get(self, request):
        form = self.form_class(instance=request.user.profile)
        return render(request, self.template_name, {
            'form': form
        })
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated')
            return redirect('users:account')
        return render(request, self.template_name, {
            'form': form
        })


class CreateSkill(LoginRequiredMixin, View):
    login_url = 'users:login'
    form_class = SkillForm
    template_name = 'users/skill_form.html'
    create_flag = True

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class(),
            'create_flag': self.create_flag
        })

    def post(self, request):
        form = SkillForm(request.POST)
        profile = request.user.profile
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill has been added')
            return redirect('users:account')
        return render(request, self.template_name, {
            'form': form,
            'create_flag': self.create_flag
        })


class UpdateSkill(LoginRequiredMixin, View):
    login_url = 'users:login'
    form_class = SkillForm
    template_name = 'users/skill_form.html'

    def get(self, request, id):
        profile = request.user.profile
        queryset = profile.skills.filter(id=id)
        if queryset:
            skill = queryset[0]
        else:
            return HttpResponseForbidden()
        form = self.form_class(instance=skill)
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, id):        
        profile = request.user.profile
        skill = profile.skills.get(id=id)
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():            
            skill.save()
            messages.success(request, 'Skill has been updated')
            return redirect('users:account')
        return render(request, self.template_name, {
            'form': form
        })


class DeleteSkill(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/skill_confirm_delete.html'

    def get(self, request, id):
        profile = request.user.profile
        queryset = profile.skills.filter(id=id)
        if queryset:
            skill = queryset[0]
        else:
            return HttpResponseForbidden()
        return render(request, self.template_name, {
            'skill': skill
        })
    
    def post(self, request, id):
        profile = request.user.profile
        skill = profile.skills.get(id=id)
        skill.delete()
        messages.success(request, 'Skill has been deleted')
        return redirect('users:account')


class Inbox(LoginRequiredMixin, View):
    login_url = 'users:login'
    template_name = 'users/inbox.html'

    def get(self, request):
        profile = request.user.profile
        messages_list = profile.incoming_messages.all()
        unread_count = messages_list.filter(is_read=False).count()
        return render(request, self.template_name, {
            'messages_list': messages_list,
            'unread_count': unread_count
        })


class MessageDetail(LoginRequiredMixin, View):
    login_url = 'users:login'
    model = Message
    template_name = 'users/message_detail.html'

    def get(self, request, id):
        profile = request.user.profile
        message = profile.incoming_messages.get(id=id)
        if not message.is_read:
            message.is_read = True
            message.save()
        return render(request, self.template_name, {
            'message': message
        })


class CreateMessage(View):
    form_class = MessageForm
    template_name = 'users/message_form.html'

    def get(self, request, id):
        recipient = get_object_or_404(Profile, id=id)
        form = self.form_class()
        return render(request, self.template_name, {
            'recipient': recipient,
            'form': form
        })
    
    def post(self, request, id):
        if request.user.is_authenticated:
            sender = request.user.profile
        else:
            sender = None
        recipient = get_object_or_404(Profile, id=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Message has been sent')
            return redirect(recipient)

        return render(request, self.template_name, {
            'recipient': recipient,
            'form': form
        })