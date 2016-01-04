import pprint
import re


def parse_memory(metrics):

    m = None
    exps = [
            re.compile(r'.* ([0-9]+)% physical memory used.*', re.M),
            ]

    for exp in exps:
        m = re.match(exp, metrics)
        if m:
            memory = float(m.group(1).replace(',', '.'))
            return {'memory': memory}

    if m is None:
        return {'memory': -1}

def parse_cpu(metrics):

    m = None
    exps = [
            re.compile(r'.*Processor\\_Total\\% Processor Time=([0-9]+,[0-9][0-9]).*', re.M),
            re.compile(r'^([0-9]+)% avg,', re.M)
            ]

    for exp in exps:
        m = re.match(exp, metrics)
        if m:
            cpu = float(m.group(1).replace(',', '.'))
            return {'cpu': cpu}

    if m is None:
        return {'cpu': -1}


def guess_event_type(event):

    monitor = event['monitor']



    #Sitescope001 -----------------------------------------------------
    #Memory
    if ('Memory on' in monitor
        #or 'Paging File Info' in monitor
        ):
        return 'memory'

    #Services
    elif ('Servicos Parados' in monitor):
        return 'services'

    #Disk
    elif ('Disk Utilization' in monitor or
         'Physical Disk' in monitor or
         'Logical Disk' in monitor):

        return 'disk'

    #CPU

    elif (#'Processor Info on' in monitor or
          'cpu monitor' in monitor.lower()):
        return 'cpu'

    elif ('Teste de Disponibilidade' in monitor):
        return 'wmi_test'

    elif ('IIS Monitor' in monitor or
         'Web Service Monitor' in monitor):
        return 'webserver'

    elif ('WMI Restart' in monitor):
        return 'wmi_restart'

    elif (monitor.startswith('WS - ')):
        return 'webservice'

    elif (monitor.startswith('Up/Down')):
        return 'ping'

    elif (monitor.startswith('Backup')):
        return 'backup'

    elif ('Tablespace_Usado' in monitor or
         'Processes Limit' in monitor or
         'Area Archive' in monitor or
          monitor.startswith('PROC') or
          'Temporary_Usage' in monitor or
          'InDoubt-Transaction' in monitor or
          'Objetos Invalidos' in monitor or
          'Jobs Interrompidos' in monitor or
          'Session Limit' in monitor or
          'Sessao em Lock' in monitor or
          'Session Limit' in monitor or
          'Archive' in monitor or
          'Archive' in monitor or
          'Archive' in monitor or
          'Archive' in monitor):
        return 'query'

    elif ('Monitor Load Checker' in monitor or
         'BAC Integration Statistics' in monitor):
        return 'sitescope'

    elif(monitor.startswith('Network Interface')):
        return 'network'


    elif ('Sitescope - Alteracao Alertas' in monitor):
        event_type = 'alert_modified'



    elif ('Trap Test' in monitor):
        return 'ignore'

    else:
        return 'unknown'

def get_corrected_metrics(event):
    if event['type'] == 'cpu':
        return parse_cpu(event['metrics'])

    if event['type'] == 'memory':
        return (parse_memory(event['metrics']))




def guess_host_name(event):
    monitor = event['monitor']
    m = None
    pattern = None
    host = None

    if (' on ' in monitor):
        pattern = re.compile(r'.* on (.*)')


    elif (' - Servicos Parados' in monitor):
        pattern = re.compile(r'(.*?) - Servicos')

    else:
        host = 'unknown'

    if pattern:
        m = re.match(pattern, monitor)
        if m:
            host = m.group(1).lower()

    return host




