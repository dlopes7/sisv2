from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


from bettersis.models import MonitorCPU, MonitorMemory



def get_host_list():
    for host in MonitorCPU.objects.values('host').distinct():
        yield host['host'].lower()


def chart(request):
    host_list = list(get_host_list())
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

        time_from_formatted = datetime.strptime(time_from, "%d/%m/%Y %H:%M:%S")
        time_to_formatted = datetime.strptime(time_to, "%d/%m/%Y %H:%M:%S")

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