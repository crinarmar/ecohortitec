# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

booleano = (
		('SI', 'Si'),
		('NO', 'No'),
    )

class Perfil(models.Model):
	USUARIO = (
		('A', 'Usuario Administrador'),
		('T', 'Usuario Tecnico'),
	)
	user = models.ForeignKey(User,related_name='perfil')
	TipoUsuario = models.CharField(max_length=1,
                                   choices=USUARIO,
                                   default='A')
	def __unicode__(self):
		texto = self.TipoUsuario
		return texto
								   
class Provincia(models.Model):
	CodProvincia = models.CharField(max_length=20)
	Provincia = models.CharField(max_length=20)
	
	class Meta:
		ordering = ['CodProvincia']
	
	def __unicode__(self):
		texto = self.Provincia
		return texto
		
class Municipio(models.Model):
	
	CodMunicipio = models.CharField(max_length=20)
	CodCatastral = models.CharField(max_length=20)
	Municipio = models.CharField(max_length=80)
	idProvincia = models.ForeignKey(Provincia,related_name='municipios')
	
	class Meta:
		ordering = ['idProvincia','CodMunicipio']
	
	def __unicode__(self):
		texto = self.Municipio
		return texto

class Administrador(models.Model):
	Nombre = models.CharField(max_length=200)
	Apellido1 = models.CharField(max_length=200)
	Apellido2 = models.CharField(max_length=200)
	NIF = models.CharField(max_length=9)
	Domicilio = models.CharField(max_length=250)
	Municipio = models.ForeignKey(Municipio)
	Provincia = models.ForeignKey(Provincia)
	CP = models.CharField(max_length=5)
	email = models.EmailField(max_length=75)
	Telefono1 = models.CharField(max_length=9)
	Telefono2 = models.CharField(max_length=9,blank=True)
	Fax = models.CharField(max_length=9,blank=True)
	fecha_ingreso = models.DateField(auto_now_add=True)
	ropo = models.CharField(max_length=12,blank=True)
	def n_explotaciones(self):
		explotaciones = Explotacion.objects.filter(idAdmin = self.id)
		n_exp = 0
		for explotacion in explotaciones:
			n_exp = n_exp + 1
		return n_exp
		
	def n_tecnicos(self):
		tecnicos = Tecnico.objects.filter(idAdmin = self.id)
		n_tec = 0
		for tecnico in tecnicos:
			n_tec = n_tec + 1
		return n_tec
	def usuario(self):
		return User.objects.get(id = self.id)
	
	def __unicode__(self):
		texto = self.Nombre+" "+self.Apellido1+" "+self.Apellido2
		return texto



class Tecnico(models.Model):
	Nombre = models.CharField(max_length=200)
	Apellido1 = models.CharField(max_length=200)
	Apellido2 = models.CharField(max_length=200)
	NIF = models.CharField(max_length=9)
	Domicilio = models.CharField(max_length=250)
	Municipio = models.ForeignKey(Municipio)
	Provincia = models.ForeignKey(Provincia)
	CP = models.CharField(max_length=5)
	email = models.EmailField(max_length=75)
	Telefono1 = models.CharField(max_length=9)
	Telefono2 = models.CharField(max_length=9,blank=True)
	Fax = models.CharField(max_length=9,blank=True)
	fecha_ingreso = models.DateField(auto_now_add=True)
	ropo = models.CharField(max_length=12,blank=True)
	idAdmin = models.ForeignKey(Administrador, related_name='tecnicos')
	activo = models.CharField(max_length=2,choices=booleano, default='SI')
	def usuario(self):
		return User.objects.get(id = self.id)
	def explotaciones_asignadas(self):
		explotaciones = UsuarioExplotacion.objects.filter(idUsuario = self.id)
		list_ids = []
		for explotacion in explotaciones:
			list_ids.append(explotacion.idExplotacion.id)
		return Explotacion.objects.filter(id__in = list_ids)
	def __unicode__(self):
		texto = self.Nombre+" "+self.Apellido1+" "+self.Apellido2
		return texto
		
class Explotacion(models.Model):
	Razon_Social = models.CharField(max_length=200)
	cif_nif = models.CharField(max_length=9)
	Domicilio = models.CharField(max_length=250)
	Localidad = models.ForeignKey(Municipio)
	Provincia = models.ForeignKey(Provincia)
	CP = models.CharField(max_length=5)
	idAdmin = models.ForeignKey(Administrador, related_name ='explotaciones')
	
	def tecnicos_asignados(self):
		usuarios = UsuarioExplotacion.objects.filter(idExplotacion = self.id)
		list_ids = []
		for usuario in usuarios:
			list_ids.append(usuario.idUsuario)
		return Tecnico.objects.filter(id__in = list_ids)
		
   
	def __unicode__(self):
		texto = self.Razon_Social
		return texto
	
class RepositorioImagenes (models.Model):
	
	imagen = models.ImageField()	

class Cultivo(models.Model):
	nombre = models.CharField(max_length=200)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()
	descripcion = models.TextField()
	localizacion = models.CharField(max_length=200)
	


class UsuarioExplotacion(models.Model):
	idUsuario = models.ForeignKey(Tecnico, related_name ='usuariosExplotaciones')
	idExplotacion = models.ForeignKey(Explotacion,related_name ='usuarios')
	def __unicode__(self):
		return str(self.id)


	
class DatosClimaticos(models.Model):
	
	EstacionClimatica = models.CharField(max_length=200)
	Temperatura = models.DecimalField(max_digits=5, decimal_places=1)
	TempMax= models.DecimalField(max_digits=5, decimal_places=1)
	TempMin = models.DecimalField(max_digits=5, decimal_places=1)
	TempMed = models.DecimalField(max_digits=5, decimal_places=1)
	Humedad = models.IntegerField()
	HumMax = models.IntegerField()
	HumMin = models.IntegerField()
	HumMed = models.IntegerField()
	Precipitacion = models.DecimalField(max_digits=5, decimal_places=3)
	fecha = models.DateField()
	idExplotacion = models.ForeignKey(Explotacion, related_name ='datosClimaticos')
	
	def __unicode__(self):
		return str(self.id)
	
	
class Maquinaria(models.Model):
	
	numero_roma = models.CharField(max_length=200)
	fecha_adquisicion = models.DateField()
	fecha_revision = models.DateField()
	TipoMaquina = models.CharField(max_length=200) 
	MarcaModelo = models.CharField(max_length=200)
	idAdmin = models.ForeignKey(Administrador,related_name ='maquinaria')
	activo = models.CharField(max_length=2,choices=booleano, default='SI')
	
	def explotacion_asignada(self):
		explotaciones = MaquinaExplotacion.objects.filter(idMaquina = self.id)
		list_ids = []
		for explotacion in explotaciones:
			list_ids.append(explotacion.idExplotacion.id)
		return Explotacion.objects.filter(id__in = list_ids)
	
	def __unicode__(self):
		return self.TipoMaquina+"-"+self.MarcaModelo+"-"+self.numero_roma
		
class MaquinaExplotacion(models.Model):
	idMaquina = models.ForeignKey(Maquinaria, related_name = 'explotaciones')
	idExplotacion = models.ForeignKey(Explotacion, related_name ='maquinarias')
	
class Aplicador(models.Model):
	
	nombre = models.CharField(max_length=200)
	apellido1 = models.CharField(max_length=200,blank=True)
	apellido2 = models.CharField(max_length=200,blank=True)
	dni = models.CharField(max_length=9)
	fecha_validez = models.DateField()
	fecha_expedicion = models.DateField()
	razon_social = models.CharField(max_length=200)
	activo = models.CharField(max_length=2,choices=booleano, default='SI')
	APLICA = (
        (1, 'Empresa Aplicadora'),
        (2, 'Persona Fisica'),
    )
	Aplicador = models.CharField(max_length=1,
                                   choices=APLICA,
                                   default=2)
								   
	Telefono = models.CharField(max_length=9,blank=True)
	
	Fax = models.CharField(max_length=9,blank=True)
	
	email = models.EmailField(max_length=75,blank=True)

	idExplotacion = models.ForeignKey(Explotacion, related_name ='aplicadores')
	
	def __unicode__(self):
		return self.nombre+" "+self.apellido1+" "+self.apellido2+" ("+self.dni+")"
	
class UHC(models.Model):
	nombre = models.CharField(max_length=200)
	idExplotacion = models.ForeignKey(Explotacion, related_name ='uhcs')
	costeAsociado = models.DecimalField(max_digits=10, decimal_places=2,blank = True,default = '0')
	indicadorEvAmbiental = models.DecimalField(max_digits=10, decimal_places=5,blank = True,default = '0')
	superficie_hectareas = models.DecimalField(max_digits=10, decimal_places=5,blank = True,default = '0')
	def parcelas_asignadas(self):
		parcelas = Parcelauhc.objects.filter(idUHC = self.id)
		list_ids = []
		for parcela in parcelas:
			list_ids.append(parcela.id)
		return Parcela.objects.filter(id__in = list_ids)
	def __unicode__(self):
		return self.nombre
	
class Cultivoexplotacion(models.Model):
	idCultivo = models.ForeignKey(Cultivo, related_name ='cultivoExp')
	idExplotacion = models.ForeignKey(Explotacion, related_name ='ExplotacioncultivoExp')
	idUHC = models.ForeignKey(UHC, related_name ='uhcExplotacionCultivo')
	superficieCultivo = models.DecimalField(max_digits=10, decimal_places=5,blank=True)
	
	
	

class Analisis(models.Model):
	TA = (
        ("SUELO", 'Suelo'),
		("AGUA", 'Agua'),
		("FOLIAR", 'Foliar'),
		("MULTIRRESIDUOS", 'Multirresiduos'),
    )
	fecha_muestra = models.DateField()
	idUHC = models.ForeignKey(UHC, related_name ='analisis')
	idExplotacion = models.ForeignKey(Explotacion,related_name = 'analisisExplotacion')
	tipo = models.CharField(max_length=16,
                                   choices=TA,
                                   default="SUELO")
	tecnico = models.ForeignKey(Tecnico,related_name='TecnicoAnalisis')
	horas = models.DecimalField(max_digits=5, decimal_places=2)
	descripcion = models.TextField(blank=True)
	laboratorio = models.CharField(max_length=200)
	numero_informe = models.IntegerField()
	fecha_emision = models.DateField()
	observaciones = models.TextField(blank=True)
	acciones = models.TextField(blank=True)
	
	#Suelo
	s_t_arcilla = models.DecimalField(max_digits=3, decimal_places=2).blank=True
	s_t_limos = models.DecimalField(max_digits=3, decimal_places=2).blank=True
	s_t_arena = models.DecimalField(max_digits=3, decimal_places=2).blank=True
	s_t_ph = models.DecimalField(max_digits=10, decimal_places=1).blank=True
	s_t_ce = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	s_pctmo = models.DecimalField(max_digits=3, decimal_places=2).blank=True
	s_pctcalizatotal = models.DecimalField(max_digits=3, decimal_places=2).blank=True
	s_cic = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	s_n = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	s_p = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	s_k = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	
	#Agua
	a_cloro = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	
	#Foliar
	f_n = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	f_p = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	f_k = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	f_b = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	f_mg = models.DecimalField(max_digits=10, decimal_places=4).blank=True
	
class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')
	filename = models.CharField(max_length=100)
	idAnalisis = models.ForeignKey(Analisis, related_name='documento')

	

	
class Multiresiduos(models.Model):

	r_p_ma = models.CharField(max_length=200)
	r_p_valor = models.DecimalField(max_digits=3, decimal_places=2)
	r_p_umbral = models.DecimalField(max_digits=3, decimal_places=2)
	r_p_comentarios = models.TextField().blank=True
	analisis = models.ForeignKey(Analisis)
	
	
class Muestreo(models.Model):

	idUHC = models.ForeignKey(UHC, related_name ='muestreo')
	fecha_muestreo = models.DateField()
	observaciones = models.TextField(blank=True)
	tecnico = models.ForeignKey(Tecnico,related_name='TecnicoMuestra')
	horas = models.DecimalField(max_digits=5, decimal_places=2)
	idExplotacion = models.ForeignKey(Explotacion,related_name='muestrasExplotacion')
	
class muestra_fenologia(models.Model):
	idMuestra = models.ForeignKey(Muestreo,related_name='fenologia')
	muestra_a = models.IntegerField(blank=True)
	muestra_b = models.IntegerField(blank=True)
	muestra_c = models.IntegerField(blank=True)
	muestra_d = models.IntegerField(blank=True)
	muestra_e = models.IntegerField(blank=True)
	muestra_f = models.IntegerField(blank=True)
	muestra_g = models.IntegerField(blank=True)
	muestra_h = models.IntegerField(blank=True)
	muestra_i = models.IntegerField(blank=True)
	

	
class muestra_insetos(models.Model):
	idMuestra = models.ForeignKey(Muestreo,related_name='insectos')
	coccinelidos = models.IntegerField(blank=True)
	neuropteros = models.IntegerField(blank=True)
	
class muestra_brotes(models.Model):
	idMuestra = models.ForeignKey(Muestreo,related_name='brotes')
	carpocapsa = models.IntegerField(blank=True)
	acaros = models.IntegerField(blank=True)
	pulgones = models.IntegerField(blank=True)
	
class muestra_zeuzera(models.Model):
	idMuestra = models.ForeignKey(Muestreo,related_name='zeuzera')
	zeuzera = models.IntegerField(blank=True)
	
class muestra_enfermedades(models.Model):
	idMuestra = models.ForeignKey(Muestreo,related_name='enfermedades')
	bacteriosis = models.IntegerField(blank=True)
	antracnosis = models.IntegerField(blank=True)
	antracnosis_2 = models.IntegerField(blank=True)

class muestra_trampas(models.Model):
	idMuestra = models.ForeignKey(Muestreo,related_name='trampas')
	carpocapsa_p1 = models.IntegerField(blank=True)
	carpocapsa_p2 = models.IntegerField(blank=True)
	carpocapsa_p3 = models.IntegerField(blank=True)
	carpocapsa_p4 = models.IntegerField(blank=True)
	carpocapsa_p5 = models.IntegerField(blank=True)
	carpocapsa_p6 = models.IntegerField(blank=True)

	
class Tiposoperacion(models.Model):
	nombre = models.CharField(max_length=200)
	orden = models.IntegerField()

class Inputoperacion(models.Model):
	input = models.CharField(max_length=200)
	idTipoOp = models.ForeignKey(Tiposoperacion,related_name = 'inputTipo')
	coefEmision = models.DecimalField(max_digits=10, decimal_places=5,blank=True)
	cantidad = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	coefAsignacion = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	costeUnitario = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	unidad = models.CharField(max_length=200)
	unidadCoef = models.CharField(max_length=200)
	nombreTipo = models.CharField(max_length=200,blank=True)

	
class Operacion(models.Model):

	tecnico = models.ForeignKey(Tecnico,related_name='TecnicoOperacion')
	horas = models.DecimalField(max_digits=5, decimal_places=2)
	idUHC = models.ForeignKey(UHC, related_name ='operaciones')
	fecha_operacion = models.DateField()
	observaciones = models.TextField(blank=True)
	idExplotacion = models.ForeignKey(Explotacion,related_name='operacionesExplotacion')
	idTipoOperacion = models.ForeignKey(Tiposoperacion,related_name='operacionesTipo')
	idInputOperacion = models.ForeignKey(Inputoperacion,related_name='operacionesInput')
	coefEmision = models.DecimalField(max_digits=10, decimal_places=5,blank=True)
	cantidad = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	coefAsignacion = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	costeUnitario = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	unidad = models.CharField(max_length=200,blank=True)
	unidadCoef = models.CharField(max_length=200,blank=True)
	emisionesTotal = models.DecimalField(max_digits=10, decimal_places=5,blank=True)
	costeTotal = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
	
	def __unicode__(self):
		return str(self.id)						   
								   
class op_poda(models.Model):
	idOperacion = models.ForeignKey(Operacion,related_name='poda')
	tipoP = (
        ("FORMACION", 'Poda de formación'),
		("PRODUCCION", 'Poda de producción'),
		("REJUVENECIMIENTO", 'Poda de rejuvenecimiento'),
		("ACLAREO", 'Aclareo'),
    )
	TipoPoda = models.CharField(max_length=100,
                                   choices=tipoP,
                                   default="FORMACION")
	Duracion = models.IntegerField(blank=True)
	Herramienta = models.CharField(max_length=200,blank=True)
	Producto = models.CharField(max_length=200,blank=True)
	Fecha_eliminacion = models.DateField()
	Modo_eliminacion = models.CharField(max_length=200,blank=True)
	def existeFecha(self):
		return self.Fecha_eliminacion.year != 1900
	
class op_labores(models.Model):
	idOperacion = models.ForeignKey(Operacion,related_name='labores')
	tipoAp = (
        ("CULTIVADOR", 'Cultivador'),
		("DISCOS", 'Arado discos'),
		("VERTEDERA", 'Arado vertedera'),
		("DESBROZADOR", 'Desbrozador'),
    )
	apero = models.CharField(max_length=100,
                                   choices=tipoAp,
                                   default="CULTIVADOR")
	distribucion = models.CharField(max_length=200,blank=True)
	superficie_labrada = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
	profundidad_labor = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
	justificacion = models.CharField(max_length=200,blank=True)
	empresa = models.CharField(max_length=200,blank=True)
	
class op_fertilizacion(models.Model):
	idOperacion = models.ForeignKey(Operacion,related_name='fertilizacion')
	tipoF = (
        ("COBERTERA", 'Abonado cobertera'),
		("FONDO", 'Abonado de fondo'),
		("ENMIENDAS", 'Enmiendas'),
    )
	tipo_fert = models.CharField(max_length=100,
                                   choices=tipoF,
                                   default="COBERTERA")
	modo_aplicacion = models.CharField(max_length=200,blank=True)
	superficie_aplicada = models.DecimalField(max_digits=5, decimal_places=2,blank=True)
	n_orden_aplicacion = models.CharField(max_length=200,blank=True)
	producto_comercial = models.CharField(max_length=200,blank=True)
	composicion = models.CharField(max_length=200,blank=True)
	riqueza_n = models.IntegerField()
	riqueza_p = models.IntegerField()
	riqueza_k = models.IntegerField()
	riqueza_Ca = models.IntegerField(blank=True)
	riqueza_Mg = models.IntegerField(blank=True)
	riqueza_S = models.IntegerField(blank=True)
	riqueza_otros = models.IntegerField(blank=True)
	dosis = models.DecimalField(max_digits=10, decimal_places=2)
	unidad_dosis = models.CharField(max_length=200)
	nitrogeno = models.DecimalField(max_digits=5, decimal_places=2)
	fosforo = models.DecimalField(max_digits=5, decimal_places=2)
	potasio = models.DecimalField(max_digits=5, decimal_places=2)
	empresa_distribuidora = models.CharField(max_length=200,blank=True)
	justificacion = models.CharField(max_length=200,blank=True)
	densidad = models.DecimalField(max_digits=10, decimal_places=2)
	abono_aplicado = models.DecimalField(max_digits=10, decimal_places=2)
	
class op_riego(models.Model):
	idOperacion = models.ForeignKey(Operacion,related_name='riego')
	sisR = (
        ("GOTEROS", 'Localizado: Goteros'),
		("ASPERSION", 'Aspersión'),
    )
	sistema_riego = models.CharField(max_length=100,
                                   choices=sisR,
                                   default="GOTEROS")
	procedencia_agua = models.CharField(max_length=200,blank=True)
	calidad_agua = models.CharField(max_length=200,blank=True)
	cantidad_agua = models.DecimalField(max_digits=10, decimal_places=2)
	uf_nitro = models.CharField(max_length=200,blank=True)
	justificacion_riego = models.CharField(max_length=200,blank=True)
	clave = models.CharField(max_length=200,blank=True)
	
class op_recoleccion(models.Model):
	idOperacion = models.ForeignKey(Operacion,related_name='recoleccion')
	reco = (
        ("MANUAL", 'Manual'),
		("MECANIZADO", 'Mecanizado'),
    )
	id_lote = models.CharField(max_length=200)
	metodo_recol = models.CharField(max_length=100,
                                   choices=reco,
                                   default="MANUAL")
	superficie_recogida = models.DecimalField(max_digits=10, decimal_places=2)
	total_recogido = models.DecimalField(max_digits=10, decimal_places=2,blank = True)
	rendimiento = models.DecimalField(max_digits=10, decimal_places=2,blank = True)
	destrio = models.DecimalField(max_digits=5, decimal_places=2,blank = True)
	id_lote_destino = models.CharField(max_length=200,blank = True)
	tratamiento_cosecha = models.CharField(max_length=200,blank = True)
	receptor_produccion = models.CharField(max_length=200,blank = True)
	n_albaran = models.CharField(max_length=200,blank = True)
	precio_agricultor = models.DecimalField(max_digits=10, decimal_places=2,blank = True)

class Aplicacion(models.Model):

	fecha_Aplicacion = models.DateField()
	numero_orden_tratamiento = models.CharField(max_length=200)
	fecha_Orden_tratamiento = models.DateField()
	gasto_caldo = models.DecimalField(max_digits=11, decimal_places=2)
								   
	superficie_tratada = models.DecimalField(max_digits=5, decimal_places=2)
	porcentaje = models.IntegerField()
	distribucion_ap = models.CharField(max_length=200)

	condiciones_aplicacion = models.CharField(max_length=200)#Preguntar si selector
	presion_tratamiento = models.DecimalField(max_digits=11, decimal_places=2)
	velocidad_tratamiento = models.DecimalField(max_digits=11, decimal_places=2)
	tecnico = models.ForeignKey(Tecnico,related_name='TecnicoAplicacion')
	horas = models.DecimalField(max_digits=5, decimal_places=2)
	
	aplicador = models.ForeignKey(Aplicador)
	idUHC = models.ForeignKey(UHC, related_name ='aplicaciones')
	maquinaria = models.ForeignKey(Maquinaria)

	
	hora_aplicacion = models.TimeField()
	observaciones = models.TextField()
	

class Producto_aplicado(models.Model):
	nombre = models.CharField(max_length=200)
	dosis = models.DecimalField(max_digits=11, decimal_places=2)
	materia_activa = models.CharField(max_length=200)
	riqueza = models.IntegerField()
	objeto = models.CharField(max_length=200)
	justific = models.CharField(max_length=200)
	casa_comercial = models.CharField(max_length=200,blank=True)
	n_registro = models.CharField(max_length=10)
	empresa_distribuidora = models.CharField(max_length=200,blank=True)
	observaciones = models.TextField(blank=True)
	aplicacion = models.ForeignKey(Aplicacion, related_name ='productos')
	

	
class Parcela(models.Model):
	SR = (
        ("SECANO", 'Secano'),
		("REGADIO", 'Regadio'),
    )
	nombre = models.CharField(max_length=200)
	provincia = models.ForeignKey(Provincia)
	municipio = models.ForeignKey(Municipio)
	poligono = models.CharField(max_length=3)
	parcela = models.CharField(max_length=5)
	recinto = models.CharField(max_length=5)
	superficie_hectareas = models.DecimalField(max_digits=11, decimal_places=6)
	sr = models.CharField(max_length=10,
                                   choices=SR,
                                   default="SECANO")
	descripcion = models.TextField()
	idExplotacion = models.ForeignKey(Explotacion,related_name = 'parcelasExplotacion')
	idcultivo = models.ForeignKey(Cultivo,related_name = 'parcelasCultivo')


	
class Parcelauhc(models.Model):

	idUHC = models.ForeignKey(UHC, related_name ='parcelasUHC')
	idParcela = models.ForeignKey(Parcela,related_name = 'parcelasuhcParcela')
	idExplotacion = models.ForeignKey(Explotacion,related_name = 'parcelauhcExplotacion')

	
# Create your models here.
