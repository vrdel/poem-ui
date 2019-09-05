from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import status


from Poem.helpers.versioned_comments import new_comment
from Poem.poem_super_admin.models import Probe, ExtRevision
from Poem.poem.saml2.config import tenant_from_request, saml_login_string, get_schemaname

from reversion.models import Version, Revision

from .views import NotFound

from Poem import settings

import datetime
import json

from Poem.api.internal_views.aggregationprofiles import *
from Poem.api.internal_views.app import *
from Poem.api.internal_views.apikey import *
from Poem.api.internal_views.groupelements import *
from Poem.api.internal_views.metricprofiles import *
from Poem.api.internal_views.metrics import *
from Poem.api.internal_views.probes import *
from Poem.api.internal_views.services import *
from Poem.api.internal_views.users import *


class GetConfigOptions(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request):
        options = dict()

        tenant = tenant_from_request(request)
        options.update(saml_login_string=saml_login_string(tenant))

        options.update(webapimetric=settings.WEBAPI_METRIC)
        options.update(webapiaggregation=settings.WEBAPI_AGGREGATION)
        options.update(tenant_name=tenant)

        return Response({'result': options})


class Saml2Login(APIView):
    authentication_classes = (SessionAuthentication,)
    keys = ['username', 'first_name', 'last_name', 'is_superuser']

    def _prefix(self, keys):
        return ['{}_saml2_'.format(get_schemaname()) + key for key in keys]

    def _remove_prefix(self, keys):
        new_keys = dict()

        for k, v in keys.items():
            new_keys[k.split('{}_saml2_'.format(get_schemaname()))[1]] = v

        return new_keys

    def get(self, request):
        result = cache.get_many(self._prefix(self.keys))

        return Response(self._remove_prefix(result))

    def delete(self, request):
        cache.delete_many(self._prefix(self.keys))

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListProbeVersionInfo(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, probekey):
        try:
            version = Version.objects.get(id=probekey)
            data = json.loads(version.serialized_data)[0]['fields']

            return Response(data)

        except Version.DoesNotExist:
            raise NotFound(status=404, detail='Probe version not found')


class ListVersions(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, obj, name):
        models = {'probe': Probe}

        try:
            obj = models[obj].objects.get(name=name)
            ct = ContentType.objects.get_for_model(obj)
            vers = Version.objects.filter(object_id=obj.id,
                                          content_type_id=ct.id)

            results = []
            for ver in vers:
                rev = Revision.objects.get(id=ver.revision_id)
                comment = new_comment(rev.comment, obj_id=obj.id,
                                      version_id=ver.id, ctt_id=ct.id)

                results.append(dict(
                    id=ver.id,
                    object_repr=ver.object_repr,
                    fields=json.loads(ver.serialized_data)[0]['fields'],
                    user=json.loads(ver.serialized_data)[0]['fields']['user'],
                    date_created=datetime.datetime.strftime(
                        rev.date_created, '%Y-%m-%d %H:%M:%S'
                    ),
                    comment=comment,
                    version=json.loads(ver.serialized_data)[0]['fields']['version']
                ))

            results = sorted(results, key=lambda k: k['id'], reverse=True)
            return Response(results)

        except Version.DoesNotExist:
            raise NotFound(status=404, detail='Version not found')
