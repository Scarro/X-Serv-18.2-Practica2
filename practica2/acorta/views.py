from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import generic

from urllib.parse import unquote

import http.client
import ssl

from .models import Url

def agregar(url):
    url = unquote(url)
    almacenada = False
    (existe, secure, url) = comprueba_url(url)
    if existe:
        try:
            nueva = Url.objects.get(url_completa=url)
        except Url.DoesNotExist:
            if secure == 1:
                protocol = "https"
            elif secure == -1:
                protocol = url.split(':')[0]
            else:
                protocol = "http"
            nueva = Url(url_completa=url, url_scheme=protocol)
            nueva.save()
            almacenada = True
    return almacenada

def comprueba_url(url):
    secure = 0
    if not url.startswith("http"):
        url1 = "https://" + url
        if not existe_url(url1):
            url1 = "http://" + url
            existe = existe_url(url1)
        else:
            existe = True
            secure = 1
    else:
        existe = existe_url(url)
        secure = -1
    return (existe, secure, url)

def existe_url(url):
    try:
        if url.startswith('https://'):
            url = url.split('//')[1]
            resp = http.client.HTTPSConnection(url,timeout=3)
            resp.request("GET", "/")
        else:
            url = url.split('//')[1]
            resp = http.client.HTTPConnection(url,timeout=3)
            resp.request("GET", "/")
        return True
    except Exception as e:
        print(e)
        return False

def index(request):
    if request.method=='POST':
        url = (request.body).decode('utf-8').split('=')[-1]
        resultado = agregar(url)
    urls = Url.objects.all()
    template = 'acortadora/index.html'
    context = {'lastest_urls': urls}
    return render(request, template, context)

def redirigir(request, acortada):
    try:
        url = Url.objects.get(url_acortada=acortada)
        direccion = url.url_scheme + "://" + url.url_completa
        return redirect(direccion)
    except:
        template = "acortadora/error.html"
        return render(request, template, {})