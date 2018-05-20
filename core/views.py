from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.shortcuts import render
import json
from django.core import serializers
import re
from .models import Kassa, Time



def show_data(request):

    return render(request, 'index.html', {

    })


def update(request):
    if request.method == "POST":
        data = []
        with open("C:/Users/fixen/Dropbox/Samberi/new.txt", 'r', encoding='utf-8') as file:
            for line in file:
                data.append(line)
        with open("C:/Users/fixen/Dropbox/Samberi/output2.txt", 'w', encoding='utf-8') as file:
            file.writelines(data)

        Time.objects.all().delete()
        date = data[0].strip()
        date_entry = Time.objects.create_time(date)

        kassas = []
        for idx, line in enumerate(data):
            if 'kassa' in line:
                info_start = idx
            if '>' in line:
                info_end = idx
                info = data[info_start:info_end + 1]
                kassas.append(info)

        dicts_lst = list()
        for kassa in kassas:
            kassa_dict = dict()
            person_counter = 0
            kassa_no = 0
            persons = "free"
            for line in kassa:
                if 'kassa' in line:
                    kassa_no = re.findall(r'\d+', line)
                    kassa_no = kassa_no[0]
                if 'person' in line:
                    person_counter += 1
            persons = person_counter
            if persons > 5:
                status = 'busy'
                kassa_entry = Kassa.objects.create_kassa(kassa_no, persons, status, date_entry)

        final_kassa = Kassa.objects.filter(kassa_date=date_entry)

        dicts = []
        for kassa in final_kassa:
            data_dict = dict(kassa=kassa.kassa_no, persons=kassa.persons, date=kassa.kassa_date.date,
                             status=kassa.status)
            dicts.append(data_dict)
        json_dict = dict(data=dicts)
        json_data = json.dumps(json_dict, indent=4)
        return HttpResponse(json_data)

    else:
        return JsonResponse({'status': 'failed'})

