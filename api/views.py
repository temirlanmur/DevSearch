from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions

from .serializers import ProjectSerializer, ReviewSerializer
from projects.models import Project, Review


class Routes(APIView):

    def get(self, request):
        routes = [
            {'GET': '/api/projects'},
            {'GET': '/api/projects/id'},
            {'POST': '/api/projects/id/vote'},

            {'POST': '/api/users/token'},
            {'POST': '/api/users/token/refresh'},
        ]
        return Response(routes)


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectRetrieve(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'project_id'


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return Review.objects.filter(owner=user, project=project)
    
    def perform_create(self, serializer):
        user = self.request.user.profile
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        value = self.request.data['value']
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post')
        elif project.owner == user:
            raise ValidationError('You cannot review your own project')
        else:
            serializer.save(
                owner=user,
                project=project,
                value=value
            )
            project.update_vote_count()