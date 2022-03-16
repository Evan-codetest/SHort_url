from django.shortcuts import render
from django.http import HttpResponse ,HttpResponseRedirect
from django.utils import timezone
from django.contrib.sessions.models import Session
from .models import Shorturl
from django.contrib import messages
from short import forms, models

import hashlib
import base64

from rest_framework import viewsets
from .serializers import Urlserializer

class Urlviewset(viewsets.ModelViewSet):
    queryset = Shorturl.objects.all().order_by('create_date')
    serializer_class = Urlserializer

# Create your views here.
Base_url = "http://127.0.0.1:8000/"
Base_count = 0
def short(url):
    url = base64.b64encode(
        hashlib.md5((url).encode('utf-8')).digest(), altchars=b"-_")[:6].decode("utf-8")
    return url

def index(request):
    global Base_count
    if request.POST:
        #print('index')
        form = forms.url_form(request.POST)
        if form.is_valid():
                get_url = request.POST.get('url_data')
                if models.Shorturl.objects.filter(original_url=get_url).exists():
                    res = models.Shorturl.objects.filter(original_url=get_url).first()
                    now = timezone.datetime.now().replace(tzinfo=None)
                    before = res.create_date.replace(tzinfo=None)
                    expire = now - before
                    if expire.days > 7:
                        date=timezone.now()
                        short_url = short(get_url+str(Base_count))
                        data = models.Shorturl.objects.create(short_url=short_url,original_url=get_url,create_date=date)
                        data.save()
                        Base_count +=1
                        #print('成功')
                        request.session['short_url'] = short_url
                        request.session['original_url'] = get_url
                        return HttpResponseRedirect('/result')                            
                    else:
                        short_url = res.short_url
                        original_url= res.original_url
                        request.session['short_url'] = short_url
                        request.session['original_url'] = get_url
                        return HttpResponseRedirect('/result')                    
                else:
                    date=timezone.now()
                    short_url = short(get_url+str(Base_count))
                    data = models.Shorturl.objects.create(short_url=short_url,original_url=get_url,create_date=date)
                    data.save()
                    Base_count +=1
                    #print('成功')
                    request.session['short_url'] = short_url
                    request.session['original_url'] = get_url
                    return HttpResponseRedirect('/result')
        else:
            get_url = False
            #print('False')
    else:
        form = forms.url_form()
    return render(request, 'index.html', locals())

def custom_url(request):
    if request.POST:
        #print('custom')
        form = forms.custom_form(request.POST)
        if form.is_valid():
            get_url = request.POST.get('url_data')
            word = request.POST.get('word')
            #print(word)
            if models.Shorturl.objects.filter(short_url=word).exists():
                data = models.Shorturl.objects.filter(short_url=word).first()
                now = timezone.datetime.now().replace(tzinfo=None)
                before = data.create_date.replace(tzinfo=None)
                expire = now - before
                if expire.days > 7:
                    data.delete()
                    date=timezone.now()
                    short_url = word
                    data = models.Shorturl.objects.create(short_url=short_url,original_url=get_url,create_date=date)
                    data.save()
                    #print('成功')
                    request.session['short_url'] = short_url
                    request.session['original_url'] = get_url
                    return HttpResponseRedirect('/result')                            
                else:
                    messages.add_message(request, messages.WARNING,'The Short URL already exists')
                    return HttpResponseRedirect('/custom_url')           
            else:
                date=timezone.now()
                short_url = word
                data = models.Shorturl.objects.create(short_url=short_url,original_url=get_url,create_date=date)
                data.save()
                #print('成功')
                request.session['short_url'] = short_url
                request.session['original_url'] = get_url
                return HttpResponseRedirect('/result')
        else:
            get_url = False
            #print('False')
    else:
        form = forms.custom_form()
    return render(request, 'custom.html', locals())

def result(request):
    if 'short_url' in request.session:
        short_url = request.session['short_url']
    if 'original_url' in request.session:
        original_url = request.session['original_url']
        result = Base_url+short_url

    return render(request, 'result.html', locals())

def read_url(request,url):
    if request.method=="GET":
        now = timezone.datetime.now().replace(tzinfo=None)
        data = models.Shorturl.objects.filter(short_url=url).first()
        if not data or not data.original_url:
            messages.add_message(request, messages.WARNING,'The Short URL does not exist')
            return HttpResponseRedirect('/')
        #now = now.replace(tzinfo=None)
        before = data.create_date.replace(tzinfo=None)
        expire = now - before
        if expire.days > 7:
            messages.add_message(request, messages.WARNING,'The Short URL has expired')
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect(data.original_url)
    if request.method=="POST":
        messages.add_message(request, messages.WARNING,'Request error')
        HttpResponseRedirect('/')
