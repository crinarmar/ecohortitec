# coding=utf-8
#from django.shortcuts import render

# Create your views here.
import unicodedata
from citagro.models import Document,Inputoperacion,Cultivoexplotacion,RepositorioImagenes,Tiposoperacion,Administrador,Cultivo,Tecnico,Perfil,Explotacion,UsuarioExplotacion,DatosClimaticos,Provincia,Municipio,MaquinaExplotacion,Maquinaria,Aplicador,UHC,Analisis,Parcela,Parcelauhc,Aplicacion,Producto_aplicado,MaquinaExplotacion,Operacion,op_poda,op_labores,op_fertilizacion,op_riego,op_recoleccion
from citagro.models import Muestreo,muestra_fenologia,muestra_insetos,muestra_trampas,muestra_brotes,muestra_zeuzera,muestra_enfermedades
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,render_to_response,redirect
from django.core.urlresolvers import reverse,reverse_lazy
from forms import FormularioAdministrador,FormularioExplotacion,AsignaUsuarioFormulario,FormularioMaquina,FormularioClima,UploadForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
import random
import datetime
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import cache_page
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
    logout as auth_logout, get_user_model, update_session_auth_hash)
from django.template.response import TemplateResponse
from citagro.serializers import PerfilSerializer,InputoperacionSerializer,TiposoperacionSerializer,RepositorioImagenesSerializer,CultivoexplotacionSerializer,AdministradorSerializer, CultivoSerializer,TecnicoSerializer,ExplotacionSerializer,DatosClimaticosSerializer,MaquinariaSerializer,UsuariosSerializer,ProvinciaSerializer,MunicipioSerializer,AplicadorSerializer,UHCSerializer,ParcelaSerializer,ParcelauhcSerializer,AnalisisSerializer,AplicacionSerializer,ProductoSerializer,UsuarioExplotacionSerializer,MaquinaExplotacionSerializer,OperacionSerializer,op_podaSerializer,op_laboresSerializer,op_fertilizacionSerializer,op_riegoSerializer,op_recoleccionSerializer
from citagro.serializers import MuestreoSerializer,muestra_fenologiaSerializer,muestra_insetosSerializer,muestra_trampasSerializer,muestra_brotesSerializer,muestra_zeuzeraSerializer,muestra_enfermedadesSerializer
from rest_framework import status
from rest_framework import generics
from io import BytesIO
from datetime import datetime
from django.core.context_processors import csrf
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)
from datetime import date
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import A4
import xlsxwriter
import csv
import smtplib, getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
try:  
    import cStringIO as StringIO
except ImportError:  
    import StringIO

pdfmetrics.registerFont(TTFont('Arial Narrow', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('Arial Narrow Bold', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('Arial Narrow Cursiva', 'VeraIt.ttf'))
 
###Subida de archivo###
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
        	newdoc = Document(filename = request.POST['filename'],docfile = request.FILES['docfile'])
        	newdoc.save(form)
        	return redirect("uploads")
    else:
        form = UploadForm()
    return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))


###Vista Principal###
def main(request):
    if request.user.is_authenticated(): 
        if request.user.is_staff:
		        return HttpResponseRedirect('/superAdministrador/')
        else:
			perfilUsuario = Perfil.objects.get(user_id = request.user.id)
			tipoId = perfilUsuario.TipoUsuario			
			if tipoId == 'A':
				return HttpResponseRedirect('/administrador/')
			elif tipoId == 'T':
				return HttpResponseRedirect('/tecnico/')
        
    return render_to_response('citagro/main.html', {}, context_instance=RequestContext(request))
	
@login_required()
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
	
def ingresar (request):
    if request.user.is_authenticated(): 
        if request.user.is_staff:
			return HttpResponseRedirect('/superAdministrador/')
        else:
			perfilUsuario = Perfil.objects.get(user_id = request.user.id)
			tipoId = perfilUsuario.TipoUsuario			
			if tipoId == 'A':
				return HttpResponseRedirect('/administrador/')
			elif tipoId == 'T':
				return HttpResponseRedirect('/tecnico/')
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username = usuario,password = clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request,acceso)
                    if acceso.is_staff:
                        return HttpResponseRedirect('/superAdministrador/')
                    else:
                        perfilUsuario = Perfil.objects.get(user_id = acceso.id)
                        tipoId = perfilUsuario.TipoUsuario
						
                        if tipoId == 'A':
                            return HttpResponseRedirect('/administrador/')
                        elif tipoId == 'T':
                            return HttpResponseRedirect('/tecnico/')
					
                else:
                    return render_to_response('citagro/home.html', {'user': request.user}, context_instance=RequestContext(request))
               
            else:
                return render_to_response('citagro/login.html',{'form':formulario},context_instance = RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('citagro/login.html',{'form':formulario},context_instance = RequestContext(request))
	
	

###VistaAdministradorCitagro###
@login_required()
def VistaAdministradorCitagro(request):
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'T':
                return HttpResponseRedirect('/tecnico/')
            elif tipoId == 'A':
                return HttpResponseRedirect('/administrador/')
        template = loader.get_template('citagro/AdministradorCitagro/AdministradorCitagro.html')
        context = RequestContext(request, {})
    
    return HttpResponse(template.render(context))
	
@login_required()
def ListaAdministradores(request):
    if not request.user.is_staff:
        perfilUsuario = Perfil.objects.get(user_id = request.user.id)
        tipoId = perfilUsuario.TipoUsuario			
        if tipoId == 'T':
            return HttpResponseRedirect('/tecnico/')
        elif tipoId == 'A':
            return HttpResponseRedirect('/administrador/')
    lista_administradores = Administrador.objects.all()
    template = loader.get_template('citagro/AdministradorCitagro/CitagroAdministradores.html')
    context = RequestContext(request, {
        'administradorCitagro': request.user,
        'lista_administradores': lista_administradores,
    })
	
    return HttpResponse(template.render(context))
	

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii
	
def creaUsuario(nombre,apellido1,apellido2):

	usuario = remove_accents(nombre[0:3]+apellido1[0:3]+apellido2[0:3])
	us = User.objects.filter(username = usuario)
	while len(us) > 0:
	    usuario = usuario+str(random.randint(0,9))
	    us = User.objects.filter(username = usuario)
	return usuario.lower()
	
@login_required()
def creaAdministrador(request):
    if not request.user.is_staff:
        perfilUsuario = Perfil.objects.get(user_id = request.user.id)
        tipoId = perfilUsuario.TipoUsuario			
        if tipoId == 'T':
            return HttpResponseRedirect('/tecnico/')
        elif tipoId == 'A':
            return HttpResponseRedirect('/administrador/')
    provincia = Provincia.objects.all()
    template = loader.get_template('citagro/AdministradorCitagro/CreaAdministrador.html')
    context = RequestContext(request, {
		'provincias': provincia,
    })
	
    if request.method == 'POST':
	
        Provi = Provincia.objects.get(id=request.POST['provincia'])
        Muni = Municipio.objects.get(id=request.POST['municipio'])
        nomb = request.POST['Nombre']
        Ap1 = request.POST['Apellido1']
        Ap2 = request.POST['Apellido2']
        dni = request.POST['NIF']
        Domi = request.POST['Domicilio']
        cp = request.POST['CP']
        mail = request.POST['email']
        Tel1 = request.POST['Telefono1']
        Tel2 = request.POST['Telefono2']
        fx = request.POST['Fax']
        f_ingreso = str(datetime.today())[0:10]
        rop = request.POST['ropo']
		
        Usuario = creaUsuario(nomb,Ap1,Ap2)
        Password = 1234
		
        user = User.objects.create_user(Usuario,mail,Password)
        user.first_name = nomb
        user.last_name = Ap1
        user.is_active = True
		
        administrador = Administrador(id = "1",Nombre = nomb,Apellido1 = Ap1,Apellido2 = Ap2,NIF = dni,Domicilio = Domi,Municipio = Muni,Provincia = Provi,CP = cp,email = mail,Telefono1 = Tel1,Telefono2 = Tel2,Fax = fx,fecha_ingreso = f_ingreso,ropo = rop)

        perfil = Perfil(user=user, TipoUsuario='A')
			
        user.save()
        administrador.save()
        perfil.save()	
        return HttpResponseRedirect('/superAdministrador/administradores')
		
    return HttpResponse(template.render(context))

	
	
###VistaAdministrador###
@login_required()
def VistaAdministrador(request): 
    
    if request.user.is_staff:
	    return HttpResponseRedirect('/superAdministrador/')
	
    perfilUsuario = Perfil.objects.get(user_id = request.user.id)
    tipoId = perfilUsuario.TipoUsuario		
    administrador = Administrador.objects.get(id = request.user.id)	
    admin = administrador
    if tipoId == 'T':
        return HttpResponseRedirect('/tecnico/')
    uhcs = []
    operaciones = []
    fertilizacion = []
    primera_exp = ""
    template = loader.get_template('citagro/Administrador/Administrador.html')
    lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
	
    if len(lista_explotaciones) > 0:
        uhcs = UHC.objects.filter(idExplotacion = lista_explotaciones[0])
        operaciones = Operacion.objects.filter(idExplotacion = lista_explotaciones[0],idUHC = uhcs[0]).order_by('idExplotacion','-fecha_operacion')
        fertilizacion = op_fertilizacion.objects.filter(idOperacion__in =list(operaciones))
        for ferti in fertilizacion:
            ferti.idOperacion.fecha_operacion.year
        primera_exp = lista_explotaciones[0]
    tecnicos = Tecnico.objects.filter(idAdmin = request.user.id)
    context = RequestContext(request, {
		'explotacion':primera_exp,
		'lista_explotaciones':lista_explotaciones,
		'tecnicos':tecnicos,
        'operaciones':operaciones,
		'fertilizacion':fertilizacion,
		'administrador':administrador,
		'uhcs':uhcs,
		'userid':administrador.id,
		'admin':admin,
	})
    
    return HttpResponse(template.render(context))
	
def EditaInput(request,string): 
    
    listaInput = string.split('*')
    id = listaInput[0]
    tipo = Tiposoperacion.objects.get(id=listaInput[2])
    r = Inputoperacion.objects.filter(id = id)
    
	
    '''input = listaInput[1]
	idTipoOp = listaInput[2]
	coefEmision = listaInput[3]
	cantidad = listaInput[4]
	coefAsignacion = listaInput[5]
	costeUnitario = listaInput[6]
	unidad = listaInput[7]
	unidadCoef = listaInput[8]'''
    r.update(
		input = listaInput[1],
		idTipoOp = Tiposoperacion.objects.get(id=listaInput[2]),
		coefEmision = listaInput[3],
		cantidad = listaInput[4],
		coefAsignacion = listaInput[5],
		costeUnitario = listaInput[6],
		unidad = listaInput[7],
		unidadCoef = listaInput[8],
		
	)

	
	
	
	
	
    
    return HttpResponseRedirect('/configuracion/')
	
@login_required()
def ListaTecnicosAdministrador(request):
    if request.user.is_staff:
	    return HttpResponseRedirect('/superAdministrador/')
    lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
    perfilUsuario = Perfil.objects.get(user_id = request.user.id)
    tipoId = perfilUsuario.TipoUsuario			
    if tipoId == 'T':
        return HttpResponseRedirect('/tecnico/')
		

    lista_tecnicos = Tecnico.objects.filter(idAdmin=request.user.id,activo = 'SI')
    administrador = Administrador.objects.get(id = request.user.id)
    provincia = Provincia.objects.all()
    municipio = Municipio.objects.all()
    template = loader.get_template('citagro/Administrador/AdministradorTecnicos.html')
    context = RequestContext(request, {
        'administrador': administrador,
        'lista_tecnicos': lista_tecnicos,
		'provincias':provincia,
		'municipios':municipio,
        'lista_explotaciones':lista_explotaciones,
    })
	
    return HttpResponse(template.render(context))

@login_required()
def creaTecnico(request):
    administrador = Administrador.objects.get(id = request.user.id)
    provincia = Provincia.objects.all()
    lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
    template = loader.get_template('citagro/Administrador/creaTecnico.html')
    context = RequestContext(request, {
		'provincias': provincia,
        'lista_explotaciones':lista_explotaciones,
		'administrador':administrador,

    })
	
    if request.method == 'POST':
	
        admin = Administrador.objects.get(id=request.user.id)
        Provi = Provincia.objects.get(id=request.POST['provincia'])
        Muni = Municipio.objects.get(id=request.POST['municipio'])
        nomb = request.POST['Nombre']
        Ap1 = request.POST['Apellido1']
        Ap2 = request.POST['Apellido2']
        dni = request.POST['NIF']
        Domi = request.POST['Domicilio']
        cp = request.POST['CP']
        mail = request.POST['email']
        Tel1 = request.POST['Telefono1']
        Tel2 = request.POST['Telefono2']
        fx = request.POST['Fax']
        f_ingreso = str(datetime.today())[0:10]
        rop = request.POST['ropo']
		
        Usuario = creaUsuario(nomb,Ap1,Ap2)
        Password = 1234
		
        user = User.objects.create_user(Usuario,mail,Password)
        user.first_name = nomb
        user.last_name = Ap1
        user.is_active = True
        tecnico = Tecnico(id = user.id,Nombre = nomb,Apellido1 = Ap1,Apellido2 = Ap2,NIF = dni,Domicilio = Domi,Municipio = Muni,Provincia = Provi,CP = cp,email = mail,Telefono1 = Tel1,Telefono2 = Tel2,Fax = fx,fecha_ingreso = f_ingreso,ropo = rop,idAdmin = admin)
		
        perfil = Perfil(user=user, TipoUsuario='T')
			
        user.save()
        tecnico.save()
        perfil.save()	
        return HttpResponseRedirect('/administrador/tecnicos')
		
    return HttpResponse(template.render(context))
	
@login_required()
def ModificaTecnico(request,id_Tecnico):

    provincia = Provincia.objects.all()
    municipio = Municipio.objects.all()
    administrador = Administrador.objects.get(id = request.user.id)
    tecnico = Tecnico.objects.get(id = id_Tecnico)
    lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
    template = loader.get_template('citagro/Administrador/creaTecnico.html')
    context = RequestContext(request, {
		'provincias': provincia,
		'municipios':municipio,
        'lista_explotaciones':lista_explotaciones,
		'tecnico':tecnico,
		'administrador':administrador,

    })
		
    return HttpResponse(template.render(context))

def crearParcela(request,string):

	lista = string.split("/")
	
	nombre = lista[0]
	prov = lista[1]
	mun = lista[2]
	poli = lista[3]
	parc = lista[4]
	rec = lista[5]
	sup = lista[6]
	sr = lista[7]
	desc = lista[8]
	idExpl = lista[9]
	idcult = lista[10]


	parcela = Parcela.objects.create( 
		nombre = nombre,
		provincia = Provincia.objects.get(id=prov),
		municipio = Municipio.objects.get(id=mun),
		poligono = poli,
		parcela = parc,
		recinto = rec,
		superficie_hectareas = sup,
		sr = sr,
		descripcion = desc,
		idExplotacion = Explotacion.objects.get(id=idExpl),
		idcultivo = Cultivo.objects.get(id=idcult)
	)
	return HttpResponseRedirect('/tecnicoExplotacion/'+idExpl)
	
@login_required()
def ListaExplotaciones(request):
    
    lista_Explotaciones_usuario = Explotacion.objects.raw('''SELECT citagro_explotacion.id,citagro_explotacion.Razon_Social,citagro_tecnico.Nombre  from citagro_explotacion join citagro_usuarioexplotacion join citagro_tecnico
	                                                      where citagro_explotacion.idAdmin_id = %s and 
	                                                      citagro_usuarioexplotacion.idExplotacion_id = citagro_explotacion.id
														  and citagro_usuarioexplotacion.idUsuario_id = citagro_tecnico.id ''', [request.user.id])
    
    lista_Explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
	
    count = len(list(lista_Explotaciones_usuario))+len(list(lista_Explotaciones))
    template = loader.get_template('citagro/Administrador/Explotaciones.html')
    context = RequestContext(request, {
        'administradorCitagro': request.user,
		'lista_explotaciones':lista_Explotaciones,
		'lista_explotaciones_usuario': lista_Explotaciones_usuario,
		'count':count,
    })
	
    return HttpResponse(template.render(context))

@login_required()	
def AdministradorExplotacionId(request,id_Explotacion):
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'T':
                return HttpResponseRedirect('/tecnico/explotacion/'+id_Explotacion)
            else:
				administrador = Administrador.objects.get(id = request.user.id)	
				lista_Explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
				template = loader.get_template('citagro/Administrador/Explotacion.html')
				explotacion = Explotacion.objects.get(id=id_Explotacion)
				uhcs = UHC.objects.filter(idExplotacion=id_Explotacion)
				listauhc = list(uhcs)

				parcelas = Parcelauhc.objects.filter(idUHC__in=listauhc)
				analisis = Analisis.objects.filter(idUHC__in=listauhc)
				aplicaciones = Aplicacion.objects.filter(idUHC__in=listauhc)
				
				
				datosClimaticos = DatosClimaticos.objects.filter(idExplotacion = id_Explotacion)
				datosClimaticos = datosClimaticos.extra(order_by=['-fecha'])
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = id_Explotacion)
				listaus = []
				for usuario in usuarios:
					listaus.append(int(usuario.idUsuario.id))
					
				tecnicoAs  = Tecnico.objects.filter(id__in=listaus)
				aplicadores = Aplicador.objects.all()
				provincias = Provincia.objects.all()
				
				context = RequestContext(request, {
					'lista_explotaciones':lista_Explotaciones,
					'explotacion':explotacion,
					'uhcsExplotacion':uhcs,
					'parcelas':parcelas,
					'analisis':analisis,
					'aplicaciones':aplicaciones,
					'tecnicosExplotacion':tecnicoAs,
					'aplicadores':aplicadores,
					'datosClimaticos':datosClimaticos,
					'provincias':provincias,
					'administrador':administrador,
				})
				
				return HttpResponse(template.render(context))

@login_required()
def creaExplotacion(request):
    #administrador = Administrador.objects.get(id = request.user.id)	
    provincia = Provincia.objects.all()
    lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
    template = loader.get_template('citagro/Administrador/creaExplotacion.html')
    context = RequestContext(request, {
		'provincias': provincia,
        'lista_explotaciones': lista_explotaciones,
		#'administrador':administrador,
    })
	
    if request.method == 'POST':
	
        #admin = Administrador.objects.get(id=request.user.id)
        Provi = Provincia.objects.get(id=request.POST['provincia'])
        Muni = Municipio.objects.get(id=request.POST['municipio'])
        Razon = request.POST['Razon_Social']
        nf = request.POST['cif_nif']
        Domicilio = request.POST['Domicilio']
        CP = request.POST['CP']
		

        #explotacion = Explotacion(Razon_Social=request.POST['Razon_Social'],cif_nif = request.POST['cif_nif'],Domicilio = request.POST['Domicilio'],Localidad = Muni,Provincia = Provi,CP = request.POST['CP'],idAdmin = "1")
        explotacion = Explotacion.objects.create( 
		Razon_Social = request.POST['Razon_Social'],
		cif_nif = request.POST['cif_nif'],
		Domicilio = request.POST['Domicilio'],
		Localidad = Municipio.objects.get(id=Muni),
		Provincia = Provincia.objects.get(id=Provi),
		CP = request.POST['CP'],
		idAdmin = Administrador.objects.get(id=1),

	)
		
		
			
        explotacion.save()
        return HttpResponseRedirect('/administrador/explotacion/'+str(explotacion.id))
		
    return HttpResponse(template.render(context))
	
@login_required()
def AsignaUsuario(request,id_Explotacion):
    explotacion = Explotacion.objects.get(id=id_Explotacion)
    if request.method == 'POST':
        form = AsignaUsuarioFormulario(request.POST,id = explotacion.id,user_id =request.user.id)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.idExplotacion = explotacion
            recipe.save()
			
            return HttpResponseRedirect('/administrador/explotaciones')
    else:
        form = AsignaUsuarioFormulario(id = explotacion.id,user_id =request.user.id)
		
    template = loader.get_template('citagro/Administrador/AsignaUsuario.html')
    context = RequestContext(request, {
        'form':form,
		'explotacion':explotacion,
    })
    return HttpResponse(template.render(context))
	
@login_required()
def VistaAnalisis(request,id_Analisis):

    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'T':
                return HttpResponseRedirect('/tecnico/analisis/'+id_Analisis)
            else:
				administrador = Administrador.objects.get(id = request.user.id)	
				analisis = Analisis.objects.get(id=id_Analisis)
				lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
				documentos = Document.objects.filter(idAnalisis=id_Analisis)
				documento = "";
				uhcParcelas = Parcelauhc.objects.filter(idUHC = analisis.idUHC)
				uhcs = UHC.objects.filter(idExplotacion = analisis.idExplotacion)
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = analisis.idExplotacion)
				listaus = []
				for usuario in usuarios:
					listaus.append(int(usuario.idUsuario.id))
					
				tecnicoAs  = Tecnico.objects.filter(id__in=listaus)
				if len(documentos) > 0:
					documento = documentos[0]
					
				
				if request.method == 'POST':
					form = UploadForm(request.POST, request.FILES)
					if form.is_valid():
						newdoc = Document(filename = request.FILES['docfile'].name,docfile = request.FILES['docfile'],idAnalisis = analisis)
						newdoc.save(form)
						return HttpResponseRedirect('/administrador/analisis/'+id_Analisis)
				else:
					form = UploadForm()
					template = loader.get_template('citagro/Administrador/analisis.html')
				   
					context = RequestContext(request, {
						'form':form,
						'analisis':analisis,
						'lista_explotaciones':lista_explotaciones,
						'tecnicosExplotacion':tecnicoAs,
						'documentos':documentos,
						'documento':documento,
						'uhcs':uhcs,
						'uhcParcelas':uhcParcelas,
						'administrador':administrador,
					})
					return HttpResponse(template.render(context))
		
@login_required()	
def VistaAplicacion(request,id_Aplicacion):
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'T':
                return HttpResponseRedirect('/tecnico/aplicacion/'+id_Aplicacion)
            else:
				administrador = Administrador.objects.get(id = request.user.id)	
				aplicacion = Aplicacion.objects.get(id=id_Aplicacion)
				lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
				productos = Producto_aplicado.objects.filter(aplicacion=id_Aplicacion)
				aplicadores = Aplicador.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				maq_exp = MaquinaExplotacion.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				uhcs = UHC.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				uhcParcelas = Parcelauhc.objects.filter(idUHC = aplicacion.idUHC)
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				listaus = []
				for usuario in usuarios:
					listaus.append(int(usuario.idUsuario.id))
				tecnicoAs  = Tecnico.objects.filter(id__in=listaus)
				maquinas = []
				for maq in maq_exp:
					maquinas.append(maq.idMaquina)
			   
				template = loader.get_template('citagro/Administrador/aplicacion.html')
				   
				context = RequestContext(request, {
						'aplicacion':aplicacion,
						'productos':productos,
						'aplicadores':aplicadores,
						'maquinaria':maquinas,
						'tecnicosExplotacion':tecnicoAs,
						'uhcs':uhcs,
						'lista_explotaciones':lista_explotaciones,
						'uhcParcelas':uhcParcelas,
						'administrador':administrador,
				})
				return HttpResponse(template.render(context))
	
@login_required()	
def VistaOperacion(request,id_Operacion):
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'T':
                return HttpResponseRedirect('/tecnico/operacion/'+id_Operacion)
            else:
				administrador = Administrador.objects.get(id = request.user.id)	
				operacion = Operacion.objects.get(id=id_Operacion)
				lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
				poda = ''
				labores = ''
				fertilizacion = ''
				riego = ''
				recoleccion = ''
				tipoP = ''
				uhcParcelas = Parcelauhc.objects.filter(idUHC = operacion.idUHC)
				uhcs = UHC.objects.filter(idExplotacion = operacion.idExplotacion)
				tipoId = "";
				tipoNombr = "";
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = operacion.idExplotacion)
				listaus = []
				for usuario in usuarios:
					listaus.append(int(usuario.idUsuario.id))
				tecnicoAs  = Tecnico.objects.filter(id__in=listaus)
				template = loader.get_template('citagro/Administrador/operacion.html')
				if operacion.tipoOp == 'PODA':
					poda = op_poda.objects.get(idOperacion = operacion)
					tipoId  = poda.id
					tipoNombr = "poda"
					tipo = poda.TipoPoda
					
					if tipo == 'FORMACION':
						tipoP = 'Poda de formación'
					elif tipo == 'PRODUCCION':
						tipoP = 'Poda de producción'
					elif tipo == 'REJUVENECIMIENTO':
						tipoP = 'Poda de rejuvenecimiento'
					elif tipo == 'ACLAREO':
						tipoP = 'Poda de aclareo'
					
				elif operacion.tipoOp == 'LABORES DE SUELO':
					labores = op_labores.objects.get(idOperacion = operacion)
					tipoId  = labores.id;
					tipoNombr = "labores"
					tipo = labores.apero
					if tipo == 'CULTIVADOR':
						tipoP = 'Cultivador'
					elif tipo == 'DISCOS':
						tipoP = 'Arado discos'
					elif tipo == 'VERTEDERA':
						tipoP = 'Arado vertedera'
					elif tipo == 'DESBROZADOR':
						tipoP = 'Desbrozador'
				elif operacion.tipoOp == 'FERTILIZACION-ENMIENDA':
					fertilizacion = op_fertilizacion.objects.get(idOperacion = operacion)
					tipoId  = fertilizacion.id;
					tipoNombr = "fertilizacion"
					tipo = fertilizacion.tipo_fert
					if tipo == 'COBERTERA':
						tipoP = 'Abonado cobertera'
					elif tipo == 'FONDO':
						tipoP = 'Abonado de fondo'
					elif tipo == 'ENMIENDAS':
						tipoP = 'Enmiendas'
				elif operacion.tipoOp == 'RIEGO':
					riego = op_riego.objects.get(idOperacion = operacion)
					tipoId  = riego.id;
					tipoNombr = "riego"
					tipo = riego.sistema_riego
					if tipo == 'GOTEROS':
						tipoP = 'Localizado: Goteros'
					elif tipo == 'ASPERSION':
						tipoP = 'Aspersión'
				else:
					recoleccion = op_recoleccion.objects.get(idOperacion = operacion)
					tipoId  = recoleccion.id;
					tipoNombr = "recoleccion"
					tipo = recoleccion.metodo_recol
					if tipo == 'MANUAL':
						tipoP = 'Manual'
					elif tipo == 'MECANIZADO':
						tipoP = 'Mecanizado'
				context = RequestContext(request, {
						'operacion':operacion,
						'uhcs':uhcs,
						'lista_explotaciones':lista_explotaciones,
						'poda':poda,
						'tipoP':tipoP,
						'labores':labores,
						'fertilizacion':fertilizacion,
						'riego':riego,
						'recoleccion':recoleccion,
						'uhcParcelas':uhcParcelas,
						'tipoId':tipoId,
						'tipoNombr':tipoNombr,
						'administrador':administrador,
						'tecnicosExplotacion':tecnicoAs,
				})
				return HttpResponse(template.render(context))
	
@login_required()
def VistaMuestreo(request,id_Muestra):
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'T':
                return HttpResponseRedirect('/tecnico/muestreo/'+id_Muestra)
            else:
				administrador = Administrador.objects.get(id = request.user.id)	
				muestra = Muestreo.objects.get(id=id_Muestra)
				lista_explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
			   
				uhcParcelas = Parcelauhc.objects.filter(idUHC = muestra.idUHC)
				uhcs = UHC.objects.filter(idExplotacion = muestra.idExplotacion)
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = muestra.idExplotacion)
				listaus = []
				for usuario in usuarios:
					listaus.append(int(usuario.idUsuario.id))
					
				tecnicoAs  = Tecnico.objects.filter(id__in=listaus, activo='SI')
				fenologia = muestra_fenologia.objects.filter(idMuestra = muestra.id)
				insect = muestra_insetos.objects.filter(idMuestra = muestra.id)
				insectos = ""
				if len(insect) > 0:
					insectos = insect[0]
				trampas = muestra_trampas.objects.filter(idMuestra = muestra.id)
				brotes = muestra_brotes.objects.filter(idMuestra = muestra.id)
				zeuzera = muestra_zeuzera.objects.filter(idMuestra = muestra.id)
				enf = muestra_enfermedades.objects.filter(idMuestra = muestra.id)
				enfermedades = ""
				if len(enf) > 0:
					enfermedades = enf[0]
				template = loader.get_template('citagro/Administrador/muestreo.html')
				context = RequestContext(request, {
						'muestreo':muestra,
						'lista_explotaciones':lista_explotaciones,
						'tecnicosExplotacion':tecnicoAs,
						'uhcs':uhcs,
						'uhcParcelas':uhcParcelas,
						'administrador':administrador,
						'fenologia':fenologia,
						'insectos':insectos,
						'trampas':trampas,
						'brotes':brotes,
						'zeuzera':zeuzera,
						'enfermedades':enfermedades,
					})
				return HttpResponse(template.render(context))
		
def pdf_view(request,id_documento):
    documento = Document.objects.get(idAnalisis = id_documento)
	
    with open(documento.docfile.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename='+documento.filename+'.pdf'
        return response
    pdf.closed
	

@login_required()
def VistaUsuarioExplotacion(request,id_Explotacion):
    lista_Explotaciones_usuario = UsuarioExplotacion.objects.raw('''SELECT *  from citagro_usuarioexplotacion join citagro_tecnico join citagro_municipio join citagro_provincia
	                                                      where citagro_usuarioexplotacion.idExplotacion_id = %s
														  and citagro_usuarioexplotacion.idUsuario_id = citagro_tecnico.id 
														  and citagro_tecnico.Municipio_id = citagro_municipio.id
														  and citagro_municipio.idProvincia_id = citagro_provincia.id''', [id_Explotacion])
    
    explotacion = Explotacion.objects.get(id = id_Explotacion)
    template = loader.get_template('citagro/Administrador/UsuarioExplotacion.html')
    context = RequestContext(request, {
        'administradorCitagro': request.user,
		'lista_explotaciones_usuario': lista_Explotaciones_usuario,
		'explotacion':explotacion,
    })
	
    return HttpResponse(template.render(context))
	

class EliminarUsuario(DeleteView):
    model = UsuarioExplotacion

    success_url = '/administrador/explotaciones'
	

@login_required()
def MaquinariaUsuario(request):
    lista_Explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
    lista_maquinas = Maquinaria.objects.filter(idAdmin = request.user.id,activo = 'SI')
    administrador = Administrador.objects.get(id = request.user.id)	
	
    template = loader.get_template('citagro/Administrador/MaquinariaUsuario.html')
    context = RequestContext(request, {
        'lista_maquinas': lista_maquinas,
        'lista_explotaciones':lista_Explotaciones,
		'administrador':administrador,
    })
	
    return HttpResponse(template.render(context))
	
@login_required()
def creaMaquina(request):
    administrador = Administrador.objects.get(id = request.user.id)	
    lista_Explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)
    template = loader.get_template('citagro/Administrador/creaMaquina.html')
    context = RequestContext(request, {'lista_explotaciones':lista_Explotaciones,'administrador': administrador})
    if request.method == 'POST':
	
        admin = Administrador.objects.get(id=request.user.id)
        roma = request.POST['numero_roma']
        fecha_ad = request.POST['fecha_adquisicion']
        fecha_rev = request.POST['fecha_revision']
        Tipo = request.POST['TipoMaquina']
        Marca = request.POST['MarcaModelo']
		
        maquina = Maquinaria(numero_roma = roma,fecha_adquisicion = fecha_ad,fecha_revision = fecha_rev,TipoMaquina = Tipo,MarcaModelo = Marca,idAdmin = admin)
		
			
        maquina.save()
        return HttpResponseRedirect('/administrador/maquinas_Y_Equipos/')
		
    return HttpResponse(template.render(context))
	
@login_required()
def ListaMaquinaria(request,id_Explotacion):
   
    lista_maquinas = Maquinaria.objects.filter(idExplotacion=id_Explotacion)
    explotacion = Explotacion.objects.get(id = id_Explotacion)
    template = loader.get_template('citagro/Administrador/Maquinaria.html')
    context = RequestContext(request, {
        'lista_maquinas': lista_maquinas,
		'explotacion': explotacion,
    })
	
    return HttpResponse(template.render(context))

	
class EliminarMaquina(DeleteView):
    model = Maquinaria

    success_url = '/administrador/explotaciones'
	
@login_required()
def datosClimaticos(request,id_Explotacion):

    datos = DatosClimaticos.objects.filter(idExplotacion=id_Explotacion)
    explotacion = Explotacion.objects.get(id = id_Explotacion)
    template = loader.get_template('citagro/Administrador/DatosClimaticos.html')
    context = RequestContext(request, {
        'datos': datos,
        'explotacion': explotacion,
    })
	
    return HttpResponse(template.render(context))
	
@login_required()
def creaDatosClimaticos(request,id_Explotacion):
    explotacion = Explotacion.objects.get(id=id_Explotacion)
    if request.method == 'POST':
        form = FormularioClima(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.idExplotacion = explotacion
            recipe.save()
			
            return HttpResponseRedirect('/administrador/Datos_Climaticos/'+id_Explotacion)
    else:
        form = FormularioClima()
		
	template = loader.get_template('citagro/Administrador/creaDatoClimatico.html')
    context = RequestContext(request, {
        'form':form,
		'explotacion':explotacion,
    })
    return HttpResponse(template.render(context))
	

	
###VistaTecnico###
@login_required()
def VistaTecnico(request):
    tecnico = Tecnico.objects.get(id = request.user.id)
    admin = tecnico.idAdmin
    lista_Explotaciones = Explotacion.objects.all()#tecnico.explotaciones_asignadas
    if request.user.is_staff:
	    return HttpResponseRedirect('/administradorCitagro/')
		
    #cultivos = Cultivo.objects.all().order_by('fecha_inicio')
    perfilUsuario = Perfil.objects.get(user_id = request.user.id)
    tipoId = perfilUsuario.TipoUsuario			
    if tipoId == 'A':
        return HttpResponseRedirect('/administrador/')
    template = loader.get_template('citagro/Administrador/Administrador.html')
    explotaciones = UsuarioExplotacion.objects.filter(idUsuario = tecnico.id).order_by('idExplotacion')
    primera_exp = ""
    if len(explotaciones) > 0:
        primera_exp = explotaciones[0].idExplotacion

    context = RequestContext(request, {
		'explotacion':primera_exp,
		#'cultivos':cultivos,
		"lista_explotaciones":lista_Explotaciones,
		"tecnico":tecnico,
		'userid':tecnico.idAdmin.id,
		'admin':admin,
    })
    	
    return HttpResponse(template.render(context))
	
@login_required()
def VistaTecnicoExplotacion(request,idExpl):
    tecnico = Tecnico.objects.get(id = request.user.id)
    admin = tecnico.idAdmin
    esExplotacion = 1
    lista_Explotaciones = Explotacion.objects.all()
    if request.user.is_staff:
	    return HttpResponseRedirect('/administradorCitagro/')
		
    cultivos = Cultivo.objects.all().order_by('fecha_inicio')
    parcelas = Parcela.objects.filter(idExplotacion = idExpl).order_by('id')
    parcelasUhc = Parcelauhc.objects.filter(idExplotacion = idExpl).order_by('id')
    perfilUsuario = Perfil.objects.get(user_id = request.user.id)
    explotacionID = Explotacion.objects.get(id = idExpl)
    tipoId = perfilUsuario.TipoUsuario			
    if tipoId == 'A':
        return HttpResponseRedirect('/administrador/')
    template = loader.get_template('citagro/Administrador/Administrador.html')
    explotaciones = UsuarioExplotacion.objects.filter(idUsuario = tecnico.id).order_by('idExplotacion')
    primera_exp = ""
    if len(explotaciones) > 0:
        primera_exp = explotaciones[0].idExplotacion

    context = RequestContext(request, {
		'explotacion':explotacionID,
		'cultivos':cultivos,
		'parcelas':parcelas,
		'parcelasUhc':parcelasUhc,
		'esExplotacion':esExplotacion,
		"lista_explotaciones":lista_Explotaciones,
		"tecnico":tecnico,
		'userid':tecnico.idAdmin.id,
		'admin':admin,
    })
    	
    return HttpResponse(template.render(context))
	
@login_required()
def VistaConfiguracion(request):
    tecnico = Tecnico.objects.get(id = request.user.id)
    admin = tecnico.idAdmin
    lista_Explotaciones = tecnico.explotaciones_asignadas
    if request.user.is_staff:
	    return HttpResponseRedirect('/administradorCitagro/')
		
	
    uhcs = UHC.objects.all()
    Inputoperaciones = Inputoperacion.objects.all().order_by('nombreTipo','input')
    perfilUsuario = Perfil.objects.get(user_id = request.user.id)
    tipoId = perfilUsuario.TipoUsuario			
    if tipoId == 'A':
        return HttpResponseRedirect('/administrador/')
    template = loader.get_template('citagro/Administrador/Configuracion.html')
    explotaciones = UsuarioExplotacion.objects.filter(idUsuario = tecnico.id).order_by('idExplotacion')
    primera_exp = ""
    if len(explotaciones) > 0:
        primera_exp = explotaciones[0].idExplotacion

    context = RequestContext(request, {
		'explotacion':primera_exp,
		'uhcs':uhcs,
		'Inputoperaciones':Inputoperaciones,
		"lista_explotaciones":lista_Explotaciones,
		"tecnico":tecnico,
		'userid':tecnico.idAdmin.id,
		'admin':admin,
    })
    	
    return HttpResponse(template.render(context))
	
	

def VistaTecnicoCultivo(request,idCultivo):
    tecnico = Tecnico.objects.get(id = request.user.id)
    admin = tecnico.idAdmin
    lista_Explotaciones = tecnico.explotaciones_asignadas
    cultivos = Cultivo.objects.all()
	
    cultivosExplotacion = Cultivoexplotacion.objects.filter(idCultivo = idCultivo)
    nombreCultivo = cultivosExplotacion[0].idCultivo.nombre 
	
    uhcs = []
    operacionesUHC = []
    operaciones = []
    aplicacionesUHC = []
    analisisUHC = []
    for cultivoExp in  cultivosExplotacion:
		uhcs.append(cultivoExp.idUHC)

    for cultivoExp in  cultivosExplotacion:
		operacionesUHC.append(cultivoExp.idUHC.id)
    for idOp in  operacionesUHC:
		operacion = Operacion.objects.filter(idUHC = idOp)
		aplicacion = Aplicacion.objects.filter(idUHC = idOp)
		analisis = Analisis.objects.filter(idUHC = idOp)
		operaciones.append(operacion[0])
		if len(analisis) > 0:
			analisisUHC.append(analisis[0])
		if len(aplicacion) > 0:
			aplicacionesUHC.append(aplicacion[0])
    if request.user.is_staff:
	    return HttpResponseRedirect('/administradorCitagro/')
		
    perfilUsuario = Perfil.objects.get(user_id = request.user.id)
    tipoId = perfilUsuario.TipoUsuario			
    if tipoId == 'A':
        return HttpResponseRedirect('/administrador/')
    template = loader.get_template('citagro/Administrador/AdministradorCultivo.html')
    explotaciones = UsuarioExplotacion.objects.filter(idUsuario = tecnico.id).order_by('idExplotacion')
    primera_exp = ""
    if len(explotaciones) > 0:
        primera_exp = explotaciones[0].idExplotacion

    context = RequestContext(request, {
		'explotacion':primera_exp,
		'operaciones':operaciones,
		'aplicacionesUHC':aplicacionesUHC,
		'analisisUHC':analisisUHC,
		"lista_explotaciones":lista_Explotaciones,
		"cultivos":cultivos,
		"idCultivo":idCultivo,
		"nombreCultivo":nombreCultivo,
		"uhcs":uhcs,
		"tecnico":tecnico,
		'userid':tecnico.idAdmin.id,
		'admin':admin,
    })
    	
    return HttpResponse(template.render(context))
	
@login_required()	
def TecnicoExplotacionId(request,id_Explotacion):
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'A':
                return HttpResponseRedirect('/administrador/explotacion/'+id_Explotacion)
            else:
				tipoOperaciones = Tiposoperacion.objects.all()
				tecnico = Tecnico.objects.get(id = request.user.id)
				userid = request.user.id;
				lista_Explotaciones = tecnico.explotaciones_asignadas
				template = loader.get_template('citagro/Administrador/ExplotacionSinUHC.html')
				explotacion = Explotacion.objects.get(id=id_Explotacion)
				uhcs = UHC.objects.filter(idExplotacion=id_Explotacion)
				listauhc = list(uhcs)
				
				parcelas = Parcela.objects.all()
				analisis = Analisis.objects.filter(idUHC__in=listauhc)
				aplicaciones = Aplicacion.objects.filter(idUHC__in=listauhc)
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = id_Explotacion)
				listaus = []
				
				datosClimaticos = DatosClimaticos.objects.filter(idExplotacion = id_Explotacion)
				datosClimaticos = datosClimaticos.extra(order_by=['-fecha'])
				provincias = Provincia.objects.all()
				
				context = RequestContext(request, {
					'lista_explotaciones':lista_Explotaciones,
					'explotacion':explotacion,
					'tipoOperaciones':tipoOperaciones,
					'userid':userid,
					'uhcsExplotacion':uhcs,
					'parcelas':parcelas,
					'analisis':analisis,
					'aplicaciones':aplicaciones,
					'datosClimaticos':datosClimaticos,
					'provincias':provincias,
					'tecnico':tecnico,
				})
				
				return HttpResponse(template.render(context))
				
@login_required()	
def TecnicoExplotacionIdUHC(request,string):

    spilt = string.split("/") 
    id_Explotacion = spilt[0] 
    idUHC = spilt[1] 
    muestras = Muestreo.objects.filter(idUHC = idUHC).order_by('-fecha_muestreo') 
	
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'A':
                return HttpResponseRedirect('/administrador/explotacion/'+id_Explotacion)
            else:
				tipoOperaciones = Tiposoperacion.objects.all()
				tecnico = Tecnico.objects.get(id = request.user.id)
				userid = request.user.id;
				lista_Explotaciones = tecnico.explotaciones_asignadas
				template = loader.get_template('citagro/Administrador/Explotacion.html')
				explotacion = Explotacion.objects.get(id=id_Explotacion)
				uhcs = UHC.objects.filter(idExplotacion=id_Explotacion)
				listauhc = list(uhcs)
				uhc = UHC.objects.get(id = idUHC)
				operacionesUHC = Operacion.objects.filter(idUHC = uhc.id)
				parcelas = Parcelauhc.objects.filter(idUHC = uhc.id)
				parcelastotales = Parcela.objects.all()
				cultivoExpl = Cultivoexplotacion.objects.filter(idUHC = idUHC )
				if len(cultivoExpl) == 0:
					cultExplotacion = ''
					idCultivoExp = ''
				else:
					cultExplotacion = cultivoExpl[0]
					idCultivoExp = cultExplotacion.id
				numParcelas = len(parcelas)
				costeUHC = 0
				indicadorEvAmbiental = 0
				numOperaciones = 0
				aplicacionesUHC = Aplicacion.objects.filter(idUHC = idUHC).order_by('-fecha_Orden_tratamiento')
				analisisUHC = Analisis.objects.filter(idUHC = idUHC).order_by('-fecha_muestra')
				for o in operacionesUHC:
					operacion = Operacion.objects.get(id = o.id)
					indicadorEvAmbiental = indicadorEvAmbiental + operacion.cantidad * operacion.idInputOperacion.coefEmision
					costeUHC = costeUHC + operacion.idInputOperacion.costeUnitario
					numOperaciones = numOperaciones + 1
				parcelas = Parcelauhc.objects.filter(idUHC__in=listauhc)
				parcelastotales = Parcela.objects.all()
				analisis = Analisis.objects.filter(idUHC__in=listauhc)
				aplicaciones = Aplicacion.objects.filter(idUHC__in=listauhc)
				usuarios = UsuarioExplotacion.objects.filter(idExplotacion = id_Explotacion)
				listaus = []
				aplicadores = Aplicador.objects.all()
				maquinasusadas = Maquinaria.objects.all()
				datosClimaticos = DatosClimaticos.objects.filter(idExplotacion = id_Explotacion)
				datosClimaticos = datosClimaticos.extra(order_by=['-fecha'])
				provincias = Provincia.objects.all()
				
				context = RequestContext(request, {
					'lista_explotaciones':lista_Explotaciones,
					'explotacion':explotacion,
					'tipoOperaciones':tipoOperaciones,
					'aplicacionesUHC':aplicacionesUHC,
					'analisisUHC':analisisUHC,
					'muestras':muestras,
					'aplicadores':aplicadores,
					'maquinasusadas':maquinasusadas,
					'userid':userid,
					'indicadorEvAmbiental':indicadorEvAmbiental,
					'idUHC':idUHC,
					'cultivoExpl':cultivoExpl,
					'cultExplotacion':cultExplotacion,
					'idCultivoExp':idCultivoExp,
					'numParcelas':numParcelas,
					'costeUHC':costeUHC,
					'numOperaciones':numOperaciones,
					'uhcsExplotacion':uhcs,
					'uhc':uhc,
					'parcelas':parcelas,
					'parcelastotales':parcelastotales,
					'analisis':analisis,
					'aplicaciones':aplicaciones,
					'datosClimaticos':datosClimaticos,
					'provincias':provincias,
					'tecnico':tecnico,
				})
				
				return HttpResponse(template.render(context))
	
	
@login_required()
def generaInformePDF(request,id_Uhc):
	uhc = UHC.objects.get(id = id_Uhc)
	cultivoexplot = Cultivoexplotacion.objects.filter(idUHC = id_Uhc)
	operaciones = Operacion.objects.filter(idUHC = id_Uhc)
	aplicaciones = Aplicacion.objects.filter(idUHC = id_Uhc)
	parcelas = Parcelauhc.objects.filter(idUHC = id_Uhc)
	response = HttpResponse(content_type='application/pdf')
	#fechahoy = datetime.date.today()
	#fecha = str(fechahoy.day)+"_"+str(fechahoy.month)+" "+str(fechahoy.year)
	nombrePDF  = 'Informe.pdf'

	response['Content-Disposition'] = 'attachment; filename = %s'  % nombrePDF
	buffer = BytesIO()

	styles= {
        'observaciones': ParagraphStyle(
            'observaciones',
			fontName='Arial Narrow',
			bulletFontName = 'Arial Narrow',
			allowWidows = 1,
			alignment = 0,
			splitLongWords = 2,
			leading = 10,
			bulletFontSize = 9,
			fontSize = 7,
			textColor = black,
        ),
		'resumen': ParagraphStyle(
            'resumen',
			fontName='Arial Narrow',
			bulletFontName = 'Arial Narrow',
			allowWidows = 1,
			alignment = 0,
			splitLongWords = 2,
			leading = 12,
			bulletFontSize = 9,
			fontSize = 8,
			textColor = black,
        ),
        'reglamento': ParagraphStyle(
            'reglamento',
			fontName='Arial Narrow',
			bulletFontName = 'Arial Narrow',
			allowWidows = 1,
			alignment = 0,
			splitLongWords = 2,
			leading = 10,
			bulletFontSize = 9,
			fontSize = 9,
			textColor = black,
        ),
    }
	width, height = A4
	p = canvas.Canvas(response)

	p.setFont('Arial Narrow', 9)
	p = canvas.Canvas(response)
	
	p.setFont('Arial Narrow', 24)
 
	p.drawCentredString(4.3*inch, 770,'Informe de Evaluación ')
	
	p.setFont('Arial Narrow Bold', 10)
	p.drawCentredString(4.3*inch, 710,'Fecha: ')
	p.rect(50,620,500,80, fill=0)
	p.drawString(1*inch,680,"Explotación: ")
	p.drawString(1*inch,660,"Cultivo: ")
	p.drawString(1*inch,640,"UHC: ")
	p.drawString(1*inch,580,"Indicadores:")
	p.drawString(1*inch,480,"Operaciones:")
	p.drawString(1*inch,380,"Aplicaciones:")
	p.drawString(1*inch,300,"Parcelas:")
	p.setFont('Arial Narrow', 9)
	p.drawString(2*inch,680,uhc.idExplotacion.Razon_Social)
	p.drawString(2*inch,660,cultivoexplot[0].idCultivo.nombre)
	p.drawString(2*inch,640,uhc.nombre)
	p.setFont('Arial Narrow', 18)

	
	data1 = [[u"Indicador Evaluación Ambiental (Kg CO2e):",'','','','','','','','','','','','','Coste Asociado (€):','','','','','','','','','','',''],[uhc.indicadorEvAmbiental,'','','','','','','','','','','','',uhc.costeAsociado,'','','','','','','','','','','']]
	
	
	t=Table(data1,5*[0.25*inch],2*[0.35*inch])
	t.setStyle(TableStyle([
				('GRID',(0,0),(-1,-1),0.5,colors.black),
				('FONT',(0,0),(5,0),'Arial Narrow Bold'),
				('VALIGN',(0,0),(-1,0),'MIDDLE'),
				('FONT',(0,0),(24,0),'Arial Narrow'),
				('ALIGN',(0,0),(24,0),'CENTER'),
				('ALIGN',(0,1),(24,1),'CENTER'),
				('SIZE',(6,0),(8,0),10),
				('SIZE',(9,0),(12,0),8),
				('BACKGROUND',(0,0),(24,0),colors.Color(red=0.93,green=0.93,blue=0.93)),
				('FONT',(13,0),(24,0),'Arial Narrow'),
				('SIZE',(13,0),(24,0),10),
				('SPAN',(0,0),(12,0)),
				('SPAN',(0,1),(12,1)),

				('SPAN',(13,0),(24,0)),
				('SPAN',(13,1),(24,1)),
				 ]))
	t.wrapOn(p,width,height)
	pos = 510
	t.drawOn(p,70,pos)

	data2 = [[u"Fecha operación",'','','','Tipo de operación','','','','','','Input operación','','','','','','','Cantidad','','','Unidad','','Huella','','']]

	cont = 0
	for operacion in operaciones:
		fila = []
		fila.append(operacion.fecha_operacion)
		fila.append("")
		fila.append("")
		fila.append("")
		cult = ''
		tipo = operacion.idTipoOperacion.nombre
		if len(tipo) > 15:
			arrayCultivo = tipo.split();
			for x in range(0,int(len(arrayCultivo)/2)):
				cult = cult+arrayCultivo[x]+" "
				if x == (int(len(arrayCultivo)/2) -1):
					cult = cult+"\n"
			for x in range(int(len(arrayCultivo)/2),len(arrayCultivo)):
				cult = cult+arrayCultivo[x]+" "
			tipo = cult
		fila.append(tipo)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		tipo = operacion.idInputOperacion.input
		if len(tipo) > 15:
			arrayCultivo = tipo.split();
			for x in range(0,int(len(arrayCultivo)/2)):
				cult = cult+arrayCultivo[x]+" "
				if x == (int(len(arrayCultivo)/2) -1):
					cult = cult+"\n"
			for x in range(int(len(arrayCultivo)/2),len(arrayCultivo)):
				cult = cult+arrayCultivo[x]+" "
			tipo = cult
		fila.append(tipo)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append(operacion.cantidad)
		fila.append("")
		fila.append("")
		fila.append(operacion.unidad)
		fila.append("")
		fila.append(operacion.emisionesTotal)
		fila.append("")
		fila.append("")
		data2.append(fila)
		cont = cont + 1
	
	tam = 1 + cont
	t=Table(data2,5*[0.25*inch],tam*[0.50*inch])
	t.setStyle(TableStyle([
				('GRID',(0,0),(-1,-1),0.5,colors.black),
				('FONT',(0,0),(5,0),'Arial Narrow Bold'),
				('VALIGN',(0,0),(-1,0),'MIDDLE'),
				('FONT',(0,0),(24,0),'Arial Narrow'),
				('ALIGN',(0,0),(24,0),'CENTER'),
				('ALIGN',(0,1),(24,1),'CENTER'),
				('SIZE',(0,0),(24,0),8),
				('BACKGROUND',(0,0),(24,0),colors.Color(red=0.93,green=0.93,blue=0.93)),
				('FONT',(13,0),(24,0),'Arial Narrow'),
				('SIZE',(13,0),(24,0),10),
				('SPAN',(0,0),(3,0)),
				('SPAN',(4,0),(9,0)),
				('SPAN',(10,0),(16,0)),
				('SPAN',(17,0),(19,0)),
				('SPAN',(20,0),(21,0)),
				('SPAN',(22,0),(24,0)),
				 ]))
	for x in range(1, cont+1):
		t.setStyle(TableStyle([
			('FONT',(0,x),(16,x),'Arial Narrow'),
			('SIZE',(0,x),(24,x),8),
			('SPAN',(0,x),(3,x)),
			('SPAN',(4,x),(9,x)),
			('SPAN',(10,x),(16,x)),
			('SPAN',(17,x),(19,x)),
			('SPAN',(20,x),(21,x)),
			('SPAN',(22,x),(24,x)),
		]))
	t.wrapOn(p,width,height)
	pos = 400
	t.drawOn(p,70,pos)

	
	data2 = [[u"Fecha Aplicación",'','','','Aplicador','','','','','','','','','','Maquinaria','','','','','','','','','','']]

	cont = 0
	for aplicacion in aplicaciones:
		fila = []
		fila.append(aplicacion.fecha_Aplicacion)
		fila.append("")
		fila.append("")
		fila.append("")
		cult = ''
		tipo = aplicacion.aplicador.nombre+' '+aplicacion.aplicador.apellido1+' '+aplicacion.aplicador.apellido2
		if len(tipo) > 35:
			arrayCultivo = tipo.split();
			for x in range(0,int(len(arrayCultivo)/2)):
				cult = cult+arrayCultivo[x]+" "
				if x == (int(len(arrayCultivo)/2) -1):
					cult = cult+"\n"
			for x in range(int(len(arrayCultivo)/2),len(arrayCultivo)):
				cult = cult+arrayCultivo[x]+" "
			tipo = cult
		fila.append(tipo)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		tipo = aplicacion.maquinaria.TipoMaquina+' '+aplicacion.maquinaria.MarcaModelo+' '+aplicacion.maquinaria.numero_roma
		if len(tipo) > 35:
			arrayCultivo = tipo.split();
			for x in range(0,int(len(arrayCultivo)/2)):
				cult = cult+arrayCultivo[x]+" "
				if x == (int(len(arrayCultivo)/2) -1):
					cult = cult+"\n"
			for x in range(int(len(arrayCultivo)/2),len(arrayCultivo)):
				cult = cult+arrayCultivo[x]+" "
			tipo = cult
		fila.append(tipo)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		data2.append(fila)
		cont = cont + 1
	
	tam = 1 + cont
	t=Table(data2,5*[0.25*inch],tam*[0.35*inch])
	t.setStyle(TableStyle([
				('GRID',(0,0),(-1,-1),0.5,colors.black),
				('FONT',(0,0),(5,0),'Arial Narrow Bold'),
				('VALIGN',(0,0),(-1,0),'MIDDLE'),
				('FONT',(0,0),(24,0),'Arial Narrow'),
				('ALIGN',(0,0),(24,0),'CENTER'),
				('ALIGN',(0,1),(24,1),'CENTER'),
				('SIZE',(0,0),(24,0),8),
				('BACKGROUND',(0,0),(24,0),colors.Color(red=0.93,green=0.93,blue=0.93)),
				('FONT',(13,0),(24,0),'Arial Narrow'),
				('SIZE',(13,0),(24,0),10),
				('SPAN',(0,0),(3,0)),
				('SPAN',(4,0),(13,0)),
				('SPAN',(14,0),(24,0)),
				 ]))
	for x in range(1, cont+1):
		t.setStyle(TableStyle([
			('FONT',(0,x),(16,x),'Arial Narrow'),
			('SIZE',(0,x),(24,x),8),
			('SPAN',(0,x),(3,x)),
			('SPAN',(4,x),(13,x)),
			('SPAN',(14,x),(24,x)),
		]))
	t.wrapOn(p,width,height)
	pos = 320
	t.drawOn(p,70,pos)
	
	
	
	data2 = [[u"Parcela",'','','','Código','','','','','','Superficie','','','','Descripcion','','','','','','Cultivo','','','','']]

	cont = 0
	for parcela in parcelas:
		fila = []
		fila.append(parcela.idParcela.nombre)
		fila.append("")
		fila.append("")
		fila.append("")
		codigo = parcela.idParcela.provincia.CodProvincia+'-'+parcela.idParcela.municipio.CodMunicipio+'-'+parcela.idParcela.poligono+'-'+parcela.idParcela.parcela+'-'+parcela.idParcela.recinto
		fila.append(codigo)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append(parcela.idParcela.superficie_hectareas)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append(parcela.idParcela.descripcion)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append(parcela.idParcela.idcultivo.nombre)
		fila.append("")
		fila.append("")
		fila.append("")
		fila.append("")
		data2.append(fila)
		cont = cont + 1
	
	tam = 1 + cont
	t=Table(data2,5*[0.25*inch],tam*[0.35*inch])
	t.setStyle(TableStyle([
				('GRID',(0,0),(-1,-1),0.5,colors.black),
				('FONT',(0,0),(5,0),'Arial Narrow Bold'),
				('VALIGN',(0,0),(-1,0),'MIDDLE'),
				('FONT',(0,0),(24,0),'Arial Narrow'),
				('ALIGN',(0,0),(24,0),'CENTER'),
				('ALIGN',(0,1),(24,1),'CENTER'),
				('SIZE',(0,0),(24,0),8),
				('BACKGROUND',(0,0),(24,0),colors.Color(red=0.93,green=0.93,blue=0.93)),
				('FONT',(13,0),(24,0),'Arial Narrow'),
				('SIZE',(13,0),(24,0),10),
				('SPAN',(0,0),(3,0)),
				('SPAN',(4,0),(9,0)),
				('SPAN',(10,0),(13,0)),
				('SPAN',(14,0),(19,0)),
				('SPAN',(20,0),(24,0)),
				 ]))
	for x in range(1, cont+1):
		t.setStyle(TableStyle([
			('FONT',(0,x),(16,x),'Arial Narrow'),
			('SIZE',(0,x),(24,x),8),
			('SPAN',(0,x),(3,x)),
			('SPAN',(4,x),(9,x)),
			('SPAN',(10,x),(13,x)),
			('SPAN',(14,x),(19,x)),
			('SPAN',(20,x),(24,x)),
		]))
	t.wrapOn(p,width,height)
	pos = 220
	t.drawOn(p,70,pos)
	p.showPage()
	
	p.save()
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
	
@login_required()	
def VistaAplicacionTecnico(request,id_Aplicacion):
	 
    if request.user.is_authenticated(): 
        if not request.user.is_staff:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'A':
                return HttpResponseRedirect('/administrador/aplicacion/'+id_Aplicacion)
            else:
				aplicacion = Aplicacion.objects.get(id=id_Aplicacion)
				tecnico = Tecnico.objects.get(id = request.user.id)
				lista_Explotaciones = tecnico.explotaciones_asignadas
				productos = Producto_aplicado.objects.filter(aplicacion=id_Aplicacion)
				aplicadores = Aplicador.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				maq_exp = MaquinaExplotacion.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				uhcs = UHC.objects.filter(idExplotacion = aplicacion.idUHC.idExplotacion)
				uhcParcelas = Parcelauhc.objects.filter(idUHC = aplicacion.idUHC)
				
				maquinas = []
				for maq in maq_exp:
					maquinas.append(maq.idMaquina)
			   
				template = loader.get_template('citagro/Administrador/aplicacion.html')
				   
				context = RequestContext(request, {
						'aplicacion':aplicacion,
						'productos':productos,
						'aplicadores':aplicadores,
						'maquinaria':maquinas,
						'uhcs':uhcs,
						'lista_explotaciones':lista_Explotaciones,
						'uhcParcelas':uhcParcelas,
						'tecnico':tecnico,

				})
				return HttpResponse(template.render(context))
	
@login_required()	
def VistaOperacionTecnico(request,id_Operacion):
    tecnico = Tecnico.objects.get(id = request.user.id)
    administrador = Administrador.objects.get(id = tecnico.idAdmin.id)	
    operacion = Operacion.objects.get(id=id_Operacion)
    lista_Explotaciones = tecnico.explotaciones_asignadas
    tipoP = ''
    uhcParcelas = Parcelauhc.objects.filter(idUHC = operacion.idUHC)
    uhcs = UHC.objects.filter(idExplotacion = operacion.idExplotacion)
    tipoId = "";
    tipoNombr = "";
    template = loader.get_template('citagro/Administrador/operacion.html')
   
    context = RequestContext(request, {
		    'operacion':operacion,
			'uhcs':uhcs,
			'lista_explotaciones':lista_Explotaciones,
			'tipoP':tipoP,
			'uhcParcelas':uhcParcelas,
			'tipoId':tipoId,
			'tipoNombr':tipoNombr,
			'tecnico':tecnico,

    })
    return HttpResponse(template.render(context))
	
@login_required()
def VistaAnalisisTecnico(request,id_Analisis):
    tecnico = Tecnico.objects.get(id = request.user.id)
    administrador = Administrador.objects.get(id = tecnico.idAdmin.id)	
    analisis = Analisis.objects.get(id=id_Analisis)
    lista_Explotaciones = tecnico.explotaciones_asignadas
    documentos = Document.objects.filter(idAnalisis=id_Analisis)
    documento = "";
    uhcParcelas = Parcelauhc.objects.filter(idUHC = analisis.idUHC)
    uhcs = UHC.objects.filter(idExplotacion = analisis.idExplotacion)
    
    if len(documentos) > 0:
        documento = documentos[0]
		
	
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
        	newdoc = Document(filename = request.FILES['docfile'].name,docfile = request.FILES['docfile'],idAnalisis = analisis)
        	newdoc.save(form)
        	return HttpResponseRedirect('/tecnico/analisis/'+id_Analisis)
    else:
        form = UploadForm()
        template = loader.get_template('citagro/Administrador/analisis.html')
       
        context = RequestContext(request, {
            'form':form,
		    'analisis':analisis,
			'lista_explotaciones':lista_Explotaciones,
			'tecnico':tecnico,
			'documentos':documentos,
			'documento':documento,
			'uhcs':uhcs,
			'uhcParcelas':uhcParcelas,
        })
        return HttpResponse(template.render(context))
		
@login_required()
def VistaTecnicoMuestreo(request,id_Muestra):
    tecnico = Tecnico.objects.get(id = request.user.id)
    muestra = Muestreo.objects.get(id=id_Muestra)
    lista_Explotaciones = tecnico.explotaciones_asignadas
   
    uhcParcelas = Parcelauhc.objects.filter(idUHC = muestra.idUHC)
    uhcs = UHC.objects.filter(idExplotacion = muestra.idExplotacion)

    fenologia = muestra_fenologia.objects.filter(idMuestra = muestra.id)
    insect = muestra_insetos.objects.filter(idMuestra = muestra.id)
    insectos = ""
    if len(insect) > 0:
        insectos = insect[0]
    trampas = muestra_trampas.objects.filter(idMuestra = muestra.id)
    brotes = muestra_brotes.objects.filter(idMuestra = muestra.id)
    zeuzera = muestra_zeuzera.objects.filter(idMuestra = muestra.id)
    enf = muestra_enfermedades.objects.filter(idMuestra = muestra.id)
    enfermedades = ""
    if len(enf) > 0:
        enfermedades = enf[0]
    template = loader.get_template('citagro/Administrador/muestreo.html')
    context = RequestContext(request, {
		    'muestreo':muestra,
			'lista_explotaciones':lista_Explotaciones,
			'uhcs':uhcs,
			'uhcParcelas':uhcParcelas,
            'tecnico':tecnico,
			'fenologia':fenologia,
			'insectos':insectos,
			'trampas':trampas,
			'brotes':brotes,
			'zeuzera':zeuzera,
			'enfermedades':enfermedades,
        })
    return HttpResponse(template.render(context))
	
@login_required()
def explotacionesAsignadas(request):
    lista_Explotaciones_usuario = Explotacion.objects.raw('''SELECT * from citagro_usuarioexplotacion join citagro_explotacion  
	                                                      where citagro_usuarioexplotacion.idUsuario_id = %s 
														  and citagro_usuarioexplotacion.idExplotacion_id = citagro_explotacion.id''', [request.user.id])
    
	
    count = len(list(lista_Explotaciones_usuario))
    template = loader.get_template('citagro/Tecnico/ExplotacionesAsignadas.html')
    context = RequestContext(request, {
        'administradorCitagro': request.user,
		'lista_explotaciones_usuario': lista_Explotaciones_usuario,
		'count':count,
    })
	
    return HttpResponse(template.render(context))
	
@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='citagro/password_change.html',
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):

    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/')
    else:
        form = password_change_form(user=request.user)
    
    admin = ""
    lista_Explotaciones = []	
    if request.user.is_staff:
	    template_name='citagro/password_change2.html',
    else:
        perfilUsuario = Perfil.objects.get(user_id = request.user.id)
        tipoId = perfilUsuario.TipoUsuario	
        if tipoId == 'A':
            admin = Administrador.objects.get(id = request.user.id)	
            lista_Explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)	
        else:
            tecnico = Tecnico.objects.get(id = request.user.id)
            lista_Explotaciones = tecnico.explotaciones_asignadas    
		
    context = {
        'form': form,
	    'administrador':admin,
		'lista_explotaciones':lista_Explotaciones,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
							
@login_required()
def cambiaUsuario(request):
    admin = ""
    lista_Explotaciones = []
    if request.user.is_authenticated(): 
        if request.user.is_staff:
            template=loader.get_template('citagro/Administrador/cambiaUsuario2.html')
        else:
            perfilUsuario = Perfil.objects.get(user_id = request.user.id)
            tipoId = perfilUsuario.TipoUsuario			
            if tipoId == 'A':
                admin = Administrador.objects.get(id = request.user.id)	
                lista_Explotaciones = Explotacion.objects.filter(idAdmin=request.user.id)	
            else:
                tecnico = Tecnico.objects.get(id = request.user.id)
                lista_Explotaciones = tecnico.explotaciones_asignadas    
            template = loader.get_template('citagro/Administrador/cambiaUsuario.html')
    
    context = RequestContext(request, {
			'lista_explotaciones':lista_Explotaciones,
			'administrador':admin,
        })
    return HttpResponse(template.render(context))

		

class AdministradorList(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer


class AdministradorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
	
class TecnicoList(generics.ListCreateAPIView):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer
	
class TecnicoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer

class TiposoperacionList(generics.ListCreateAPIView):
    queryset = Tiposoperacion.objects.all()
    serializer_class = TiposoperacionSerializer
	
class TiposoperacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tiposoperacion.objects.all()
    serializer_class = TiposoperacionSerializer

class InputoperacionList(generics.ListCreateAPIView):
    queryset = Inputoperacion.objects.all()
    serializer_class = InputoperacionSerializer
	
class InputoperacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inputoperacion.objects.all()
    serializer_class = InputoperacionSerializer
	
class ExplotacionList(generics.ListCreateAPIView):
    queryset = Explotacion.objects.all()
    serializer_class = ExplotacionSerializer
	
class ExplotacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Explotacion.objects.all()
    serializer_class = ExplotacionSerializer
	
class DatosClimaticosList(generics.ListCreateAPIView):
    queryset = DatosClimaticos.objects.all()
    serializer_class = DatosClimaticosSerializer
	
class DatosClimaticosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DatosClimaticos.objects.all()
    serializer_class = DatosClimaticosSerializer
	
class MaquinariaList(generics.ListCreateAPIView):
    queryset = Maquinaria.objects.all()
    serializer_class = MaquinariaSerializer
	
class MaquinariaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Maquinaria.objects.all()
    serializer_class = MaquinariaSerializer
	
class UsuariosList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer
	
class UsuariosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer
	
class ProvinciaList(generics.ListCreateAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
	
class ProvinciaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
	
class MunicipioList(generics.ListCreateAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
	
class MunicipioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
	
class AplicadorList(generics.ListCreateAPIView):
    queryset = Aplicador.objects.all()
    serializer_class = AplicadorSerializer
	
class AplicadorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aplicador.objects.all()
    serializer_class = AplicadorSerializer
	
class UHCList(generics.ListCreateAPIView):
    queryset = UHC.objects.all()
    serializer_class = UHCSerializer
	
class UHCDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UHC.objects.all()
    serializer_class = UHCSerializer
	
class AnalisisList(generics.ListCreateAPIView):
    queryset = Analisis.objects.all()
    serializer_class = AnalisisSerializer
	
class AnalisisDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Analisis.objects.all()
    serializer_class = AnalisisSerializer
	
class ParcelaList(generics.ListCreateAPIView):
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer
	
class ParcelaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parcela.objects.all()
    serializer_class = ParcelaSerializer

class ParcelauhcList(generics.ListCreateAPIView):
    queryset = Parcelauhc.objects.all()
    serializer_class = ParcelauhcSerializer
	
class ParcelauhcDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parcelauhc.objects.all()
    serializer_class = ParcelauhcSerializer

class CultivoList(generics.ListCreateAPIView):
    queryset = Cultivo.objects.all()
    serializer_class = CultivoSerializer
	
class CultivoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cultivo.objects.all()
    serializer_class = CultivoSerializer

class CultivoexplotacionList(generics.ListCreateAPIView):
    queryset = Cultivoexplotacion.objects.all()
    serializer_class = CultivoexplotacionSerializer
	
class CultivoexplotacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cultivoexplotacion.objects.all()
    serializer_class = CultivoexplotacionSerializer
	
class AplicacionList(generics.ListCreateAPIView):
    queryset = Aplicacion.objects.all()
    serializer_class = AplicacionSerializer
	
class AplicacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aplicacion.objects.all()
    serializer_class = AplicacionSerializer

class ProductoList(generics.ListCreateAPIView):
    queryset = Producto_aplicado.objects.all()
    serializer_class = ProductoSerializer
	
class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto_aplicado.objects.all()
    serializer_class = ProductoSerializer

class PerfilList(generics.ListCreateAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
	
class PerfilDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
	
class UsuarioExplotacionList(generics.ListCreateAPIView):
    queryset = UsuarioExplotacion.objects.all()
    serializer_class = UsuarioExplotacionSerializer
	
class UsuarioExplotacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UsuarioExplotacion.objects.all()
    serializer_class = UsuarioExplotacionSerializer
	
class MaquinaExplotacionList(generics.ListCreateAPIView):
    queryset = MaquinaExplotacion.objects.all()
    serializer_class = MaquinaExplotacionSerializer
	
class MaquinaExplotacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MaquinaExplotacion.objects.all()
    serializer_class = MaquinaExplotacionSerializer
	
class OperacionList(generics.ListCreateAPIView):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer
	
class OperacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer
	
class op_podaList(generics.ListCreateAPIView):
    queryset = op_poda.objects.all()
    serializer_class = op_podaSerializer
	
class op_podaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = op_poda.objects.all()
    serializer_class = op_podaSerializer
	
class op_laboresList(generics.ListCreateAPIView):
    queryset = op_labores.objects.all()
    serializer_class = op_laboresSerializer
	
class op_laboresDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = op_labores.objects.all()
    serializer_class = op_laboresSerializer
	
class op_fertilizacionList(generics.ListCreateAPIView):
    queryset = op_fertilizacion.objects.all()
    serializer_class = op_fertilizacionSerializer
	
class op_fertilizacionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = op_fertilizacion.objects.all()
    serializer_class = op_fertilizacionSerializer
	
class op_riegoList(generics.ListCreateAPIView):
    queryset = op_riego.objects.all()
    serializer_class = op_riegoSerializer
	
class op_riegoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = op_riego.objects.all()
    serializer_class = op_riegoSerializer
	
class op_recoleccionList(generics.ListCreateAPIView):
    queryset = op_recoleccion.objects.all()
    serializer_class = op_recoleccionSerializer
	
class op_recoleccionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = op_recoleccion.objects.all()
    serializer_class = op_recoleccionSerializer
	
class MuestreoList(generics.ListCreateAPIView):
    queryset = Muestreo.objects.all()
    serializer_class = MuestreoSerializer
	
class MuestreoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Muestreo.objects.all()
    serializer_class = MuestreoSerializer
	
class muestra_fenologiaList(generics.ListCreateAPIView):
    queryset = muestra_fenologia.objects.all()
    serializer_class = muestra_fenologiaSerializer
	
class muestra_fenologiaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = muestra_fenologia.objects.all()
    serializer_class = muestra_fenologiaSerializer	
	
class muestra_insetosList(generics.ListCreateAPIView):
    queryset = muestra_insetos.objects.all()
    serializer_class = muestra_insetosSerializer
	
class muestra_insetosDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = muestra_insetos.objects.all()
    serializer_class = muestra_insetosSerializer

class muestra_trampasList(generics.ListCreateAPIView):
    queryset = muestra_trampas.objects.all()
    serializer_class = muestra_trampasSerializer
	
class muestra_trampasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = muestra_trampas.objects.all()
    serializer_class = muestra_trampasSerializer

class muestra_brotesList(generics.ListCreateAPIView):
    queryset = muestra_brotes.objects.all()
    serializer_class = muestra_brotesSerializer
	
class muestra_brotesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = muestra_brotes.objects.all()
    serializer_class = muestra_brotesSerializer		

class muestra_zeuzeraList(generics.ListCreateAPIView):
    queryset = muestra_zeuzera.objects.all()
    serializer_class = muestra_zeuzeraSerializer
	
class muestra_zeuzeraDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = muestra_zeuzera.objects.all()
    serializer_class = muestra_zeuzeraSerializer	

class muestra_enfermedadesList(generics.ListCreateAPIView):
    queryset = muestra_enfermedades.objects.all()
    serializer_class = muestra_enfermedadesSerializer
	
class muestra_enfermedadesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = muestra_enfermedades.objects.all()
    serializer_class = muestra_enfermedadesSerializer		
	

