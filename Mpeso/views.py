from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.http.response import JsonResponse

def home(request):
    if request.user.is_authenticated:
        return redirect('miprogreso')
    else:
        return render(request, 'home.html')

def reggister(request):
    if request.method == 'GET':
        return render(request, 'reggister.html')
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('peso')
            except:
                return render(request, 'reggister.html', {
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'reggister.html', {
                'error': 'Las contraseñas no coinciden'
            })

def loggin(request):
    if request.method == 'GET':
        return render(request, 'loggin.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'loggin.html', {
                'error': 'El usuario no está registrado'
            })
        else:
            login(request, user)
            if UserPeso.objects.filter(user=request.user, altura__isnull=False):
                return redirect('miprogreso')
            else:
                return redirect('peso')
                
def desloggin(request):
    logout(request)
    return redirect('home')

@login_required
def peso(request):
    user = request.user

    if request.method == 'GET':
        user_peso_instance = UserPeso.objects.filter(user=user).last()
        peso_actual_instance = PesoActual.objects.filter(user=user).last()
        
        context = {
            'pesoActual': peso_actual_instance.pesoActual if peso_actual_instance else '',
            'pesoIdeal': user_peso_instance.pesoIdeal if user_peso_instance else '',
            'altura': user_peso_instance.altura if user_peso_instance else ''
        }
        return render(request, 'peso.html', context)
    else:
        pesoActual = request.POST['pesoActual']
        pesoIdeal = request.POST['pesoIdeal']
        altura = request.POST['altura']
        
        UserPeso.objects.update_or_create(pesoIdeal=pesoIdeal,altura=altura,user=user)
        PesoActual.objects.create(pesoActual=pesoActual, user=user)
        
        return redirect('miprogreso')
        
        
@login_required
def miprogreso(request):
    usuarios = UserPeso.objects.filter(user=request.user)
    usuario = usuarios.last()
    pesoActualUser = PesoActual.objects.filter(user=request.user).last()
    pesoActual = pesoActualUser.pesoActual
    pesoIdeal = usuario.pesoIdeal
    altura = usuario.altura
    
    pesoAbajar = pesoActual - pesoIdeal
    imc = pesoActual/(altura/100)**2
    if request.method == 'GET':  
            return render(request, 'miprogreso.html', {
            'pesoa': pesoActual,
            'pesoi': pesoIdeal,
            'pesoAbajar': pesoAbajar,
            'imc': round(imc, 2)
        })
    else:
        pesoA = request.POST['peso']
        PesoActual.objects.create(pesoActual=pesoA, user=request.user)
        pesoActualUser = PesoActual.objects.filter(user=request.user).last()
        pesoActual = pesoActualUser.pesoActual
        
        pesoAbajar = pesoActual - pesoIdeal
        imc = pesoActual/(altura/100)**2
        
        return render(request, 'miprogreso.html', {
            'pesoa': pesoActual,
            'pesoi': pesoIdeal,
            'pesoAbajar': pesoAbajar,
            'imc': round(imc, 2)
        })

@login_required
def get_chart(request):
    
    datosB = PesoActual.objects.filter(user=request.user)
    datos = [dato.pesoActual for dato in datosB]
    chart = {
        'xAxis': [
            {
                'type': 'category',
                'data': []
            }
        ],
        'yAxis': [
            {
                'type': 'value'
            }
        ],
        'series': [
            {
                'data': datos,
                'type': 'line',
            }
        ]
        }
    
    return JsonResponse(chart)

