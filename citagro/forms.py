from django import forms
from models import Tecnico, Administrador,Explotacion,UsuarioExplotacion,Provincia,Municipio,Maquinaria,DatosClimaticos
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import re
from django.db.models import Count
from django.forms.widgets import TextInput
from django.db.models.fields import PositiveIntegerField
from django.utils import six
#from djangular.forms import NgModelFormMixin, NgModelForm

class UploadForm(forms.Form):
	docfile = forms.FileField(
        label='Selecciona un archivo'
    )

 
def validoDNI(dni):
		tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
		dig_ext = "XYZ"
		reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
		numeros = "1234567890"
		dni = dni.upper()
		if len(dni) == 9:
			dig_control = dni[8]
			dni = dni[:8]
			if dni[0] in dig_ext:
				dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
			return len(dni) == len([n for n in dni if n in numeros]) \
				and tabla[int(dni)%23] == dig_control
		return False
		
def validarCIF(valor):
    """
    Nos indica si un CIF es valido.
    El valor debe estar normalizado
    @note:
      - ante cualquier problema se valida como False
    """
    bRet = False
    CLAVES_CIF='PQS' + 'ABEH' + 'CDFGJRUVNW'
    CONTROL_CIF_LETRA = 'KPQS'
    CONTROL_CIF_NUMERO = 'ABEH'

    EQUIVALENCIAS_CIF = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G',
8:'H', 9:'I', 10:'J', 0:'J'}

    if len(valor) == 9:
        v0 = valor[0]
        if v0 in CLAVES_CIF:
            try:
                sumPar = 0
                sumImpar = 0
                for i in xrange(1,8):
                    if i % 2:
                        v = int(valor[i]) * 2
                        if v > 9: v = 1 + (v - 10)
                        sumImpar += v
                    else:
                        v = int(valor[i])
                        sumPar += v
                suma = sumPar + sumImpar
                e = suma % 10
                d = 10 - e
                letraCif = EQUIVALENCIAS_CIF[d]
                if valor[0] in CONTROL_CIF_LETRA:
                    if valor[-1] == letraCif: bRet = True
                elif valor[0] in CONTROL_CIF_NUMERO:
                    if d == 10: d = 0
                    if valor[-1] == str(d): bRet = True
                else:
                    if d == 10: d = 0
                    if valor[-1] == str(d) or valor[-1] == letraCif: bRet = True
            except:
                pass

    return bRet
	
class PositiveIntWidget(TextInput):
    input_type = 'number'
    def __init__(self, *args, **kwargs):
        if not 'attrs' in kwargs:
            kwargs['attrs'] = dict(min=0)
        else:
            kwargs['attrs'].setdefault('min', 0)
        super(PositiveIntWidget, self).__init__(*args, **kwargs)
		


'''class FormularioTecnico(NgModelFormMixin, NgModelForm):

    
	
    def __init__(self, *args, **kwargs):
        
        self.provincia = kwargs.pop('provincia',None)
        super(FormularioTecnico, self).__init__(*args, **kwargs)
        
        if self.provincia != None:
            municipios = Municipio.objects.filter(idProvincia = self.provincia.id)
        else:
            municipios = Municipio.objects.all()
       
        self.fields['Municipio'].queryset = municipios
	
	
    class Meta:
        model = Tecnico
        fields = ('Nombre', 'Apellido1', 'Apellido2','NIF','Domicilio','Provincia','Municipio','CP','email','Telefono1','Telefono2','Fax','ropo')
        labels = {'ropo': _('Num. reg en el ROPO')}
		
		
    def clean_CP(self):
        data = self.cleaned_data['CP']
        if (len(data) > 0 and len(data) < 5) or (not data.isdigit()):
		    raise forms.ValidationError("El codigo postal que has escrito no es valido")
        return data
		
    def clean_Nombre(self):
        data = self.cleaned_data['Nombre']
        if data.isdigit() or len(data) < 3:
		    raise forms.ValidationError("El nombre que has escrito no es valido")
        return data	

    def clean_Apellido1(self):
        data = self.cleaned_data['Apellido1']
        if data.isdigit() or len(data) < 3:
		    raise forms.ValidationError("El apellido que has escrito no es valido")
        return data	
		
    def clean_Apellido2(self):
        data = self.cleaned_data['Apellido2']
        if data.isdigit() or len(data) < 3:
		    raise forms.ValidationError("El apellido que has escrito no es valido")
        return data
		
		
    def clean_NIF(self):
        data = self.cleaned_data['NIF']
        dni = Tecnico.objects.filter(NIF=data)
        if len(dni) > 0:
            raise forms.ValidationError("Ya existe un usuario tecnico con ese NIF")
        else:
            if not validoDNI(data):
                raise forms.ValidationError("El dni que has escrito es invalido")
        return data
		
    def clean_ropo(self):
        data = self.cleaned_data['ropo']
		
        if len(data) > 1:
			primer_caracter = int(data[0])
			segundo_caracter = int(data[1])
			ultimo_caracter = data[len(data)-1]
			penultimo_caracter = data[len(data)-2]
			num = data[:-2]
			
			if (not num.isdigit()) or (ultimo_caracter.isdigit()) or (penultimo_caracter.isdigit()) or (len(data) != 12) or (primer_caracter != 0) or (segundo_caracter != 1):
				raise forms.ValidationError("El numero de registro en ROPO que has escrito es invalido")
				
        return data
		
    def clean_Telefono1(self):
        data = self.cleaned_data['Telefono1']
        exp = '^[679][0-9]+'
        if not re.match(exp,data):
            raise forms.ValidationError("El telefono no es valido")
        return data
		
    def clean_Telefono2(self):
        data = self.cleaned_data['Telefono2']
        if len(data) > 0:
            exp = '^[679][0-9]+'
            if not re.match(exp,data):
                raise forms.ValidationError("El telefono no es valido")
        return data
		
    def clean_Fax(self):
        data = self.cleaned_data['Fax']
        if len(data) > 0:
            exp = '^[679][0-9]+'
            if not re.match(exp,data):
                raise forms.ValidationError("El numero de FAX no es valido")
        return data
	'''	
class FormularioAdministrador(forms.ModelForm):
    
	
    def __init__(self, *args, **kwargs):
        
        self.provincia = kwargs.pop('provincia',None)
        super(FormularioAdministrador, self).__init__(*args, **kwargs)
        
        if self.provincia != None:
            municipios = Municipio.objects.filter(idProvincia = self.provincia.id)
        else:
            municipios = Municipio.objects.all()
       
        self.fields['Municipio'].queryset = municipios
       
        

    class Meta:
        model = Administrador
        fields = ('Nombre', 'Apellido1', 'Apellido2','NIF','Domicilio','Provincia','Municipio','CP','email','Telefono1','Telefono2','Fax','ropo')
        labels = {'ropo': _('Num. reg en el ROPO')}
		
    
		
    def clean_CP(self):
        data = self.cleaned_data['CP']
        if (len(data) > 0 and len(data) < 5) or (not data.isdigit()):
		    raise forms.ValidationError("El codigo postal que has escrito no es valido")
        return data
		
    def clean_Nombre(self):
        data = self.cleaned_data['Nombre']
        if data.isdigit() or len(data) < 3:
		    raise forms.ValidationError("El nombre que has escrito no es valido")
        return data	

    def clean_Apellido1(self):
        data = self.cleaned_data['Apellido1']
        if data.isdigit() or len(data) < 3:
		    raise forms.ValidationError("El apellido que has escrito no es valido")
        return data	
		
    def clean_Apellido2(self):
        data = self.cleaned_data['Apellido2']
        if data.isdigit() or len(data) < 3:
		    raise forms.ValidationError("El apellido que has escrito no es valido")
        return data
		
	
   
    
		
    def clean_NIF(self):
        data = self.cleaned_data['NIF']
        dni = Administrador.objects.filter(NIF=data)
        if len(dni) > 0:
            raise forms.ValidationError("Ya existe un usuario administrador con ese NIF")
        else:
            if not validoDNI(data):
                raise forms.ValidationError("El dni que has escrito es invalido")
        return data
		
    def clean_ropo(self):
        data = self.cleaned_data['ropo']
		
        if len(data) > 1:
			primer_caracter = int(data[0])
			segundo_caracter = int(data[1])
			ultimo_caracter = data[len(data)-1]
			penultimo_caracter = data[len(data)-2]
			num = data[:-2]
			
			if (not num.isdigit()) or (ultimo_caracter.isdigit()) or (penultimo_caracter.isdigit()) or (len(data) != 12) or (primer_caracter != 0) or (segundo_caracter != 1):
				raise forms.ValidationError("El numero de registro en ROPO que has escrito es invalido")
				
        return data
		
    def clean_Telefono1(self):
        data = self.cleaned_data['Telefono1']
        exp = '^[679][0-9]+'
        if not re.match(exp,data):
            raise forms.ValidationError("El telefono no es valido")
        return data
		
    def clean_Telefono2(self):
        data = self.cleaned_data['Telefono2']
        if len(data) > 0:
            exp = '^[679][0-9]+'
            if not re.match(exp,data):
                raise forms.ValidationError("El telefono no es valido")
        return data
		
    def clean_Fax(self):
        data = self.cleaned_data['Fax']
        if len(data) > 0:
            exp = '^[679][0-9]+'
            if not re.match(exp,data):
                raise forms.ValidationError("El numero de FAX no es valido")
        return data
		
class FormularioExplotacion(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        
        self.provincia = kwargs.pop('provincia',None)
        super(FormularioExplotacion, self).__init__(*args, **kwargs)
        
        if self.provincia != None:
            municipios = Municipio.objects.filter(idProvincia = self.provincia.id)
        else:
            municipios = Municipio.objects.all()
       
        self.fields['Localidad'].queryset = municipios
	
    class Meta:
        model = Explotacion
        fields = ('Razon_Social', 'cif_nif', 'Domicilio','Provincia','Localidad','CP')
        labels = {'cif_nif': _('CIF/NIF')}
		
		
    def clean_CP(self):
        data = self.cleaned_data['CP']
        if (len(data) > 0 and len(data) < 5) or (not data.isdigit()):
		    raise forms.ValidationError("El codigo postal que has escrito no es valido")
        return data
	
		
    def clean_cif_nif(self):
        data = self.cleaned_data['cif_nif']
        nif = Explotacion.objects.filter(cif_nif=data)
        ultimo_caracter = data[len(data)-1]
        primer_caracter = data[0]
		
        if ultimo_caracter.isdigit() and (not primer_caracter.isdigit()):
            if len(nif) > 0:
                raise forms.ValidationError("Ya existe una explotacion con ese CIF")
            else:
                if not validarCIF(data):
                    raise forms.ValidationError("El nif que has escrito es invalido")
        elif (not ultimo_caracter.isdigit()) and primer_caracter.isdigit():
            if len(nif) > 0:
                raise forms.ValidationError("Ya existe una explotacion con ese DNI")
            else:
                if not validoDNI(data):
                    raise forms.ValidationError("El dni que has escrito es invalido")
        else:
            raise forms.ValidationError("nif/cif incorrecto")
		
        return data
	
	

class AsignaUsuarioFormulario(forms.ModelForm):
    
    class Meta:
        model = UsuarioExplotacion
        fields=['idUsuario']

		
    def __init__(self, *args, **kwargs):
        
        self.id = kwargs.pop('id',None)
        self.user_id =kwargs.pop('user_id',None)
        super(AsignaUsuarioFormulario, self).__init__(*args, **kwargs)
        tecnicos = Tecnico.objects.filter(idAdmin = self.user_id)
        usuariosExplotaciones = UsuarioExplotacion.objects.filter(idExplotacion = self.id)
        lista_id = []
        for usuarioExplotacion in usuariosExplotaciones:
            lista_id = lista_id + [usuarioExplotacion.idUsuario.id]
       
        self.fields['idUsuario'].queryset = Tecnico.objects.filter(idAdmin = self.user_id).exclude(id__in = lista_id)
		
class FormularioMaquina(forms.ModelForm):
    
    class Meta:
        model = Maquinaria
        exclude=['idExplotacion']
		
class FormularioClima(forms.ModelForm):
    
    class Meta:
        model = DatosClimaticos
        exclude=['idExplotacion']
	
		
		
		
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }
		

		

		

		
	
	
