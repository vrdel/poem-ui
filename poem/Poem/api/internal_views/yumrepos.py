from Poem.poem_super_admin.models import YumRepo

from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView


class ListYumRepos(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, name=None):
        if name:
            try:
                repo = YumRepo.objects.get(name=name)
                result = {
                    'id': repo.id,
                    'name': repo.name,
                    'description': repo.description
                }
                return Response(result)

            except YumRepo.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            repos = YumRepo.objects.all()

            results = []
            for repo in repos:
                results.append(
                    {
                        'id': repo.id,
                        'name': repo.name,
                        'description': repo.description
                    }
                )

            results = sorted(results, key=lambda k: k['name'].lower())

            return Response(results)
