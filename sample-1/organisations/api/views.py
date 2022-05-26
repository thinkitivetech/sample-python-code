from rest_framework import viewsets

from cyber_risk_web.organisations.models import Organisation, Report

from .serializers import OrganisationSerializer, ReportSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
