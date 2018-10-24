from django.shortcuts import render
from .models import ItemRank, ItemSite
from django.http import HttpResponse
from .excel_utils import WriteToExcel
from .forms import RankForm
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
from django.core import serializers

# Create your views here.

def test(request):
    return HttpResponse("HIHIHI")

def crawl_main(request):
    rk = ItemRank.objects.filter(keyword='샴푸').order_by('-stt_de', '-stt_tm', 'site', 'rk')
    return render(request, 'main_app/tables.html', {'rk':rk})

def crawl_main_c(request):
    rk = ItemRank.objects.filter(keyword='샴푸').order_by('-stt_de', '-stt_tm', 'site', 'rk')
    return render(request, 'main_app/charts.html', {'rk':rk})

def crawl_main_d(request):

    rk = ItemRank.objects.filter(keyword='샴푸', stt_de='20180903').order_by('-stt_de', '-stt_tm', 'site', 'rk')
    site = ItemSite.objects.all().order_by('keyword')
    keyword = None
    if request.method == 'POST':
        if 'excel' in request.POST:
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment;filename=excel.xlsx'
                kwd = request.POST.get('keyword' , None)
                startDate = request.POST.get('startDate', '').replace("-","",2)
                endDate = request.POST.get('endDate', '').replace("-","",2)
                rk = ItemRank.objects.filter(keyword=kwd, stt_de__range=(startDate, endDate)).order_by('-stt_de', '-stt_tm', 'site', 'rk')
                xlsx_data = WriteToExcel(rk, keyword)
                response.write(xlsx_data)
                return response
    else:
        form = RankForm()


    context = {
	'form': form,
	'rk': rk,
	'kwd': site,
    }

    return render(request, 'main_app/index.html', context)

@require_POST
def getJsonData(request):
    
    if request.method == 'POST':
        kwd = request.POST.get('keyword', None)
        startDate = request.POST.get('startDate', '')
        endDate = request.POST.get('endDate', '')
	
        data = ItemRank.objects.filter(stt_de__range=(startDate, endDate), keyword=kwd).order_by('-stt_de', '-stt_tm', 'site', 'rk').values()
        #print(data)
        #jsonData = serializers.serialize('json', data)
        #print(jsonData)
    context = {'jsonData' : data}
    return HttpResponse(json.dumps(list(data)), content_type='applicataion/json')
    #return HttpResponse(jsonData, content_type='application/json')
   

