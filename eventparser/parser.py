import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sisv2.settings")

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from datetime import datetime, timedelta
import django
import time

from eventparser.utils import guess_event_type, guess_host_name, get_corrected_metrics
from bettersis.models import MonitorCPU, Sitescope, MonitorMemory


django.setup()

def create_monitor_model(event):
    id = str(event['time']).replace(' ', '').replace('-', '').replace(':', '') + event['group'] + event['id'].replace(':', '')
    if event['type'] == 'cpu':
        new_event, created = MonitorCPU.objects.get_or_create(_id = id,
                                                     name = event['monitor'],
                                                     state = event['state'],
                                                     time = event['time'],
                                                     value=event['metrics']['cpu'],
                                                     sitescope=Sitescope.objects.get(name=event['sitescope']),
                                                     host=event['host'])
        new_event.save()

    elif event['type'] == 'memory':
        new_event, created = MonitorMemory.objects.get_or_create(_id = id,
                                                     name = event['monitor'],
                                                     state = event['state'],
                                                     time = event['time'],
                                                     value=event['metrics']['memory'],
                                                     sitescope=Sitescope.objects.get(name=event['sitescope']),
                                                     host=event['host'])
        new_event.save()


def process_events(sitescope, date):
    time_format = '%H:%M:%S %m/%d/%Y'

    col_time, col_status, col_group_id =  0, 1, 2
    col_monitor_name, col_metrics, col_id =  3, 4, 5


    caminho_log = r'\\{sis_address}\logs\SiteScope{year}_{month}_{day}.log'.format(sis_address=sitescope.address,
                                                                        day = str(date.day).zfill(2),
                                                                        month = str(date.month).zfill(2),
                                                                        year = date.year)

    num_line = 0
    num_new = 0


    try:
        oldest_event = max(MonitorCPU.objects.all().order_by('-id')[0].time,
                           MonitorMemory.objects.all().order_by('-id')[0].time)
    except IndexError:
        oldest_event = None



    with open(caminho_log, 'r', encoding="utf8") as arquivo:
        for line in arquivo:
            num_line +=1

            line_array = line.split('\t')[:6]
            event_date = datetime.strptime(line_array[col_time], time_format)


            if event_date < oldest_event:
                continue

            num_new += 1

            if len(line_array) == 6:
                line_struct = {'time': event_date,
                               'state': line_array[col_status],
                               'id': line_array[col_id],
                               'monitor': line_array[col_monitor_name],
                               'metrics': line_array[col_metrics],
                               'sitescope': sitescope.name,
                               'group': line_array[col_group_id]}

                line_struct['type'] = guess_event_type(line_struct)
                line_struct['host'] = guess_host_name(line_struct)

                line_struct['metrics'] = get_corrected_metrics(line_struct)

                create_monitor_model(line_struct)
    print('{date}: {num_events} processed. {num_news} inserted.'.format(date=datetime.now(),
                                                                        num_events=num_line,
                                                                        num_news=num_new))


if __name__ == '__main__':
    sitescopes = [
                  'hp-sitescope001',
                  #'hp-sitescope002',
                  #'hp-sitescope003',
                  #'hp-sitescope004',
                  #'hp-sitescope005',
                 ]

    while True:
        for sitescope in sitescopes:
            sis_address = '{sis}.dc.nova'.format(sis=sitescope)
            sis_model, created = Sitescope.objects.get_or_create(name=sitescope, address=sis_address)

            start_date = datetime.now()
            end_date = datetime.now()

            difference = (end_date - start_date).days

            for single_date in (start_date + timedelta(n) for n in range(difference+1)):
                print('{date}: Processing {day}'.format(date=datetime.now(),
                                                        day=single_date))
                process_events(sis_model, single_date)

        time.sleep(5 * 60)




