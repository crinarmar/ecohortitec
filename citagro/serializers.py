from rest_framework import serializers
from citagro.models import Administrador,Inputoperacion,Cultivoexplotacion,RepositorioImagenes,Tiposoperacion,Cultivo,Tecnico,Perfil,Explotacion,UsuarioExplotacion,MaquinaExplotacion,DatosClimaticos,Provincia,Municipio,Maquinaria,User,Aplicador,UHC,Parcela,Parcelauhc,Analisis,Aplicacion,Producto_aplicado,Operacion,op_poda,op_labores,op_fertilizacion,op_riego,op_recoleccion
from citagro.models import Muestreo,muestra_fenologia,muestra_insetos,muestra_trampas,muestra_brotes,muestra_zeuzera,muestra_enfermedades

class PerfilSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Perfil
		fields = ('id','user','TipoUsuario')

class UsuariosSerializer(serializers.ModelSerializer):
    
    perfil = PerfilSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','is_staff','is_active','perfil')
		
class DatosClimaticosSerializer(serializers.ModelSerializer):

    class Meta:
        model = DatosClimaticos
        fields = ('id', 'EstacionClimatica', 'fecha','Temperatura', 'TempMax','TempMin', 'TempMed','Humedad','HumMax','HumMin','HumMed','Precipitacion','idExplotacion',)
		
class TiposoperacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tiposoperacion
        fields = ('id', 'nombre','orden')
		
class InputoperacionSerializer(serializers.ModelSerializer):

	
    idTipoOperacion = serializers.ReadOnlyField(source = 'idTipoOp.id')
    tipoOperacion = serializers.ReadOnlyField(source = 'idTipoOp.nombre')
    orden = serializers.ReadOnlyField(source = 'idTipoOp.orden')
    class Meta:
        model = Inputoperacion
        fields = ('id','input','idTipoOp','coefEmision','cantidad','coefAsignacion','costeUnitario','unidad','unidadCoef','tipoOperacion','orden','idTipoOperacion','nombreTipo')
		
		
class CultivoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cultivo
        fields = ('id', 'nombre', 'fecha_inicio','fecha_fin', 'descripcion','localizacion')
		
class CultivoexplotacionSerializer(serializers.ModelSerializer):

    nombre = serializers.ReadOnlyField(source = 'idCultivo.nombre')
    class Meta:
        model = Cultivoexplotacion
        fields = ('id', 'idCultivo', 'superficieCultivo','idExplotacion','idUHC','nombre')
		
	
class MunicipioSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Municipio
		fields = ('id','CodMunicipio','Municipio','idProvincia')
		
class ProvinciaSerializer(serializers.ModelSerializer):
	
	municipios = MunicipioSerializer(many=True, read_only=True)
	
	class Meta:
		model = Provincia
		fields = ('id','CodProvincia','Provincia','municipios')
		
		
class AplicadorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Aplicador
		fields = ('id','activo','Aplicador','Telefono','Fax','email','idExplotacion','nombre','apellido1','apellido2','dni','fecha_validez','fecha_expedicion','razon_social')
		
class UsuarioExplotacionSerializer(serializers.ModelSerializer):
	
    usNombre = serializers.ReadOnlyField(source='idUsuario.Nombre')
    usApellido1 = serializers.ReadOnlyField(source='idUsuario.Apellido1')
    usApellido2 = serializers.ReadOnlyField(source='idUsuario.Apellido2')
    usNif = serializers.ReadOnlyField(source='idUsuario.NIF')
    usMunicipio = serializers.ReadOnlyField(source='idUsuario.Municipio.Municipio')
    usProvincia = serializers.ReadOnlyField(source='idUsuario.Provincia.Provincia')
    usTel1 = serializers.ReadOnlyField(source='idUsuario.Telefono1')
    usF_ing = serializers.ReadOnlyField(source='idUsuario.fecha_ingreso')
    activo = serializers.ReadOnlyField(source='idUsuario.activo')
	
    class Meta:
		model = UsuarioExplotacion
		fields = ('id','idUsuario','activo','idExplotacion','usNombre','usApellido1','usApellido2','usNif','usMunicipio','usProvincia','usTel1','usF_ing')
		
class MaquinaExplotacionSerializer(serializers.ModelSerializer):
	
    maq_Tipo = serializers.ReadOnlyField(source='idMaquina.TipoMaquina')
    maq_marca = serializers.ReadOnlyField(source='idMaquina.MarcaModelo')
    maq_roma = serializers.ReadOnlyField(source='idMaquina.numero_roma')
    maq_f_ad = serializers.ReadOnlyField(source='idMaquina.fecha_adquisicion')
    maq_f_rev = serializers.ReadOnlyField(source='idMaquina.fecha_revision')
	
    class Meta:
		model = MaquinaExplotacion
		fields = ('id','idMaquina','idExplotacion','maq_Tipo','maq_marca','maq_roma','maq_f_ad','maq_f_rev')
		
class MaquinariaSerializer(serializers.ModelSerializer):

    explotaciones = MaquinaExplotacionSerializer(many=True, read_only=True)
    class Meta:
        model = Maquinaria
        fields = ('id','activo', 'numero_roma', 'fecha_adquisicion','fecha_revision', 'TipoMaquina','MarcaModelo','idAdmin','explotaciones')
		
class TecnicoSerializer(serializers.ModelSerializer):
    usuariosExplotaciones = UsuarioExplotacionSerializer(many=True, read_only=True)
    class Meta:
        model = Tecnico
        fields = ('id','activo', 'Nombre', 'Apellido1', 'Apellido2','NIF', 'Domicilio','Municipio','Provincia','CP','email','Telefono1','Telefono2','Fax','fecha_ingreso','ropo','idAdmin','usuariosExplotaciones', )
		

class AnalisisSerializer(serializers.ModelSerializer):
    uhc_nombre = serializers.ReadOnlyField(source='idUHC.nombre')
    TecnicoNombre = serializers.ReadOnlyField(source='tecnico.Nombre')
    TecnicoApellido1 = serializers.ReadOnlyField(source='tecnico.Apellido1')
    TecnicoApellido2 = serializers.ReadOnlyField(source='tecnico.Apellido2')
    class Meta:
        model = Analisis
        fields = ('id', 'fecha_muestra', 'idUHC','uhc_nombre', 'tipo','tecnico','TecnicoNombre','TecnicoApellido1','TecnicoApellido2', 'descripcion','laboratorio','numero_informe','fecha_emision','observaciones','acciones','idExplotacion','tecnico','horas')
		
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto_aplicado
        fields = ('id','nombre','dosis','materia_activa','riqueza','objeto','justific','casa_comercial','n_registro','empresa_distribuidora','observaciones','aplicacion')
			
		
class AplicacionSerializer(serializers.ModelSerializer):
    uhc_nombre = serializers.ReadOnlyField(source='idUHC.nombre')
    productos = ProductoSerializer(many=True, read_only=True)
    aplicador_nombre = serializers.ReadOnlyField(source='aplicador.nombre')
    aplicador_ap1 = serializers.ReadOnlyField(source='aplicador.apellido1')
    aplicador_ap2 = serializers.ReadOnlyField(source='aplicador.apellido2')
    maquina_tipo = serializers.ReadOnlyField(source='maquinaria.TipoMaquina')
    maquina_modelo = serializers.ReadOnlyField(source='maquinaria.MarcaModelo')
    maquina_roma = serializers.ReadOnlyField(source='maquinaria.numero_roma')
    TecnicoNombre = serializers.ReadOnlyField(source='tecnico.Nombre')
    TecnicoApellido1 = serializers.ReadOnlyField(source='tecnico.Apellido1')
    TecnicoApellido2 = serializers.ReadOnlyField(source='tecnico.Apellido2')
    class Meta:
        model = Aplicacion
        fields = ('id', 'fecha_Aplicacion','numero_orden_tratamiento','fecha_Orden_tratamiento','gasto_caldo','superficie_tratada','porcentaje','distribucion_ap','condiciones_aplicacion','presion_tratamiento','velocidad_tratamiento','aplicador','aplicador_nombre','aplicador_ap1','aplicador_ap2', 'idUHC','uhc_nombre', 'maquinaria','maquina_tipo','maquina_modelo','maquina_roma','hora_aplicacion','observaciones','productos','tecnico','TecnicoNombre','TecnicoApellido1','TecnicoApellido2','horas')
			
		
class ParcelaSerializer(serializers.ModelSerializer):		
    parcela_codProv = serializers.ReadOnlyField(source='provincia.CodProvincia')
    parcela_codMun = serializers.ReadOnlyField(source='municipio.CodMunicipio')
    parcela_Prov = serializers.ReadOnlyField(source='provincia.Provincia')
    parcela_Mun = serializers.ReadOnlyField(source='municipio.Municipio')
    nombreCultivo = serializers.ReadOnlyField(source='idcultivo.nombre')

    class Meta:
        model = Parcela
        fields = ('id','nombre','provincia','parcela_codProv','parcela_Prov','municipio','parcela_codMun','parcela_Mun','poligono','parcela','recinto','superficie_hectareas','sr','descripcion','idExplotacion','idcultivo','nombreCultivo')
		
class ParcelauhcSerializer(serializers.ModelSerializer):		

	
    nombre = serializers.ReadOnlyField(source='idParcela.nombre')
    uhc_nombre = serializers.ReadOnlyField(source='idUHC.nombre')
    parcela_codProv = serializers.ReadOnlyField(source='idParcela.provincia.CodProvincia')
    parcela_codMun = serializers.ReadOnlyField(source='idParcela.municipio.CodMunicipio')
    poligono = serializers.ReadOnlyField(source='idParcela.poligono')
    parcela = serializers.ReadOnlyField(source='idParcela.parcela')
    recinto = serializers.ReadOnlyField(source='idParcela.recinto')
    superficie_hectareas = serializers.ReadOnlyField(source='idParcela.superficie_hectareas')
    descripcion = serializers.ReadOnlyField(source='idParcela.descripcion')
    nombreCultivo = serializers.ReadOnlyField(source='idParcela.idcultivo.nombre')

	
    class Meta:
        model = Parcelauhc
        fields = ('id','idUHC','idParcela','nombre','uhc_nombre','parcela_codProv','parcela_codMun','poligono','parcela','recinto','superficie_hectareas','descripcion','nombreCultivo','idExplotacion')
		
class RepositorioImagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model= RepositorioImagenes
        fields=('id','imagen')
		

class op_podaSerializer(serializers.ModelSerializer):
    class Meta:
        model = op_poda
        fields = ('id', 'idOperacion', 'TipoPoda','Duracion','Herramienta','Producto','Fecha_eliminacion','Modo_eliminacion')	
		
class op_laboresSerializer(serializers.ModelSerializer):
    class Meta:
        model = op_labores
        fields = ('id', 'idOperacion', 'apero','distribucion','superficie_labrada','profundidad_labor','justificacion','empresa')
		
class op_fertilizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = op_fertilizacion
        fields = ('id', 'idOperacion','tipo_fert','modo_aplicacion','superficie_aplicada','n_orden_aplicacion','producto_comercial','composicion','riqueza_n','riqueza_p','riqueza_k','riqueza_Ca','riqueza_Mg','riqueza_S','riqueza_otros','dosis','unidad_dosis','nitrogeno','fosforo','potasio','empresa_distribuidora','justificacion','densidad','abono_aplicado')			

class op_riegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = op_riego
        fields = ('id', 'idOperacion','sistema_riego','procedencia_agua','calidad_agua','cantidad_agua','uf_nitro','justificacion_riego','clave')
		
class op_recoleccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = op_recoleccion
        fields = ('id', 'idOperacion','id_lote','metodo_recol','superficie_recogida','total_recogido','rendimiento','destrio','id_lote_destino','tratamiento_cosecha','receptor_produccion','n_albaran','precio_agricultor')
	
class OperacionSerializer(serializers.ModelSerializer):
    uhc_nombre = serializers.ReadOnlyField(source='idUHC.nombre')
    TecnicoNombre = serializers.ReadOnlyField(source='tecnico.Nombre')
    TecnicoApellido1 = serializers.ReadOnlyField(source='tecnico.Apellido1')
    TecnicoApellido2 = serializers.ReadOnlyField(source='tecnico.Apellido2')
    tipoOperacion = serializers.ReadOnlyField(source='idTipoOperacion.nombre')
    inputOperacion = serializers.ReadOnlyField(source='idInputOperacion.input')
    class Meta:
        model = Operacion
        fields = ('id', 'fecha_operacion', 'idUHC','uhc_nombre','observaciones','idExplotacion','tecnico','horas','TecnicoNombre','TecnicoApellido1','TecnicoApellido2','idInputOperacion','idTipoOperacion','tipoOperacion','inputOperacion','cantidad','unidad','coefEmision','coefAsignacion','costeUnitario','unidadCoef','emisionesTotal','costeTotal')

class muestra_fenologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = muestra_fenologia
        fields = ('id', 'idMuestra','muestra_a','muestra_b','muestra_c','muestra_d','muestra_e','muestra_f','muestra_g','muestra_h','muestra_i')

	
class muestra_insetosSerializer(serializers.ModelSerializer):
    class Meta:
        model = muestra_insetos
        fields = ('id', 'idMuestra','coccinelidos','neuropteros')
		
class muestra_trampasSerializer(serializers.ModelSerializer):
    class Meta:
        model = muestra_trampas
        fields = ('id', 'idMuestra','carpocapsa_p1','carpocapsa_p2','carpocapsa_p3','carpocapsa_p4','carpocapsa_p5','carpocapsa_p6')
		
class muestra_brotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = muestra_brotes
        fields = ('id', 'idMuestra','carpocapsa','acaros','pulgones')
		
class muestra_zeuzeraSerializer(serializers.ModelSerializer):
    class Meta:
        model = muestra_zeuzera
        fields = ('id', 'idMuestra','zeuzera')
		
class muestra_enfermedadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = muestra_enfermedades
        fields = ('id', 'idMuestra','bacteriosis','antracnosis','antracnosis_2')
			
class MuestreoSerializer(serializers.ModelSerializer):
    uhc_nombre = serializers.ReadOnlyField(source='idUHC.nombre')
    fenologia = muestra_fenologiaSerializer(many=True, read_only=True)
    insectos = muestra_insetosSerializer(many=True, read_only=True)
    trampas = muestra_trampasSerializer(many=True, read_only=True)
    brotes = muestra_brotesSerializer(many=True, read_only=True)
    zeuzera = muestra_zeuzeraSerializer(many=True, read_only=True)
    enfermedades = muestra_enfermedadesSerializer(many=True, read_only=True)
    TecnicoNombre = serializers.ReadOnlyField(source='tecnico.Nombre')
    TecnicoApellido1 = serializers.ReadOnlyField(source='tecnico.Apellido1')
    TecnicoApellido2 = serializers.ReadOnlyField(source='tecnico.Apellido2')
    class Meta:
        model = Muestreo
        fields = ('id', 'fecha_muestreo', 'idUHC','uhc_nombre','observaciones','horas','idExplotacion','tecnico','TecnicoNombre','TecnicoApellido1','TecnicoApellido2','fenologia','insectos','trampas','brotes','zeuzera','enfermedades')
	
class UHCSerializer(serializers.ModelSerializer):		
    analisis = AnalisisSerializer(many=True, read_only=True)
    parcelas = ParcelauhcSerializer(many=True, read_only=True)
    aplicaciones = AplicacionSerializer(many=True, read_only=True)
    operaciones = OperacionSerializer(many=True, read_only=True)
    muestreo = MuestreoSerializer(many=True, read_only=True)
    Razon_Social = serializers.ReadOnlyField(source='idExplotacion.Razon_Social')
    class Meta:
        model = UHC
        fields = ('id','nombre','idExplotacion','parcelas','analisis','aplicaciones','operaciones','muestreo','costeAsociado','indicadorEvAmbiental','superficie_hectareas','Razon_Social')

		
class ExplotacionSerializer(serializers.ModelSerializer):
    datosClimaticos = DatosClimaticosSerializer(many=True, read_only=True)
    maquinarias= MaquinaExplotacionSerializer(many=True, read_only=True)
    usuarios= UsuarioExplotacionSerializer(many=True, read_only=True)
    aplicadores = AplicadorSerializer(many=True, read_only=True)
    uhcs = UHCSerializer(many=True, read_only=True)
    parcelasExplotacion = ParcelauhcSerializer(many=True,read_only=True)
    analisisExplotacion = AnalisisSerializer(many=True,read_only=True)
    operacionesExplotacion = OperacionSerializer(many=True, read_only=True)
    muestrasExplotacion = MuestreoSerializer(many=True, read_only=True)
	
    class Meta:
        model = Explotacion
        fields = ('id', 'Razon_Social', 'cif_nif', 'Domicilio','Localidad', 'Provincia','CP','idAdmin','datosClimaticos','maquinarias','usuarios','aplicadores','uhcs','parcelasExplotacion','analisisExplotacion','operacionesExplotacion','muestrasExplotacion')

class AdministradorSerializer(serializers.ModelSerializer):
    
    tecnicos = TecnicoSerializer(many=True, read_only=True)
    explotaciones = ExplotacionSerializer(many=True, read_only=True)
    maquinaria = MaquinariaSerializer(many=True,read_only=True)
    class Meta:
        model = Administrador
        fields = ('id', 'Nombre', 'Apellido1', 'Apellido2','NIF', 'Domicilio','Municipio','Provincia','CP','email','Telefono1','Telefono2','Fax','fecha_ingreso','ropo', 'tecnicos','explotaciones','maquinaria')



