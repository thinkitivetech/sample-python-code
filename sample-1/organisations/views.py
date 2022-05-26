import json

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render


@login_required
def list(request):
    url = "http://localhost:8000/api/organisations/"
    result = requests.get(url, params=request.GET)
    context = {}
    if result.status_code == 200:
        organisations_list = json.loads(result.text)
        p = Paginator(organisations_list, 3)
        page = request.GET.get("page")
        organisations = p.get_page(page)
        context["organisations"] = organisations
        context["data_exist"] = True
    else:
        context["data_exist"] = False
        messages.error(request, "Can't fetch the data, Retry!")
    return render(request, "organisations/list.html", context)


@login_required
def report(request, organisation_id):
    url = "http://localhost:8000/api/organisations/" + organisation_id
    result = requests.get(url, params=request.GET)
    context = {}
    if result.status_code == 200:
        context["organisation"] = json.loads(result.text)
    return render(request, "organisations/report.html", context)
