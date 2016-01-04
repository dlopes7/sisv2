import json
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


from bettersis.models import MonitorCPU, MonitorMemory, Sitescope, Host



def get_host_list(sitescope):
    for host in Host.objects.filter(sitescope=sitescope):
        yield host.name.lower()

def view_host_list(request):

    sitescope_name = request.GET['sitescope']
    sitescope = Sitescope.objects.get(name=sitescope_name)
    host_list = list(get_host_list(sitescope))

    return HttpResponse(json.dumps(host_list), content_type='application/javascript')

def chart(request):
    sitescope = Sitescope.objects.get(name='hp-sitescope001')
    host_list = list(get_host_list(sitescope))
    host_list.sort()

    metrics = ['Cpu', 'Memory']

    return render(request, 'chart.html', {'hosts': host_list,
                                          'metrics': metrics})

def json_chart(request):
    try:
        host = request.GET['host']
        metric = request.GET['metric']
        time_from = request.GET['time_from']
        time_to = request.GET['time_to']
        sitescope= request.GET['sitescope']

        time_from_formatted = datetime.strptime(time_from, "%d/%m/%Y %H:%M:%S")
        time_to_formatted = datetime.strptime(time_to, "%d/%m/%Y %H:%M:%S")

        sis = Sitescope.objects.get(name=sitescope)

        if metric == 'Cpu':
            monitors = MonitorCPU.objects.filter(host=host,
                                                 time__gt=time_from_formatted,
                                                 time__lt=time_to_formatted,
                                                 value__gt = 0,
                                                 ).order_by('time')
        elif metric == 'Memory':
            monitors = MonitorMemory.objects.filter(host=host,
                                                 time__gt=time_from_formatted,
                                                 time__lt=time_to_formatted,
                                                 value__gt = 0,
                                                 ).order_by('time')


        data = serializers.serialize('json',
                                     monitors,
                                     fields=('time', 'value'),
                                     )

    except KeyError as e:
        return HttpResponseBadRequest('Missing the parameter: ' + str(e))

    return HttpResponse(data, content_type='application/javascript')