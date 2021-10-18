from rest_framework.views import APIView
from rest_framework.response import Response


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