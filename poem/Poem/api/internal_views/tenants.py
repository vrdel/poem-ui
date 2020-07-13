import datetime

from Poem.api.internal_views.utils import get_tenant_resources
from Poem.tenants.models import Tenant
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from tenant_schemas.utils import get_public_schema_name


class ListTenants(APIView):
    authentication_classes = (SessionAuthentication,)

    def get(self, request, name=None):
        if name:
            try:
                if name == 'SuperPOEM_Tenant':
                    tenant = Tenant.objects.get(
                        schema_name=get_public_schema_name()
                    )
                    tenant_name = 'SuperPOEM Tenant'
                    metric_key = 'metric_templates'
                else:
                    tenant = Tenant.objects.get(name=name)
                    tenant_name = tenant.name
                    metric_key = 'metrics'

                data = get_tenant_resources(tenant.schema_name)
                results = dict(
                    name=tenant_name,
                    schema_name=tenant.schema_name,
                    domain_url=tenant.domain_url,
                    created_on=datetime.date.strftime(
                        tenant.created_on, '%Y-%m-%d'
                    ),
                    nr_metrics=data[metric_key],
                    nr_probes=data['probes']
                )

            except Tenant.DoesNotExist:
                return Response(
                    {'detail': 'Tenant not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            results = []
            tenants = Tenant.objects.all()

            for tenant in tenants:
                if tenant.schema_name == get_public_schema_name():
                    tenant_name = 'SuperPOEM Tenant'
                else:
                    tenant_name = tenant.name

                results.append(dict(
                    name=tenant_name,
                    schema_name=tenant.schema_name,
                    domain_url=tenant.domain_url,
                    created_on=datetime.date.strftime(tenant.created_on, '%Y-%m-%d')
                ))

            results = sorted(results, key=lambda k: k['name'].lower())

        return Response(results)
