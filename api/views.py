from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import ProjectSerializer
from projects.models import Project


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
    