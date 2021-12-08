from django import shortcuts
from django.conf import settings
from django.shortcuts import render, redirect
from EjercitoCRUD.models import Soldados, Armas, ArmaTomada, HombresCaidos, NuevasIncorporaciones
from django.db import connection
import datetime
from django.contrib import messages
import random
from EjercitoCRUD.fetchApp import dictfetchall
from django.contrib.auth.decorators import login_required



@login_required
def index (request):
    
    return render(request, 'index.html')

@login_required
def ListarNuevasIncorporaciones(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # showall = NuevasIncorporaciones.objects.all()
    with connection.cursor() as cursor:
        cursor.execute("SELECT soldados.nombre, nuevas_incorporaciones.fecha_incorporacion FROM nuevas_incorporaciones JOIN soldados ON nuevas_incorporaciones.id_soldado = soldados.id_soldado;")
        showall = dictfetchall(cursor)
        # print (showall)
    return render(request, 'nuevasincorporaciones.html',{"data":showall} )

@login_required
def ListarHombresCaidos(request):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT soldados.nombre, hombres_caidos.fecha_de_deceso FROM hombres_caidos JOIN soldados ON hombres_caidos.id_soldado = soldados.id_soldado;")
        showall = dictfetchall(cursor)
    return render(request,'hombrescaidos.html',{"data":showall} )

@login_required
def ListarHombresHeridos(request):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT nombre FROM soldados WHERE herido = true AND vivo = true")
        showall= dictfetchall(cursor)
    return render(request, 'hombresheridos.html', {"data":showall})

@login_required
def ListarArmasTomadas(request):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT soldados.nombre, armas.nombre_arma, arma_tomada.momento_toma, armas.tipo_arma, armas.danio FROM arma_tomada JOIN armas ON armas.id_arma = arma_tomada.id_arma JOIN soldados ON arma_tomada.nombre_soldado = soldados.nombre ORDER BY arma_tomada.momento_toma DESC;")
        showall = dictfetchall(cursor)
        # print(type(showall))
        # for i in showall:
        #     print (i)
    return render(request, 'armastomadas.html', {"data":showall})

@login_required
def RegistroSoldado(request):
    if request.method=="POST":
        if request.POST.get('nombre') and request.POST.get('arma'):
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_arma FROM armas WHERE nombre_arma =%s;", [request.POST.get('arma')])
                arma_tomada = cursor.fetchone()
                ct = datetime.datetime.now()
                # ts = ct.timestamp()
                cursor.execute("INSERT INTO arma_tomada(id_arma, momento_toma, nombre_soldado) VALUES (%s,%s, %s);", [arma_tomada,ct, request.POST.get('nombre')])
                cursor.execute("INSERT INTO soldados(nombre, id_arma_tomada, herido, vivo) VALUES (%s,%s, FALSE, TRUE);", [request.POST.get('nombre'), arma_tomada])                 
                cursor.execute("SELECT id_soldado FROM soldados WHERE  nombre = %s;",[request.POST.get('nombre')])
                id_soldado = cursor.fetchone()
                cursor.execute("INSERT INTO nuevas_incorporaciones(id_soldado, fecha_incorporacion) VALUES (%s,%s);", [id_soldado, ct])
                                 
                messages.success(request, 'Soldado agregado.')
                cursor.execute("select nombre_arma from armas;")
                showall = dictfetchall(cursor)

            return render(request, 'registrosoldado.html',{"data":showall})
    elif request.method=="GET":
        with connection.cursor() as cursor:
            cursor.execute("select nombre_arma from armas;")
            # armamento = ["tik-to-k", "Wha-tsA-pp", "Fac-ebo-ok", "Inst-ag-ram", "Zo-om", "Mess-enger", "Snapc-hat", "Tel-eg-ram", "Go-o-glem-eet", "Ne-t-flix"]
            # tipo_de_arma = ["Larga distancia", "Mediana-distancia", "Cuerpo a cuerpo"]
            showall = dictfetchall(cursor)
            # print(showall)
            # for arma in armamento:
            #     tipo = tipo_de_arma[random.randint(0,2)]
            #     danio = random.randint(50,100)
            #     cursor.execute("INSERT INTO armas (nombre_arma, danio, tipo_arma) VALUES (%s,%s,%s);",[arma, danio, tipo] )
                            
        return render(request, 'registrosoldado.html', {"data":showall})
 
@login_required              
def TomaDeArma(request):
    if request.method=="POST":
        if request.POST.get('nombre') and request.POST.get('nombre_arma'):
            with connection.cursor() as cursor:
                # obtener id de arma a partir de la seleccion del formulario pasad por POST
                nombre_arma = request.POST.get('nombre_arma')
                cursor.execute("SELECT id_arma FROM armas WHERE nombre_arma=%s;", [nombre_arma])
                id_arma = cursor.fetchone()
                # # obtener id soldado a partir del nombre del soldado
                # cursor.execute("SELECT id_soldado FROM soldados WHERE nombre = %s;", [request.POST.get('nombre')])
                # id_soldado = cursor.fetchone()
                ct = datetime.datetime.now()
                
                # crear toma de arma a partir de id y timestamp
                cursor.execute("INSERT INTO arma_tomada (id_arma, momento_toma, nombre_soldado) VALUES (%s,%s,%s);",[id_arma, ct, request.POST.get('nombre')])
                
                # obtener id arma_tomada a partir de timestamp 
                cursor.execute("SELECT id_arma_tomada FROM arma_tomada WHERE momento_toma=%s;", [ct])
                id_arma_tomada = cursor.fetchone()
                
                #actualizar arma_tomada por el soldado
                cursor.execute("UPDATE soldados SET id_arma_tomada = %s WHERE nombre = %s;",[id_arma_tomada, request.POST.get('nombre')])
        with connection.cursor() as cursor:
            # asignar armas y nombre de soldado a los manus
            cursor.execute("SELECT nombre_arma;")
            showArmas = dictfetchall(cursor)
            cursor.execute("SELECT nombre FROM soldados WHERE vivo=true;")
            showNombres = dictfetchall(cursor)
            
                               
                               
        return render(request, 'tomadearma.html', {"dataNombre":showNombres,"dataArma":showArmas})


    elif request.method=="GET":
         # asignar armas y nombre de soldado a los manus
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre_arma FROM armas;")
            showArmas = dictfetchall(cursor)
            cursor.execute("SELECT nombre FROM soldados WHERE vivo=true;")
            showNombres = dictfetchall(cursor)
            
                               
                               
        return render(request, 'tomadearma.html', {"dataNombre":showNombres,"dataArma":showArmas})

@login_required
def Novedades(request):
    if request.method=="POST":
        if request.POST.get('nombre'):
            nombre = str(request.POST.get('nombre'))
            print (nombre)
            if request.POST.get('herido'):
                herido = 'true'
            else:
                herido = 'false'
            if request.POST.get('deceso'):
                deceso = True
                vivo = 'false'

            
            with connection.cursor() as cursor:
                # print(herido)
                # print(vivo)
            # actualizar si el soldado esta herido o no
                cursor.execute("UPDATE soldados SET herido = %s WHERE nombre = %s;", [herido, nombre])
                # print('hello world!')
            # actualizar si el soldado esta muerto
                if request.POST.get('deceso'):
                    
                    deceso = True
                    vivo = 'false'
                    with connection.cursor() as cursor:
                        # identificadr soldado caido
                        cursor.execute("SELECT id_soldado FROM soldados WHERE nombre = %s;", [nombre])
                        soldado = cursor.fetchone()
                        id_soldado1 = int(str(soldado[0]))
                        print (str(id_soldado1))
                        #registrar momento de deceso
                        ct = datetime.datetime.now()

                        # marcar como no vivo y agregar a registro de hombres caidos
                        cursor.execute("UPDATE soldados SET vivo = %s WHERE nombre = %s;", [vivo, nombre])
                        cursor.execute("INSERT INTO hombres_caidos (id_soldado, fecha_de_deceso) VALUES (%s,%s);",[id_soldado1, ct])
        # asignar nombres al menu
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM soldados WHERE vivo=true;")
            showNombres = dictfetchall(cursor)
        
        return render(request, 'novedades.html', {"data":showNombres})

    else:
        # asignar nombres al menu
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre FROM soldados where vivo = true;")
            showNombres = dictfetchall(cursor)
        
        return render(request, 'novedades.html', {"data":showNombres})
        