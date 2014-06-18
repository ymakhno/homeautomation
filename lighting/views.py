from datetime import time
import json
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.template.context import RequestContext
from lighting.models import Lighter, Rule, WebCamera
from lighting.zwave import ChangeLightLevel, UpdateZWaveStatus

def main(request):
    return redirect("index")

def index(request):
    template = loader.get_template("lighting/main.html")
    context = RequestContext(request, {
        'lighters' : Lighter.objects.all(),
        'rules' : Rule.objects.all()
    })
    return HttpResponse(template.render(context))

def lights(request):
    if request.method == 'GET' or request.method == 'POST':
        if request.method == 'POST':
            lighter = Lighter.objects.get(pk = request.POST["id"])
            ChangeLightLevel(lighter, int(request.POST["value"])).do()
            UpdateZWaveStatus().do()

        result = []
        for lighter in Lighter.objects.all():
            result.append([lighter.value > 0, lighter.value])
        return HttpResponse(json.dumps(result), content_type="application/json")

def delete_rule(request):
    Rule.objects.get(pk = int(request.GET["id"])).delete()
    return redirect("index")

def add_rule(request):
    rule = Rule(
        monday = request.POST["rule_mon"] == "true",
        tuesday = request.POST["rule_tue"] == "true",
        wednesday = request.POST["rule_wed"] == "true",
        thursday = request.POST["rule_thu"] == "true",
        friday = request.POST["rule_fri"] == "true",
        saturday = request.POST["rule_sat"] == "true",
        sunday = request.POST["rule_sun"] == "true",
        start = time(int(request.POST["rule_start_hour"]), int(request.POST["rule_start_min"])),
        start_delta = int(request.POST["rule_start_delta"]),
        end = time(int(request.POST["rule_end_hour"]), int(request.POST["rule_end_min"])),
        end_delta = int(request.POST["rule_end_delta"]),
        lighter = Lighter.objects.get(pk = int(request.POST["rule_lighter"]))
    )
    rule.save()
    return redirect("index")

def cameras(request):
    template = loader.get_template("lighting/cameras.html")
    context = RequestContext(request, {
        'cameras' : WebCamera.objects.all(),
    })
    return HttpResponse(template.render(context))