(function(){

	var administrador = angular.module('administrador',["ui.bootstrap", "ngCookies"]);
	
	administrador.config(function ($interpolateProvider) {
			$interpolateProvider.startSymbol("[[");
			$interpolateProvider.endSymbol("]]");
		}
	);
	

	
	function validateCIF(cif)
	{
			//Quitamos el primer caracter y el ultimo digito
			var valueCif=cif.substr(1,cif.length-2);

			var suma=0;

			//Sumamos las cifras pares de la cadena
			for(i=1;i<valueCif.length;i=i+2)
			{
				suma=suma+parseInt(valueCif.substr(i,1));
			}

			var suma2=0;

			//Sumamos las cifras impares de la cadena
			for(i=0;i<valueCif.length;i=i+2)
			{
				result=parseInt(valueCif.substr(i,1))*2;
				if(String(result).length==1)
				{
					// Un solo caracter
					suma2=suma2+parseInt(result);
				}else{
					// Dos caracteres. Los sumamos...
					suma2=suma2+parseInt(String(result).substr(0,1))+parseInt(String(result).substr(1,1));
				}
			}

			// Sumamos las dos sumas que hemos realizado
			suma=suma+suma2;

			var unidad=String(suma).substr(1,1)
			unidad=10-parseInt(unidad);

			var primerCaracter=cif.substr(0,1).toUpperCase();

			if(primerCaracter.match(/^[FJKNPQRSUVW]$/))
			{
				//Empieza por .... Comparamos la ultima letra
				if(String.fromCharCode(64+unidad).toUpperCase()==cif.substr(cif.length-1,1).toUpperCase())
					return true;
			}else if(primerCaracter.match(/^[XYZ]$/)){
				//Se valida como un dni
				var newcif;
				if(primerCaracter=="X")
					newcif=cif.substr(1);
				else if(primerCaracter=="Y")
					newcif="1"+cif.substr(1);
				else if(primerCaracter=="Z")
					newcif="2"+cif.substr(1);
				return validateDNI(newcif);
			}else if(primerCaracter.match(/^[ABCDEFGHLM]$/)){
				//Se revisa que el ultimo valor coincida con el calculo
				if(unidad==10)
					unidad=0;
				if(cif.substr(cif.length-1,1)==String(unidad))
					return true;
			}else{
				//Se valida como un dni
				return validateDNI(cif);
			}
			return false;
	};
	
	function validateDNI(dni)
	{
		var lockup = 'TRWAGMYFPDXBNJZSQVHLCKE';
		var valueDni=dni.substr(0,dni.length-1);
		var letra=dni.substr(dni.length-1,1).toUpperCase();

		if(lockup.charAt(valueDni % 23)==letra)
			return true;
		return false;
	};

	var expresion_regular_dni = /^[XYZ]?\d{5,8}[A-Z]$/;
	var expresion_regular_cif = /^[ABCDEFGHJNPQRSUVW]{1}/;
	administrador.directive('nifcif', function() {
	return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$validators.nifcif = function(modelValue, viewValue) {
        if (ctrl.$isEmpty(modelValue)) {
          // consider empty models to be valid
          return true;
        }
		
		if(expresion_regular_cif.test(viewValue)){
			return validateCIF(viewValue);
		}else if(expresion_regular_dni.test(viewValue)){
			return validateDNI(viewValue);
		}else{
			return false;
		}
      };
    }
  };
});
	
	administrador.controller('MunicipiosController',['$http','$log','$scope',function($http,$log,$scope){
		
		$scope.iniciaMunicipios= function(){

			$http.get('/api/municipios').success(function(dato){	
				$scope.municipios = dato;
			});
		};
		$scope.guardaExplotacion = function(){

			explotacion = {
			Razon_Social : $scope.Razon_Social,
			cif_nif : $scope.cif_nif,
			Domicilio : $scope.Domicilio,
			Localidad : $scope.municipioSeleccionado,
			Provincia :$scope.provinciaSeleccionada,
			CP : $scope.CP,
			idAdmin : 1};


			
			$http.post('/api/explotaciones/',explotacion).
			success(function(data,status,headers,config){
				location.replace('/tecnico/')

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
		};
		
	}]);
	
	administrador.controller('MaquinariaController',['$http','$log','$scope',function($http,$log,$scope){
		
		$scope.fecha_revision = new Date();
		
		$scope.datosMaquina= function(maquinaid){
			$http.get('/api/maquinaria/'+maquinaid).success(function(data){
					$scope.numero_roma = data.numero_roma;
					$scope.TipoMaquina = data.TipoMaquina;
					$scope.MarcaModelo = data.MarcaModelo;
					$scope.fecha_adquisicion = new Date(data.fecha_adquisicion)
					$scope.fecha_revision2 = new Date(data.fecha_revision)
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
		};
		
		$scope.modMaquina = function(maquinaId,adminId){
			day = $scope.fecha_revision2.getDate();
			if(day.toString().length < 2){
				day = "0"+day.toString();
			}
			frev = $scope.fecha_revision2.toJSON().substring(0,8)+day;
			f_adq = document.getElementById("fecha_adquisicion").value;
			$http.put('/api/maquinaria/'+maquinaId,{numero_roma: $scope.numero_roma,fecha_adquisicion: f_adq,
				fecha_revision: frev, TipoMaquina: $scope.TipoMaquina, MarcaModelo: $scope.MarcaModelo, idAdmin: adminId,activo: 'SI'
				}).
				success(function(data,status,headers,config){
					location.reload();
				});
		};
		
		
		$scope.revisionMaquina = function(idMaquina){
			$http.get('/api/maquinaria/'+idMaquina).
			success(function(data){
			
			day = $scope.fecha_revision.getDate();
			if(day.toString().length < 2){
				day = "0"+day.toString();
			}
			frev = $scope.fecha_revision.toJSON().substring(0,8)+day;
			$http.put('/api/maquinaria/'+idMaquina,{numero_roma: data.numero_roma,fecha_adquisicion: data.fecha_adquisicion,
				fecha_revision: frev, TipoMaquina: data.TipoMaquina, MarcaModelo: data.MarcaModelo, idAdmin: data.idAdmin,activo: data.activo
				}).
				success(function(data,status,headers,config){
					location.reload();
				});
			});
		};
		
		$scope.cierraVentanta = function(maquinaId){
			$('#eliminaMaquina'+maquinaId).modal('toggle');
		};
		
		
		$scope.eliminarMaquina= function(maquinaid){
			$http.get('/api/maquinaria/'+maquinaid).success(function(data){
				maquina = {numero_roma: data.numero_roma,fecha_adquisicion: data.fecha_adquisicion,
				fecha_revision: data.fecha_revision, TipoMaquina: data.TipoMaquina, MarcaModelo: data.MarcaModelo, idAdmin: data.idAdmin,activo: 'NO'
				};		
					$http.put('/api/maquinaria/'+maquinaid,maquina).
						success(function(data,status,headers,config){
							location.reload();
					});
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
		};
		
	}]);

	administrador.controller("PanelController",function(){
		this.tab = 1;
		this.tab2 = 4;
		
		this.selectTab = function(setTab){
			this.tab = setTab;
		};
		this.isSelected = function(checkTab){
			return this.tab === checkTab;
		};
		this.selectTabSec = function(setTab){
			this.tab2 = setTab;
		};
		this.isSelectedSec = function(checkTab){
			return this.tab2 === checkTab;
		};
	});
	
	
	
	administrador.controller('AdministradorController',['$http','$log','$scope',function($http,$log,$scope){
		
		$scope.usuarios = [];
		$scope.municipios = [];
		$scope.provincias = [];
		$scope.cultivos = [];
		$scope.Inputs = [];
		$scope.Operaciones = [];
		$scope.Tipos = [];
		$scope.parcelasArray  = [];
		$scope.idExpSeleccionado;
		$scope.uhcSeleccion;
		$scope.maquinasusadas = [];
		$scope.tecnicos = [];		
		$scope.maquinas = [];
		$scope.muestra = false;
		$scope.muestra2 = false;
		$scope.tipoAplicador = 1;
		var tecnicosExplotacion = [];
		var maquinariaExplotacion = [];
		aplicadores = [];
		usuarios = [];
		temperatura=[];
		humedad=[];
		precipitacion=[];
		temp2=[];
		hum2=[];
		precip2=[];
		$scope.cultivosExplotacion = [];
		
		$scope.initialize = function(idAdmin,idExp){
			$scope.idExpSeleccionado = idExp;
			$http.get('/api/administradores/'+idAdmin).success(function(dato){
				dato = dato[0];
				$http.get('/api/explotaciones/'+idExp).success(function(dato2){	
					$scope.maquinasusadas = dato2.maquinarias;
					$scope.analisis = dato2.analisisExplotacion;
					$scope.parcelas = dato2.parcelasExplotacion;
					$scope.operaciones = dato2.operacionesExplotacion;
					$scope.muestras = dato2.muestrasExplotacion;
					uhcs = dato2.uhcs;
					
					for (i = 0; i < uhcs.length; i++){
				
						for (j = 0; j < uhcs[i].aplicaciones.length; j++){
								aplicaciones.push(uhcs[i].aplicaciones[j]);
						}
					}
					for (i = 0; i < dato2.aplicadores.length; i++){
						if(dato2.aplicadores[i].activo == 'SI'){
							aplicadores.push(dato2.aplicadores[i])
						}
					}
					for (i = 0; i < dato2.usuarios.length; i++){
						if(dato2.usuarios[i].activo == 'SI'){
							usuarios.push(dato2.usuarios[i])
						}
					}
					
					$scope.usuarios = usuarios;
					$scope.aplicadores = aplicadores;
					$scope.aplicaciones = aplicaciones;
					
					for (i = 0; i < dato.tecnicos.length; i++){
						var existe = false;
						for(j = 0; j < dato2.usuarios.length ; j++){
							if(dato.tecnicos[i].id == dato2.usuarios[j].idUsuario){
								existe = true;
							}
						}
						if(existe == false && dato.tecnicos[i].activo == "SI"){
							tecnicosExplotacion.push(dato.tecnicos[i]);
						}
					}
					if (tecnicosExplotacion.length > 0){
						$scope.muestra = true;
					}
					
					for (i = 0; i < dato.maquinaria.length; i++){
						var existe = false;
						for(j = 0; j < dato2.maquinarias.length ; j++){
							if(dato.maquinaria[i].id == dato2.maquinarias[j].idMaquina){
								existe = true;
							}
						}
						if(existe == false){
							maquinariaExplotacion.push(dato.maquinaria[i]);
						}
					}
					
					if (maquinariaExplotacion.length > 0){
						$scope.muestra2 = true;
					}
					$scope.tecnicos = tecnicosExplotacion;
					$scope.maquinas = maquinariaExplotacion;
					$http.get('/api/municipios/').
						success(function(data){
							$scope.municipios = data;
						}).
						error(function(data,status,headers,config){
							$log.log("Error");
						});
				});
				
			});
			$http.get('/api/cultivo').success(function(datoCultivo){	
					$scope.cultivos = datoCultivo; 
			});
			$http.get('/api/parcelas').success(function(datoParcelas){	
					$scope.parcelas = datoParcelas;
			});
			$http.get('/api/Tiposoperacion').success(function(datoTipo){	
					$scope.Tipos = datoTipo;
			});
			$http.get('/api/Inputoperacion').success(function(datoInput){	
					$scope.Inputs = datoInput;
			});
			$http.get('/api/operaciones').success(function(dataOp){	
					$scope.Operaciones = dataOp;
			});
				
		};
		$scope.initializeUHC = function(idAdmin,idExp,idUhc){
			$scope.uhcSeleccion = idUhc
			
			$scope.idExpSeleccionado = idExp;
			$http.get('/api/administradores/'+idAdmin).success(function(dato){
				dato = dato[0];
				
				
			});
			$http.get('/api/explotaciones/'+idExp).success(function(dato2){	
				
					$scope.maquinasusadas = dato2.maquinarias;
					$scope.analisis = dato2.analisisExplotacion;
					$scope.parcelas = dato2.parcelasExplotacion;
					$scope.operaciones = dato2.operacionesExplotacion;
					$scope.muestras = dato2.muestrasExplotacion;
					uhcs = dato2.uhcs;
					for (i = 0; i < uhcs.length; i++){
						
						for (j = 0; j < uhcs[i].aplicaciones.length; j++){
								aplicaciones.push(uhcs[i].aplicaciones[j]);
						}
					}
					for (i = 0; i < dato2.aplicadores.length; i++){
						if(dato2.aplicadores[i].activo == 'SI'){
							aplicadores.push(dato2.aplicadores[i])
						}
					}
					for (i = 0; i < dato2.usuarios.length; i++){
						if(dato2.usuarios[i].activo == 'SI'){
							usuarios.push(dato2.usuarios[i])
						}
					}
					
					$scope.usuarios = usuarios;
					$scope.aplicadores = aplicadores;
					$scope.aplicaciones = aplicaciones;
					
					for (i = 0; i < dato.tecnicos.length; i++){
						var existe = false;
						for(j = 0; j < dato2.usuarios.length ; j++){
							if(dato.tecnicos[i].id == dato2.usuarios[j].idUsuario){
								existe = true;
							}
						}
						if(existe == false && dato.tecnicos[i].activo == "SI"){
							tecnicosExplotacion.push(dato.tecnicos[i]);
						}
					}
					if (tecnicosExplotacion.length > 0){
						$scope.muestra = true;
					}
					
					for (i = 0; i < dato.maquinaria.length; i++){
						var existe = false;
						for(j = 0; j < dato2.maquinarias.length ; j++){
							if(dato.maquinaria[i].id == dato2.maquinarias[j].idMaquina){
								existe = true;
							}
						}
						if(existe == false){
							maquinariaExplotacion.push(dato.maquinaria[i]);
						}
					}
					
					if (maquinariaExplotacion.length > 0){
						$scope.muestra2 = true;
					}
					$scope.tecnicos = tecnicosExplotacion;
					$scope.maquinas = maquinariaExplotacion;
					$http.get('/api/municipios/').
						success(function(data){
							$scope.municipios = data;
						}).
						error(function(data,status,headers,config){
							$log.log("Error");
						});
				});
			$http.get('/api/cultivo').success(function(datoCultivo){	
					$scope.cultivos = datoCultivo; 
			});
			$http.get('/api/cultivoexplotacion').success(function(datoCultivosExplotacion){	
					$scope.cultivosExplotacion = datoCultivosExplotacion; 
			});
			$http.get('/api/parcelauhc').success(function(datoParcelas){
					lista= [];
					for(j = 0; j < datoParcelas.length ; j++){
						if (datoParcelas[j].idUHC == idUhc){
							lista.push(datoParcelas[j])
						}	
					}						
					$scope.parcelas = lista;
			});
			$http.get('/api/Tiposoperacion').success(function(datoTipo){	
					$scope.Tipos = datoTipo;
			});
			$http.get('/api/Inputoperacion').success(function(datoInput){	
					$scope.Inputs = datoInput;
			});
			$http.get('/api/operaciones').success(function(dataOp){	
					lista= [];
					for(j = 0; j < dataOp.length ; j++){
						if (dataOp[j].idUHC == idUhc){
							lista.push(dataOp[j])
						}							
					}
					$scope.Operaciones = lista;
			});
			$http.get('/api/municipios').success(function(dataMun){	
					$scope.municipios = dataMun;
			});
			$http.get('/api/provincias').success(function(dataPro){	
					$scope.provincias = dataPro;
			});
				
		};
		
		//Parcelas
		var parcelas = [];
		var analisis = [];
		var aplicaciones = [];
		var uhcs = [];
		
		
		$scope.guardarUHC = function(idExp){
			uhc = {nombre : $scope.nombreUHC,idExplotacion : idExp};


			
			$http.post('/api/uhcs/',uhc).
			success(function(data,status,headers,config){
				location.replace('/tecnico/explotacion/'+idExp)

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
		}
		$scope.cambia = function(idExp){

			window.location = "/tecnico/explotacion/"+idExp+"/"+$scope.uhcSeleccionado;
		
		};
		$scope.borrarParcela = function(idPar){
			$http.delete('/api/parcelauhc/'+idPar).
				success(function(data,status,headers,config){
					var index = 0;
					parcelas = $scope.parcelas;
					for (i=0; i<parcelas.length; i++){
						if(parcelas[i].id == idPar){
							index = i;
						}
					}
					parcelas.splice(index,1);
					$scope.parcelas = parcelas;
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
		
		}
		$scope.cambioInput = function(){
			idInput = document.getElementById("inputOp").value;
			$http.get('/api/Inputoperacion/'+idInput).success(function(dataInput){	
					$scope.cantidadOperacion = dataInput.cantidad;
					$scope.unidadOperacion = dataInput.unidad;
					$scope.coefEmisionOperacion = dataInput.coefEmision;
					$scope.unidadCoefOperacion = dataInput.unidadCoef;
					$scope.coefAsigOperacion = dataInput.coefAsignacion;
					$scope.costeUnitarioOperacion = dataInput.costeUnitario;
					
					

			});
		}
		
		//explotacionHTML
		
		$scope.guardarParcela = function(idExpl){ 
			
			idParcela = document.getElementById("parcelaSeleccionado").value;
			idUhc = document.getElementById("uhcSeleccionado").value;
			
			parcela = {idUHC : idUhc,idParcela: idParcela,idExplotacion: idExpl};
			/*parcela = {nombre: $scope.nombreParcela,provincia: $scope.provinciaSeleccionada,municipio: $scope.municipioSeleccionado, poligono: poli,parcela: parce ,recinto: recin,superficie_hectareas: $scope.superficie, sr: $scope.sr, idUHC: $scope.ParcelaUHC,descripcion: desc,idExplotacion: idexp,idcultivo: $scope.ParcelaCultivo};*/
			
			//location.replace('/crearParcela/'+ $scope.nombreParcela+'/'+$scope.provinciaSeleccionada+'/'+$scope.municipioSeleccionado+'/'+poli+'/'+parce+'/'+recin+'/'+$scope.superficie+'/'+$scope.sr+'/'+idUHC+'/'+desc+'/'+idexp+'/'+idCul)
			$http.post('/api/parcelauhc/',parcela).
			success(function(data,status,headers,config){
				
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
			
		};
		$scope.guardarCultivo = function(idExp,idUHC){
			superficie = $scope.superficieCultivo;
			idCult = $scope.cultivoCult;
			cultivo = {idCultivo : idCult,superficieCultivo:superficie,idExplotacion : idExp,idUHC: idUHC};
			
			$http.post('/api/cultivoexplotacion/',cultivo).
			success(function(data,status,headers,config){
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
				
			};
		
		this.todasSeleccionadas = function(dato){
			return dato=="";
		};
		
			
			$scope.eliminar = function(dato,palabra){
				if(palabra == "parcela"){
					$http.delete('/api/parcelas/'+dato).
				success(function(data,status,headers,config){
					var index = 0;
					parcelas = $scope.parcelas;
					for (i=0; i<parcelas.length; i++){
						if(parcelas[i].id == dato){
							index = i;
						}
					}
					parcelas.splice(index,1);
					$scope.parcelas = parcelas;
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
				}else if(palabra == "aplicacion"){
					$http.delete('/api/aplicaciones/'+dato).
				success(function(data,status,headers,config){
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
				}
			};
			
			$scope.editar = function(parcela){
				$http.get('/api/parcelas/'+parcela).success(function(data){
					
				$scope.ParcelaUHC2 = data.idUHC;
				$scope.provinciaSeleccionada = data.provincia;
				$http.get('/api/municipios/'+data.municipio).success(function(dataMun){
					$scope.municipioParcela = dataMun
				});
				$scope.nombreParcela2 = data.nombre;
				$scope.poligono2 = data.poligono;
				$scope.parcela2 = data.parcela;
				$scope.recinto2 = data.recinto;
				$scope.superficie2 = data.superficie_hectareas;
				$scope.sr2 = data.sr;
				$scope.descripcion2 = data.descripcion;

				});
				
			};
			
			$scope.cerrarParcela = function(parcela){
				$('#Eliminar'+parcela).modal('toggle');
			};
			
			// fin parcela
			
			
			
			
		
		$scope.creaUHC = function(idExp){
			uhc = document.getElementById("uhcid").value;
			$http.post('/api/uhcs/',{nombre: uhc,idExplotacion: idExp}).
			success(function(data,status,headers,config){
				location.reload();
			});
		};
		
		$scope.formateaFecha = function(fecha){
			return fecha.substring(8, 10)+"/"+fecha.substring(5, 7)+"/"+fecha.substring(0, 4);
		};
		
		$scope.guardarUsuarios = function(idExp){
			elementos = document.getElementsByClassName("blankCheckbox");
			usuarios = $scope.usuarios;
			for (i = 0; i < elementos.length; i++){
				var existe = false;
				if(elementos[i].checked){
					$http.post('/api/usuarioExplotacion/',{idUsuario: elementos[i].value,idExplotacion: idExp}).
					success(function(data,status,headers,config){
						$http.get('/api/tecnicos/'+data.idUsuario).success(function(dato){	
							for (i = 0;i< tecnicosExplotacion.length; i++){
								if (tecnicosExplotacion[i].id == dato.id){
									tecnicosExplotacion.splice(i,1);
								}
							}
							$scope.tecnicos = tecnicosExplotacion;
							usuarios = $scope.usuarios;
							usuarios.push(data);
							$scope.usuarios = usuarios;
							
							if(tecnicosExplotacion.length == 0){
								$scope.muestra = false;
							}
							
						});

					}).
					error(function(data,status,headers,config){
						$log.log(data)
					});
					
				}
			}
			$('#AsignarUsuarios'+idExp).modal('toggle');

		};
		
		$scope.guardarMaquinas = function(idExp){
			elementos = document.getElementsByClassName("blankCheckbox2");
			maquinas = $scope.maquinasusadas;
			for (i = 0; i < elementos.length; i++){
				var existe = false;
				if(elementos[i].checked){
					$http.post('/api/maquinaExplotacion/',{idMaquina: elementos[i].value,idExplotacion: idExp}).
					success(function(data,status,headers,config){
						$http.get('/api/maquinaria/'+data.idMaquina).success(function(dato){	
							for (i = 0;i< maquinariaExplotacion.length; i++){
								if (maquinariaExplotacion[i].id == dato.id){
									maquinariaExplotacion.splice(i,1);
								}
							}
							$scope.maquinas = maquinariaExplotacion;
							maquinas = $scope.maquinasusadas;
							maquinas.push(data);
							$scope.maquinasusadas = maquinas;
							
							if(maquinariaExplotacion.length == 0){
								$scope.muestra2 = false;
							}
							
						});

					}).
					error(function(data,status,headers,config){
						$log.log(data)
					});
				}
			}
			$('#AsignarMaquina'+idExp).modal('toggle');

		};
		
		$scope.creaAplicador = function(idExp){
		
			var razon = $scope.razon_social;
			if($scope.razon_social == null){
				razon = "Persona física";
			}
			
			day1 = $scope.fecha_validez.getDate();
			if(day1.toString().length < 2){
				day1 = "0"+day1.toString();
			}
			f_validez = $scope.fecha_validez.toJSON().substring(0,8)+day1;
			
			day2 = $scope.fecha_expedicion.getDate();
			if(day2.toString().length < 2){
				day2 = "0"+day2.toString();
			}
			f_exp = $scope.fecha_expedicion.toJSON().substring(0,8)+day2;
			
			$http.post('/api/aplicadores/',{Aplicador: $scope.tipoAplicador,nombre: $scope.nombre,apellido1: $scope.apellido1,apellido2: $scope.apellido2,
			razon_social: razon,dni : $scope.dni,fecha_validez : f_validez,fecha_expedicion : f_exp,
			Telefono: $scope.Telefono,Fax : $scope.Fax,email : $scope.email ,idExplotacion: idExp,activo:'SI'}).
			success(function(data,status,headers,config){
				aplicadores = $scope.aplicadores;
				aplicadores.push(data);
				$scope.aplicadores = aplicadores;
				$("#nuevoAplicador").modal('toggle');
				document.getElementById("formAplicadores").reset();
			}).
			error(function(data,status,headers,config){
				$log.log(data);
			});
		};

		$scope.crearDatoClimatico = function(idExp){
		
			fdato = document.getElementById("fechaDato").value;
			estacion = document.getElementById("EstacionClimatica").value;
			temp = document.getElementById("Temperatura").value;
			tempMax = document.getElementById("TempMax").value;
			tempMin = document.getElementById("TempMin").value;
			tempMed = document.getElementById("TempMed").value;
			humedad = document.getElementById("Humedad").value;
			humMax = document.getElementById("HumMax").value;
			humMin = document.getElementById("HumMin").value;
			humMed = document.getElementById("HumMed").value;
			precipitacion = document.getElementById("Precipitacion").value;
		

			$http.post('/api/datosClimaticos/',{EstacionClimatica: estacion,Temperatura: temp,
			TempMax: tempMax,TempMin: tempMin,TempMed:tempMed,Humedad: humedad,HumMax: humMax,
			HumMin: humMin,HumMed: humMed,Precipitacion: precipitacion,fecha: fdato,idExplotacion: idExp}).
			success(function(data,status,headers,config){
				$log.log("creado");
			}).
			error(function(data,status,headers,config){
				$log.log(data)
			});
			$('#nuevoDatoClimático').modal('toggle');

		};
		
		$scope.cerrar = function(dato,id){
			$(dato+""+id).modal('toggle');
		}
		
		$scope.designarUsuario= function(usid,tecid){
		
			$http.delete('/api/usuarioExplotacion/'+usid).
				success(function(data,status,headers,config){
					$http.get('/api/tecnicos/'+tecid).success(function(dato){	
						usuarios = $scope.usuarios;
				
						for (i = 0;i< usuarios.length; i++){
							if (usuarios[i].id == usid){
								usuarios.splice(i,1);
							}
						}

						$scope.usuarios = usuarios;
						tecnicosExplotacion.push(dato);
						$scope.muestra = true;
						$('#designarUsuario'+usid).modal('toggle');
					});
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
		};
		
		$scope.designarMaquina= function(maqid,maqexpid){
		
			$http.delete('/api/maquinaExplotacion/'+maqexpid).
				success(function(data,status,headers,config){
					$http.get('/api/maquinaria/'+maqid).success(function(dato){	
						maq_usadas = $scope.maquinasusadas;
				
						for (i = 0;i< maq_usadas.length; i++){
							if (maq_usadas[i].id == maqexpid){
								maq_usadas.splice(i,1);
							}
						}

						$scope.maquinasusadas = maq_usadas;
						maquinariaExplotacion.push(dato);
						$scope.muestra2 = true;
						$('#designarMaquina'+maqid).modal('toggle');
					});
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
		};
		
		$scope.eliminarAplicador= function(apid,idExp){
			$http.get('/api/aplicadores/'+apid).success(function(data){
				aplicador = {Aplicador: data.Aplicador,nombre: data.nombre,apellido1: data.apellido1,apellido2: data.apellido2,
			razon_social: data.razon_social,dni : data.dni,fecha_validez : data.fecha_validez,fecha_expedicion : data.fecha_expedicion,
			Telefono: data.Telefono,Fax : data.Fax,email : data.email ,idExplotacion: idExp,activo:'NO'};		
				$http.put('/api/aplicadores/'+apid,aplicador).
				success(function(data3,status,headers,config){
					aplicadores = $scope.aplicadores;
					
					for (i = 0;i< aplicadores.length; i++){
						if (aplicadores[i].id == apid){
							aplicadores.splice(i,1);
						}
					}
					$('#eliminarAplicador'+maqid).modal('toggle');
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
			});
		
		};
		
		var nombreTecnico = "";
		var productos = [];
		$scope.sp=100;
		
		$scope.isSelectedParcial = function(sp){
			if(sp==1){

				return false;
			}else{
				$scope.porcentaje = 100;
				return true;
			}
		};
		
		var id = 0;
		
		//Guardar aplicacion ventana UHC seleccionado
		
		$scope.guardarAplicacion = function(tecnicoID){

			day1 = $scope.fechaaplicacion.getDate();
			if(day1.toString().length < 2){
				day1 = "0"+day1.toString();
			}
			day2 = $scope.fechatratamiento.getDate();
			if(day2.toString().length < 2){
				day2 = "0"+day2.toString();
			}
			
			
			time = $scope.mytime.getHours();
			if(time.toString().length < 2){
				time = "0"+time.toString();
			}
			
			var obs = $scope.observaciones;
			if( obs == null){
				obs = "Sin observaciones"
			}
			
			hras = $scope.horasAp;
			if(hras == null || hras == ''){
				hras = '0';
			}
			
			aplicacion = {fecha_Aplicacion: $scope.fechaaplicacion.toJSON().substring(0,8)+day1,numero_orden_tratamiento: $scope.n_tratamiento,fecha_Orden_tratamiento: $scope.fechatratamiento.toJSON().substring(0,8)+day2,
			gasto_caldo: $scope.g_caldo, superficie_tratada: $scope.superficie_tratada,porcentaje: $scope.porcentaje,
			distribucion_ap: $scope.distribucion_ap,condiciones_aplicacion: $scope.condiciones_ap,presion_tratamiento: $scope.presion,
			velocidad_tratamiento: $scope.velocidad,aplicador: $scope.aplicadorSeleccionado,maquinaria: $scope.maquinariaSeleccionado,idUHC: $scope.AplicacionUHC,hora_aplicacion: time+$scope.mytime.toJSON().substring(13,24)
			,observaciones: obs,tecnico :tecnicoID, horas: hras}
			$http.post('/api/aplicaciones/',aplicacion).
			success(function(data,status,headers,config){
				
				window.location = "/administrador/aplicacion/"+data.id;
				
			}).
			error(function(data,status,headers,config){
				$log.log(data);
			});
			
		
			
		
		};
		
	}]);
	
	administrador.controller('EditaParcela',['$http','$log','$scope',function($http,$log,$scope){
	
		var provincias = [];
		var municipios = [];
		
		$scope.guardarParcelaExplotacion = function(idParcela,explotacion,provincia,municipio,idCult){
			mun = document.getElementById('munSeleccionado').value;
			parcela = {nombre: $scope.nombreParcela2,provincia: $scope.provinciaSeleccionada ,municipio: mun, poligono: $scope.poligono2,parcela: $scope.parcela2 ,recinto: $scope.recinto2,superficie_hectareas: $scope.superficie2 ,sr: $scope.sr2, idUHC: $scope.ParcelaUHC2,descripcion: $scope.descripcion2,idExplotacion: explotacion,idcultivo:idCult};

			$http.get('/api/parcelas/'+idParcela).
			success(function(data,status,headers,config){
				data.nombre = $scope.nombreParcela2;
				data.provincia =  $scope.provinciaSeleccionada;
				data.municipio = mun;
				data.poligono = $scope.poligono2;
				data.parcela = $scope.parcela2 ;
				data.recinto = $scope.recinto2;
				data.superficie_hectareas = $scope.superficie2 ;
				data.sr = $scope.sr2;
				data.descripcion =  $scope.descripcion2;
				data.idUHC = $scope.ParcelaUHC2;
				$http.put('/api/parcelas/'+idParcela,data).
				success(function(data,status,headers,config){
					location.reload();

				}).
				error(function(data,status,headers,config){
					$log.log(data);

				});

			}).
			error(function(data,status,headers,config){
				$log.log(data);

			});
			
		
		};
	
	}]);

	administrador.controller('CreaAplicacion',['$http','$log','$scope',function($http,$log,$scope){
	
		var nombreTecnico = "";
		var productos = [];
		$scope.sp=100;
		//$scope.productos = [];
		
		$scope.open = function($event) {
			$event.preventDefault();
			$event.stopPropagation();

			$scope.opened = true;
		};
		
		$scope.isSelectedParcial = function(sp){
			if(sp==1){

				return false;
			}else{
				$scope.porcentaje = 100;
				return true;
			}
		};
		
		var id = 0;
		
		$scope.aplicadores = function(explotacion) {
			
			$http.get('/api/explotaciones/'+explotacion).success(function(data){
				$scope.aplicadores = data.aplicadores;
				$scope.maquinas = data.maquinarias;
			});
			

		};
		

		$scope.guardarAplicacion = function(){
			day1 = $scope.fechaaplicacion.getDate();
			if(day1.toString().length < 2){
				day1 = "0"+day1.toString();
			}
			day2 = $scope.fechatratamiento.getDate();
			if(day2.toString().length < 2){
				day2 = "0"+day2.toString();
			}
			
			
			time = $scope.mytime.getHours();
			if(time.toString().length < 2){
				time = "0"+time.toString();
			}
			
			var obs = $scope.observaciones;
			if( obs == null){
				obs = "Sin observaciones"
			}
			hras = $scope.horasAp;
			if(hras == null || hras == ''){
				hras = '0';
			}
			
			$http.post('/api/aplicaciones/',{fecha_Aplicacion: $scope.fechaaplicacion.toJSON().substring(0,8)+day1,numero_orden_tratamiento: $scope.n_tratamiento,fecha_Orden_tratamiento: $scope.fechatratamiento.toJSON().substring(0,8)+day2,
			gasto_caldo: $scope.g_caldo, superficie_tratada: $scope.superficie_tratada,porcentaje: $scope.porcentaje,
			distribucion_ap: $scope.distribucion_ap,condiciones_aplicacion: $scope.condiciones_ap,presion_tratamiento: $scope.presion,
			velocidad_tratamiento: $scope.velocidad,aplicador: $scope.aplicadorSeleccionado,maquinaria: $scope.maquinariaSeleccionado,idUHC: $scope.AplicacionUHC,hora_aplicacion: time+$scope.mytime.toJSON().substring(13,24)
			,observaciones: obs,tecnico: $scope.AplicacionTecnico,horas: hras}).
			success(function(data,status,headers,config){
				
				window.location = "/administrador/aplicacion/"+data.id;
			}).
			error(function(data,status,headers,config){
				$log.log(data);
			});
			
		
			
		
		};
		
	}]);
	
	administrador.controller('CreaOperacion',['$http','$log','$scope',function($http,$log,$scope){
	
		var nombreTecnico = "";
		var productos = [];
		$scope.riqueza_n = 0;
		$scope.riqueza_p = 0;
		$scope.riqueza_k = 0;
		$scope.riqueza_Ca = 0;
		$scope.riqueza_Mg = 0;
		$scope.riqueza_S = 0;
		$scope.riqueza_otros = 0;
		$scope.dosis = 0;
		$scope.nitrogeno = 0;
		$scope.fosforo = 0;
		$scope.potasio = 0;
		$scope.potasio = 0;
		$scope.unidad_dosis = "Kg/Ha";
		$scope.superficie_recogida = 0;
		var operacionTipo = "";
		
		$scope.iniciaOperacion = function(idOp,idExp){
			$scope.idExpSeleccionado = idExp;
			$http.get('/api/operaciones/'+idOp).success(function(data){
				$log.log("Te inicias aqui")
				$scope.fecha_operacion = new Date(data.fecha_operacion);
				$scope.operacionTipo = data.idTipoOperacion;
				$scope.operacionInput = data.idInputOperacion;
				$scope.cantidadOperacion = data.cantidad;
				$scope.unidadOperacion = data.unidad;
				$scope.coefEmisionOperacion = data.coefEmision;
				$scope.unidadCoefOperacion = data.unidadCoef;
				$scope.coefAsigOperacion = data.coefAsignacion;
				$scope.costeUnitarioOperacion = data.costeUnitario;
				$scope.observacionesOperacion = data.observaciones;
				$scope.costeTotalAux = data.costeTotal;
				$scope.emisionTotalAux = data.	emisionesTotal;
				$scope.OperacionUHC = data.idUHC;
				$scope.observaciones = data.observaciones;
				$scope.OperacionTecnico = data.tecnico;
				$scope.horasOp = data.horas;
				$scope.tipoOp = data.tipoOp;
				$scope.idExplotacion = data.idExplotacion;
				$scope.idTipoOperacion = data.idTipoOperacion;
				$scope.idInputOperacion = data.idInputOperacion;
				$scope.coefEmision = data.coefEmision;
				$scope.cantidad = data.cantidad;
				$scope.coefAsignacion = data.coefAsignacion;
				$scope.costeUnitario = data.costeUnitario;
				$scope.unidad = data.unidad;
				$scope.unidadCoef = data.unidadCoef;
				operacionTipo = data.tipoOp;
			

				
				
			});
			$http.get('/api/Tiposoperacion/').success(function(dataTipoOperación){
				$scope.Tipos = dataTipoOperación;
			});
			$http.get('/api/Inputoperacion/').success(function(dataInputoperacion){
				$scope.Inputs = dataInputoperacion;
			});
		};
		
		
		$scope.actualizaN = function(){
			$scope.nitrogeno = ($scope.riqueza_n) * ($scope.dosis) / 100;
		};
		$scope.actualizaP = function(){
			$scope.fosforo = ($scope.riqueza_p) * ($scope.dosis) / 100;
		};
		$scope.actualizaK = function(){
			$scope.potasio = ($scope.riqueza_k) * ($scope.dosis) / 100;
		};
		$scope.actualizaDosis = function(){
			$scope.nitrogeno = ($scope.riqueza_n) * ($scope.dosis) / 100;
			$scope.fosforo = ($scope.riqueza_p) * ($scope.dosis) / 100;
			$scope.potasio = ($scope.riqueza_k) * ($scope.dosis) / 100;
		};
		
		
		$scope.guardarOperacion = function(expid,tecid,tipoUs,idUhc){

			f_op = document.getElementById("fecha_operacion").value;
			
			var obs = $scope.observacionesOperacion;
			if( obs == '' || obs == undefined){
				obs = "Sin observaciones"
			}
			hras = $scope.horasOp;
			if(hras == null || hras == ''){
				hras = '0';
			}
				$http.get('/api/uhcs/'+idUhc).
						success(function(datauhc1){
					
							
					
			emisionTotal = $scope.cantidadOperacion*$scope.coefEmisionOperacion*$scope.coefAsigOperacion*parseFloat(datauhc1.superficie_hectareas);
			cosTotal = $scope.cantidadOperacion*$scope.coefAsigOperacion*$scope.costeUnitarioOperacion*parseFloat(datauhc1.superficie_hectareas);
			//$scope.fechaaplicacion.toJSON().substring(0,8)+day1
			operacion = {fecha_operacion: f_op,idUHC: idUhc,observaciones: obs,idExplotacion: expid,tecnico: tecid,horas: hras,idTipoOperacion: $scope.operacionTipo,idInputOperacion:$scope.operacionInput,cantidad:$scope.cantidadOperacion,unidad:$scope.unidadOperacion,coefEmision:$scope.coefEmisionOperacion,unidadCoef:$scope.unidadCoefOperacion,coefAsignacion:$scope.coefAsigOperacion,costeUnitario:$scope.costeUnitarioOperacion,emisionesTotal:emisionTotal,costeTotal:cosTotal};
		
			$http.post('/api/operaciones/',operacion).
			success(function(data,status,headers,config){
				$http.get('/api/uhcs/'+idUhc).
						success(function(datauhc){
							costeT2 = parseFloat(datauhc.costeAsociado) + parseFloat(cosTotal);
							indT2 = parseFloat(datauhc.indicadorEvAmbiental) + parseFloat(emisionTotal);
							costeT2 = costeT2.toFixed(2);  
							indT2 = indT2.toFixed(5);  
							datauhc.costeAsociado = parseFloat(costeT2);
							datauhc.indicadorEvAmbiental = parseFloat(indT2);
							$http.put('/api/uhcs/'+idUhc,datauhc).
							success(function(data,status,headers,config){
								location.reload();
							}).
							error(function(datauhc,status,headers,config){
								$log.log(datauhc);
							});	
						}).
						error(function(datauhc,status,headers,config){
							$log.log("Error");
						});
				//location.reload()
			}).
			error(function(data,status,headers,config){
				$log.log(data);
			});
				}).
						error(function(datauhc1,status,headers,config){
							$log.log("Error");
						});

			
		
		};
		

		$scope.cancelar = function(){
			$scope.editaOp = false;
		};
		
		$scope.editaOperacion = function(){
			$scope.editaOp = true;
		};
		$scope.volver = function(idExpl, idUhc){
			location.replace('/tecnico/explotacion/'+idExpl+'/'+idUhc)
		};
		
		$scope.modificarOperacion = function(idOp,idExp,tipoId,tipoNombr,tecid,idUhc){
		
			f_op = document.getElementById("fecha_operacion").value;
			
			var obs = $scope.observacionesOperacion;
			if(obs == null || obs == ""){
				obs = "Sin observaciones"
			}
			$log.log($scope.tipoOp)
			$log.log(operacionTipo)
			
			hras = $scope.horasOp;
			if(hras == null || hras == ''){
				hras = '0';
			}
			cosTotalAux = $scope.costeTotalAux;
			emisionTotalAux = $scope.emisionTotalAux; 
			$http.get('/api/uhcs/'+idUhc).
			success(function(datauhc){
				emisionTotal = $scope.cantidadOperacion*$scope.coefEmisionOperacion*$scope.coefAsigOperacion*parseFloat(datauhc.superficie_hectareas);
				emisionTotalaux = emisionTotal.toFixed(5);
				cosTotal = $scope.cantidadOperacion*$scope.coefAsigOperacion*$scope.costeUnitarioOperacion*parseFloat(datauhc.superficie_hectareas);
				cosTotalAux2 = cosTotal.toFixed(2);
				operacion = {idUHC:idUhc,idExplotacion:idExp,fecha_operacion: f_op,observaciones: obs,tecnico: tecid,horas: hras,idTipoOperacion: $scope.operacionTipo,idInputOperacion:$scope.operacionInput,cantidad:$scope.cantidadOperacion,unidad:$scope.unidadOperacion,coefEmision:$scope.coefEmisionOperacion,unidadCoef:$scope.unidadCoefOperacion,coefAsignacion:$scope.coefAsigOperacion,costeUnitario:$scope.costeUnitarioOperacion,emisionesTotal:emisionTotalaux,costeTotal:cosTotalAux2};
						
				$http.put('/api/operaciones/'+idOp,operacion).
				success(function(data,status,headers,config){

					
								datauhc.costeAsociado = parseFloat(datauhc.costeAsociado) - parseFloat(cosTotalAux);
								datauhc.indicadorEvAmbiental = parseFloat(datauhc.indicadorEvAmbiental) - parseFloat(emisionTotalAux);
								costeT2 = parseFloat(datauhc.costeAsociado) + parseFloat(cosTotal);
								indT2 = parseFloat(datauhc.indicadorEvAmbiental) + parseFloat(emisionTotal);
								costeT2 = costeT2.toFixed(2);  
								indT2 = indT2.toFixed(5);  
								datauhc.costeAsociado = parseFloat(costeT2);
								datauhc.indicadorEvAmbiental = parseFloat(indT2);
								$http.put('/api/uhcs/'+idUhc,datauhc).
								success(function(data2,status,headers,config){
									location.reload();
								}).
								error(function(data2,status,headers,config){
									$log.log(datauhc);
								});	
					}).
					error(function(data,status,headers,config){
						$log.log("Error");
					});
				}).
				error(function(datauhc,status,headers,config){
					$log.log("Error");
				});
					
					
			
		
			
			
		
		};
		
		
	}]);

	administrador.controller('CreaAnalisis',['$http','$log','$scope',function($http,$log,$scope){
	
		var nombreTecnico = "";
		
		$scope.tecnicoNombre = function(idTecnico) {
			$http.get('/api/tecnicos/'+idTecnico).success(function(data){
			nombreTecnico = data.Nombre;});
			return nombreTecnico;
		};
		
		$scope.guardarAnalisis = function(idExp,tecnid,tipoUs){
			
			fm = document.getElementById("fechamuestra").value;
			fe = document.getElementById("fechaemision").value;
			
			obs = $scope.obsm;
			if (obs == null){
				obs = "Sin observaciones";
			}
			acc = $scope.accm;
			if (acc == null){
				acc = "Sin acciones";
			}
			
			desc = $scope.desm;
			if (desc == null){
				desc = "Sin descripción";
			}
			hras = $scope.horasAn;
			if(hras == null || hras == ''){
				hras = '0';
			}
			
			analisis = {fecha_muestra: fm,idUHC: $scope.AnalisisUHC,tipo: $scope.tipom
			,descripcion: desc,laboratorio: $scope.laboratorio,numero_informe: $scope.informeLaboratorio,
			fecha_emision: fe,observaciones: obs,acciones: acc,idExplotacion : idExp,tecnico: tecnid,horas: hras};
			
			
			$http.post('/api/analisis/',analisis).
			success(function(data,status,headers,config){
				window.location = "/"+tipoUs+"/analisis/"+data.id;

			}).
			error(function(data,status,headers,config){
				$log.log(data);

			});
		};
		
	}]);
	
	administrador.controller('CreaParcela',['$http','$log','$scope',function($http,$log,$scope){
	
		
		$scope.iniParcela = function(){

			$http.get('/api/municipios/').
				success(function(data){
					$scope.municipios = data;
				}).
				error(function(data,status,headers,config){
					$log.log("Error");
				});
		
		};
		
		
		$scope.guardarParcela = function(idexp){

			poli = $scope.poligono;
			parce = $scope.parcela;
			recin = $scope.recinto;
			desc = $scope.descripcion;
			
			while(String(poli).length < 3){
				poli = "0"+poli;
			}
			while(String(parce).length < 5){
				parce = "0"+parce;
			}
			while(String(recin).length < 5){
				recin = "0"+recin;
			}
			
			if($scope.descripcion == null){
				desc = "Sin descripción";
			}
			
			$http.post('/api/parcelas/',{nombre: $scope.nombreParcela,provincia: $scope.provinciaSeleccionada,municipio: $scope.municipioSeleccionado, poligono: poli
			,parcela: parce ,recinto: recin,superficie_hectareas: $scope.superficie ,sr: $scope.sr, idUHC: $scope.ParcelaUHC,descripcion: desc,idExplotacion: idexp}).
			success(function(data,status,headers,config){
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
		
		};
	
	}]);
	
	
	administrador.controller('codigo',['$http','$log','$scope',function($http,$log,$scope){
	
		$scope.dynamicPopover =$scope.parcela.nombre;
		$scope.dynamicPopoverTitle = 'Title';
		
		$scope.munPar = function(municipioid){
			var municipio = 0;
			$http.get('/api/municipios/'+municipioid).
			
			success(function(data){
				$scope.munip=data.CodMunicipio;
			});
		};
		
		$scope.stringan = function(provinciaid,num){
			var n = provinciaid.toString();
			while (n.length < num){
				n = "0"+n;
			}
			return n;
		};
		
		
		
		
	}]);
	
	administrador.controller('Aplicacion',['$http','$log','$scope',function($http,$log,$scope){
	
		var productos = [];
		$scope.modifica = false;
		
		$scope.iniciaAplicacion = function(idAp){
			$http.get('/api/aplicaciones/'+idAp).success(function(data){
				
				$scope.fechaaplicacion = new Date(data.fecha_Aplicacion);
				$scope.n_tratamiento = data.numero_orden_tratamiento;
				$scope.fechatratamiento = new Date(data.fecha_Orden_tratamiento);
				$scope.g_caldo = data.gasto_caldo;
				$scope.superficie_tratada = data.superficie_tratada;
				$scope.porcentaje = data.porcentaje;
				if (data.porcentaje != 100){
					$scope.sp = 1;
				}else{
					$scope.sp = 100;
				}
				$scope.distribucion_ap = data.distribucion_ap;
				$scope.condiciones_ap = data.condiciones_aplicacion;
				$scope.presion = data.presion_tratamiento;
				$scope.velocidad = data.velocidad_tratamiento;
				$scope.aplicadorSeleccionado = data.aplicador;
				$scope.AplicacionUHC = data.idUHC;
			    $scope.maquinariaSeleccionado = data.maquinaria;
				fecha = new Date();
				fecha.setHours(data.hora_aplicacion.substring(0,2));
				fecha.setMinutes(data.hora_aplicacion.substring(3,5));
				fecha.setSeconds(data.hora_aplicacion.substring(6,8));
				$scope.mytime = fecha;
				$scope.observaciones = data.observaciones;
				$scope.AplicacionTecnico = data.tecnico;
				$scope.horasAp = data.horas;
				
			});
		};
		
		$scope.guardarProducto = function(aplicacion){
			var obs = $scope.obs
			if( obs = ""){
				obs = "Sin observaciones"
			}
		
			var nuevo_producto = {
				nombre: $scope.producto,
				dosis: $scope.dosis,
				materia_activa: $scope.materia,
				riqueza: $scope.riqueza,
				objeto: $scope.objeto,
				justific: $scope.justificacion,
				casa_comercial: $scope.c_com,
				n_registro: $scope.n_reg,
				empresa_distribuidora: $scope.e_distrib,
				observaciones: obs,
				aplicacion: aplicacion};
				
			$http.post('/api/productos/',nuevo_producto).
				success(function(data,status,headers,config){
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
				});
		};
		
		$scope.cerrar = function(productoid){
			$('#EliminarProducto'+productoid).modal('toggle');
		};
		
		$scope.goUHC = function(){
			alert("entra")
			window.location = "/tecnico/explotacion/"+idExplotacion+"/"+idUHC;
		};
		
		$scope.cancelar = function(){
			$scope.editaAp = false;
		};
		
		$scope.editaAplicacion = function(){
			$scope.editaAp = true;
		};
		
		$scope.eliminarProducto = function(productoid){
			$http.delete('/api/productos/'+productoid).
				success(function(data,status,headers,config){
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
				});
		};
		$scope.modificarAplicacion = function(idAp,idExp,idTecnico){
		
			fap = document.getElementById("fechaaplicacion").value;
			ftrat = document.getElementById("fechatratamiento").value;
			
			obs = $scope.observaciones;
			if (obs == ""){
				obs = "Sin observaciones";
			}
			
			time = $scope.mytime.getHours();
			if(time.toString().length < 2){
				time = "0"+time.toString();
			}
			hras = $scope.horasAp;
			if(hras == null || hras == ''){
				hras = '0';
			}

			aplicacion = {fecha_Aplicacion: fap,numero_orden_tratamiento: $scope.n_tratamiento,fecha_Orden_tratamiento: ftrat,
			gasto_caldo: $scope.g_caldo, superficie_tratada: $scope.superficie_tratada,porcentaje: $scope.porcentaje, 
			distribucion_ap: $scope.distribucion_ap, condiciones_aplicacion: $scope.condiciones_ap, presion_tratamiento: $scope.presion,
			velocidad_tratamiento: $scope.velocidad, aplicador: $scope.aplicadorSeleccionado, idUHC: $scope.AplicacionUHC,
			maquinaria: $scope.maquinariaSeleccionado,hora_aplicacion: time+$scope.mytime.toJSON().substring(13,24),observaciones: obs,
			idExplotacion : idExp,tecnico: idTecnico, horas: hras};
			
			
			$http.put('/api/aplicaciones/'+idAp,aplicacion).
			success(function(data,status,headers,config){
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);

			});
		};
		
	
	}]);
	
	administrador.controller('ParcelasController',['$http','$log','$scope',function($http,$log,$scope){
		
		var parcelas = [];
		var analisis = [];
		var aplicaciones = [];
		var uhcs = [];
		
		this.todasSeleccionadas = function(dato){
			return dato=="";
		};
		
		$scope.initialize = function(dato){
		
			
			$http.get('/api/explotaciones/'+dato).success(function(data){
			
			uhcs = data.uhcs;
			
			
			for (i = 0; i < data.uhcs.length; i++){
				$scope.nombreuhc = uhcs[i].nombre;
				
				for (j = 0; j < uhcs[i].aplicaciones.length; j++){
						aplicaciones.push(uhcs[i].aplicaciones[j]);
				}
				
				for (j = 0; j < uhcs[i].parcelas.length; j++){
						parcelas.push(uhcs[i].parcelas[j]);
						analisis.push(uhcs[i].analisis[j]);
						//aplicaciones.push(uhcs[i].aplicaciones[j];
				}
				
			}
			
			$scope.parcelas = parcelas;
			$scope.analisis = analisis;
			$scope.aplicaciones = aplicaciones;

			});
			
			$scope.eliminar = function(dato,palabra){
				if(palabra == "parcela"){
					$http.delete('/api/parcelas/'+dato).
				success(function(data,status,headers,config){
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
				}else if(palabra == "aplicacion"){
					$http.delete('/api/aplicaciones/'+dato).
				success(function(data,status,headers,config){
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
				}
			};
			
			$scope.editar = function(parcela){
				$http.get('/api/parcelas/'+parcela).success(function(data){
					
				$scope.ParcelaUHC2 = data.idUHC;
				$scope.provinciaSeleccionada = data.provincia;
				$scope.municipioSeleccionado = data.municipio;
				$scope.nombreParcela2 = data.nombre;
				$scope.poligono2 = data.poligono;
				$scope.parcela2 = data.parcela;
				$scope.recinto2 = data.recinto;
				$scope.superficie2 = data.superficie_hectareas;
				$scope.sr2 = data.sr;
				$scope.descripcion2 = data.descripcion;

				});
				
			};
			
			$scope.guardarParcela = function(parcelaid,idExp,provid,munid){

			poli = $scope.poligono2;
			parce = $scope.parcela2;
			recin = $scope.recinto2;
			desc = $scope.descripcion2;
			
			
			while(String(poli).length < 3){
				poli = "0"+poli;
			}
			while(String(parce).length < 5){
				parce = "0"+parce;
			}
			while(String(recin).length < 5){
				recin = "0"+recin;
			}
			
			if($scope.descripcion == null){
				desc = "Sin descripción";
			}

			
			parcela = {idUHC: $scope.ParcelaUHC2,nombre: $scope.nombreParcela2,poligono: poli,parcela: parce,recinto: recin,
						superficie_hectareas: $scope.superficie2,sr: $scope.sr2,descripcion: desc,idExplotacion: idExp,
						provincia: provid, municipio: munid};
						
				
			$http.put('/api/parcelas/'+parcelaid,parcela).
			success(function(data,status,headers,config){
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);

			});
				
			};
			
			
			
			
			
			$scope.cerrar = function(parcela){
				$('#Eliminar'+parcela).modal('toggle');
			};

		};

		
		
		
	}]);
	
	administrador.controller('UsuarioExplotacion',['$http','$log','$scope',function($http,$log,$scope){
		
		var usuario = this;
		usuario.datos = [];

		$scope.initialize2 = function(dato){
		
			var codProvincia = null;
			var idmunicipio = null;
			$http.get('/api/tecnicos/'+dato).success(function(data){
			$scope.us = data;
			
			codProvincia = data.Provincia;
			idmunicipio = data.Municipio;
				$http.get('/api/provincias/'+codProvincia).success(function(data){
					$scope.Provincia = data.Provincia;
					for (i = 0; i < data.municipios.length; i++){
						if (data.municipios[i].id === idmunicipio){
							$scope.Municipio = data.municipios[i].Municipio;
						}
					}
				
				});
			});
			
		};
		
	}]);
	administrador.controller('AplicadorExplotacion',['$http','$log','$scope',function($http,$log,$scope){
		
		var aplicador = this;
		aplicador.datos = [];

		$scope.initialize3 = function(dato){
			var tipoAplicador = null;
			var idAplicador = null;

			$http.get('/api/aplicadores/'+dato).success(function(data){
				
				tipoAplicador = data.Aplicador;
				idAplicador = data.id;
				
				if (tipoAplicador === 1){
					$http.get('/api/empresasAplicadoras/'+dato).success(function(data2){
					$scope.NombreAplicador = data2.nombre;
					$scope.TipoAplicador = 'Empresa Aplicadora';
					});
				}else if (tipoAplicador === 2){
					$http.get('/api/personasFisicas/'+dato).success(function(data2){
					$scope.NombreAplicador = data2.nombre+" "+data2.apellido1+" "+data2.apellido2;
					$scope.TipoAplicador = 'Persona Física';
					});
				}
				
			});
			
		};
		
	}]);

	administrador.controller('AnalisisController',['$http','$log','$scope',function($http,$log,$scope){
		
		$scope.iniciaAnalisis = function(idAnalisis){
			$http.get('/api/analisis/'+idAnalisis).success(function(data){
				$scope.fechamuestra = new Date(data.fecha_muestra);
				$scope.AnalisisUHC = data.idUHC;
				$scope.tipom = data.tipo;
				$scope.tecnicom = data.tecnico;
				$scope.desm = data.descripcion;
				$scope.laboratorio = data.laboratorio;
				$scope.informeLaboratorio = data.numero_informe;
				$scope.fechaemision = new Date(data.fecha_emision);
				$scope.obsm = data.observaciones;
				$scope.accm = data.acciones;
				$scope.AnalisisTecnico = data.tecnico;
				$scope.horasAn = data.horas;
			});
		};
		
		
		$scope.modificarAnalisis = function(idAnalisis,idExp,idTec){
		
			
			fm = document.getElementById("fechamuestra").value;
			var day1 = $scope.fechamuestra.getDate();
			if(day1.toString().length < 2){
				day1 = "0"+day1.toString();
			}
			var day2 = $scope.fechaemision.getDate();
			if(day2.toString().length < 2){
				day2 = "0"+day2.toString();
			}
			
			obs = $scope.obsm;
			if (obs == ""){
				obs = "Sin observaciones";
			}
			acc = $scope.accm;
			if (acc == ""){
				acc = "Sin acciones";
			}
			
			desc = $scope.desm;
			if (desc == ""){
				desc = "Sin descripción";
			}
			
			hras = $scope.horasAn;
			if(hras == null || hras == ''){
				hras = '0';
			}
			
			analisis = {fecha_muestra: $scope.fechamuestra.toJSON().substring(0,8)+day1,idUHC: $scope.AnalisisUHC,tipo: $scope.tipom
			,tecnico: idTec,descripcion: desc,laboratorio: $scope.laboratorio,numero_informe: $scope.informeLaboratorio,
			fecha_emision: $scope.fechaemision.toJSON().substring(0,8)+day2,observaciones: obs,acciones: acc,idExplotacion : idExp,tecnico: $scope.AnalisisTecnico, horas: hras};
			
			
			$http.put('/api/analisis/'+idAnalisis,analisis).
			success(function(data,status,headers,config){
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);

			});
		};
		$scope.cancelar = function(){
			$scope.modifica = false;
		};
		
	}]);
	
	administrador.controller('TecnicoModifica',['$http','$log','$scope',function($http,$log,$scope){
		$scope.inicia = function(idTecnico){
			$http.get('/api/tecnicos/'+idTecnico).success(function(data){
				$scope.Nombre2 = data.Nombre;
				$scope.Apellido12 = data.Apellido1;
				$scope.Apellido22 = data.Apellido2;
				$scope.NIF2 = data.NIF;
				$scope.Domicilio2 = data.Domicilio;
				$scope.CP2 = data.CP;
				$scope.provinciaSeleccionada2 = data.Provincia;
				$scope.municipioSeleccionado2 = data.Municipio;
				$scope.email2 = data.email;
				$scope.Telefono12 = data.Telefono1;
				$scope.Telefono22 = data.Telefono2;
				$scope.Fax2 = data.Fax;
				$scope.ropo2 = data.ropo;
			});
		};
		$scope.modificaTecnico = function(idTec,idAdmin){
			
			tecnico = {Nombre: $scope.Nombre2,Apellido1: $scope.Apellido12, Apellido2: $scope.Apellido22,NIF: $scope.NIF2,
			Domicilio: $scope.Domicilio2, CP: $scope.CP2, Provincia: $scope.provinciaSeleccionada2, Municipio: $scope.municipioSeleccionado2,
			email: $scope.email2, Telefono1: $scope.Telefono12, Telefono2: $scope.Telefono22, Fax: $scope.Fax2, ropo: $scope.ropo2,
			idAdmin: idAdmin,activo: 'SI'};
			$http.put('/api/tecnicos/'+idTec,tecnico).
				success(function(data,status,headers,config){
					window.location = "/administrador/tecnicos/";
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
		};
		$scope.cerrar = function(dato,id){
			$(dato+""+id).modal('toggle');
		}
		$scope.eliminaTecnico = function(idTec,idAdmin){

			$http.delete('/api/usuarios/'+idTec).
				success(function(data2,status,headers,config){
					$http.get('/api/tecnicos/'+idTec).success(function(data){
						tecnico = {Nombre: data.Nombre,Apellido1: data.Apellido1, Apellido2: data.Apellido2,NIF: data.NIF,
						Domicilio: data.Domicilio, CP: data.CP, Provincia: data.Provincia, Municipio: data.Municipio,
						email: data.email, Telefono1: data.Telefono1, Telefono2: data.Telefono2, Fax: data.Fax, 
						ropo: data.ropo,idAdmin: idAdmin,activo: 'NO'};		
						$http.put('/api/tecnicos/'+idTec,tecnico).
						success(function(data3,status,headers,config){
							window.location = "/administrador/tecnicos/";
						}).
						error(function(data,status,headers,config){
							$log.log(data)
						});
					}).
					error(function(data,status,headers,config){
						$log.log(data)
					});
				}).
				error(function(data,status,headers,config){
					$log.log(data)
				});
		};
	}]);
	
administrador.controller('creaMuestra',['$http','$log','$scope',function($http,$log,$scope){
	var elementoId = "fenol";
	var arrayFenologia = [{letra: "A", texto: "Germinación | % plantas", tipo: "fenologia", valor: "0"}]
	arrayFenologia.push({letra: "B", texto: "Desarrollo de hojas (tallo/s principal/es)   | % plantas", tipo: "fenologia", valor: "0"})
	arrayFenologia.push({letra: "C", texto: "Formación brotes laterales | % plantas", tipo: "fenologia", valor: "0"})
	arrayFenologia.push({letra: "D", texto: "Órgano floral | % plantas", tipo: "fenologia", valor: "0"})
	arrayFenologia.push({letra: "E", texto: "Floración | % plantas", tipo: "fenologia", valor: "0"})
	arrayFenologia.push({letra: "F", texto: "Formación del fruto | % plantas", tipo: "fenologia", valor: "0"});
    arrayFenologia.push({letra: "G", texto: "Maduración del fruto/semilla | % plantas", tipo: "fenologia", valor: "0"});
    arrayFenologia.push({letra: "H", texto: "Cosecha | % plantas", tipo: "fenologia", valor: "0"});
    arrayFenologia.push({letra: "I", texto: "Senescencia | % plantas", tipo: "fenologia", valor: "0"});

	var arrayInsectos = [{letra: "I1", texto: "Nesidiocoris  |  % plantas con presencia", tipo: "insectos", valor: "0"}]
	arrayInsectos.push({letra: "I2", texto: "Swirskii  |  % de plantas con presencia", tipo: "insectos", valor: "0"})

	
	var arrayTrampas = [{letra: "P1", texto: "Mosca blanca | % plantas afectadas", tipo: "trampas", valor: "0"}]
	arrayTrampas.push({letra: "P2", texto: "Araña roja | Núm. de focos/1000m2", tipo: "trampas", valor: "0"})
	arrayTrampas.push({letra: "P3", texto: "Pulgón | Núm. de focos/1000m2 ", tipo: "trampas", valor: "0"})
	arrayTrampas.push({letra: "P4", texto: "Trips | % plantas afectadas ", tipo: "trampas", valor: "0"})
	arrayTrampas.push({letra: "P5", texto: "Orugas | % plantas afectadas ", tipo: "trampas", valor: "0"})
	arrayTrampas.push({letra: "P6", texto: "Nematodos | % plantas con daños ", tipo: "trampas", valor: "0"})

	
	var arrayEnfermedades = [{letra: "E1", texto: "Oidio | % plantas afectadas", tipo: "enfermedades", valor: "0"}]
	arrayEnfermedades.push({letra: "E2", texto: "Podredumbre gris (Botrytis cinerea) | % plantas afectadas", tipo: "enfermedades", valor: "0"})
	arrayEnfermedades.push({letra: "E3", texto: "Virus del mosaico amarillo (ZYMV) | % plantas afectadas", tipo: "enfermedades", valor: "0"})

	
	var valores = [0,1,2];
	$scope.valores = valores;
	$scope.arrayFenologia = arrayFenologia;
	$scope.arrayInsectos = arrayInsectos;
	$scope.arrayTrampas = arrayTrampas;
	$scope.arrayEnfermedades = arrayEnfermedades;
	$scope.muestraFenologia = true;
	var fen = 0;
	var trp = 0;
	var insc = 0;
	var enf = 0;
	
	$scope.iniciaMuestra = function(idMuestra){
		
		$http.get('/api/muestras/'+idMuestra).success(function(data){
			$scope.MuestraTecnico = data.tecnico;
			$scope.horasMu = data.horas;
			$scope.fecha_muestra = new Date(data.fecha_muestreo)
			$scope.MuestraUHC = data.idUHC;
			$scope.observaciones = data.observaciones;
			if(data.fenologia.length > 0){
				$log.log("fenologia")
				document.getElementById("A").selectedIndex = data.fenologia[0].muestra_a;
				document.getElementById("B").selectedIndex = data.fenologia[0].muestra_b;
				document.getElementById("C").selectedIndex = data.fenologia[0].muestra_c;
				document.getElementById("D").selectedIndex = data.fenologia[0].muestra_d;
				document.getElementById("E").selectedIndex = data.fenologia[0].muestra_e;
				document.getElementById("F").selectedIndex = data.fenologia[0].muestra_f;
				document.getElementById("G").selectedIndex = data.fenologia[0].muestra_g;
				document.getElementById("H").selectedIndex = data.fenologia[0].muestra_h;
				document.getElementById("I").selectedIndex = data.fenologia[0].muestra_i;

				fen = data.fenologia[0].id;
			}
			if(data.trampas.length > 0){
				$log.log("trampas")
				document.getElementById("P1").value = data.trampas[0].carpocapsa_p1;
				document.getElementById("P2").value = data.trampas[0].carpocapsa_p2;
				document.getElementById("P3").value = data.trampas[0].carpocapsa_p3;
				document.getElementById("P4").value = data.trampas[0].carpocapsa_p4;
				document.getElementById("P5").value = data.trampas[0].carpocapsa_p5;
				document.getElementById("P6").value = data.trampas[0].carpocapsa_p6;
				trp = data.trampas[0].id;
			}
			if(data.insectos.length > 0){
				$log.log("insectos")
				document.getElementById("1").value = data.insectos[0].coccinelidos;
				document.getElementById("2").value = data.insectos[0].neuropteros;
				insc = data.insectos[0].id;
			}
			if(data.enfermedades.length > 0){
				$log.log("enfermedades")
				document.getElementById("12").value = data.enfermedades[0].bacteriosis;
				document.getElementById("13").value = data.enfermedades[0].antracnosis;
				document.getElementById("14").value = data.enfermedades[0].antracnosis_2;
				enf = data.enfermedades[0].id;
			}
		});
	};
	
	
	$scope.modificaMuestra = function(expid,tecid,muestraId){

			f_m = document.getElementById("fecha_muestra").value;
			
			var obs = $scope.observaciones2;
			if( obs == null){
				obs = "Sin observaciones"
			}
			hras = $scope.horasMu;
			if(hras == null || hras == ''){
				hras = '0';
			}
			arrayFen = ["A","B","C","D","E","F","G","H","I"];
			arrayIns = ["1","2"];
			arrayTmp = ["P1","P2","P3","P4","P5","P6"];
			arrayEnf = ["12","13","14"]
			arrayId = arrayFen.concat(arrayTmp).concat(arrayIns).concat(arrayEnf);
			modificaMuestras = [];
			
			for(i = 0; i < arrayId.length; i++){
				if(arrayFen.indexOf(arrayId[i]) != -1){
					value = document.getElementById(arrayId[i]).options.selectedIndex;
					if (value > 0){
						if (modificaMuestras.indexOf("fenol") == -1){
							modificaMuestras.push("fenol");
						}
					}
				}else if (arrayTmp.indexOf(arrayId[i]) != -1){
					value = parseFloat(document.getElementById(arrayId[i]).value);
					if(value > 0){
						if (modificaMuestras.indexOf("tramp") == -1){
							modificaMuestras.push("tramp");
						}
					}		
				}else if (arrayIns.indexOf(arrayId[i]) != -1){
					value = parseInt($scope.arrayInsectos[i-14].valor);
					if(value > 0){
						if(modificaMuestras.indexOf("insect") == -1){
							modificaMuestras.push("insect");
						}
					}	
				}else if (arrayBrt.indexOf(arrayId[i]) != -1){
					value = parseInt(document.getElementById(arrayId[i]).value);
					if(value > 0){
						if(modificaMuestras.indexOf("brot") == -1){
							modificaMuestras.push("brot");
						}
					}	
				}else if (arrayZeuz.indexOf(arrayId[i]) != -1){
					value = parseInt(document.getElementById(arrayId[i]).value);
					if(value > 0){
						if(modificaMuestras.indexOf("zeuz") == -1){
							modificaMuestras.push("zeuz");
						}
					}	
				}else if (arrayEnf.indexOf(arrayId[i]) != -1){
					value = parseInt(document.getElementById(arrayId[i]).value);
					if(value > 0){
						if(modificaMuestras.indexOf("enfe") == -1){
							modificaMuestras.push("enfe");
						}
					}	
				}
				
			}

			muestra = {fecha_muestreo: f_m,idUHC: $scope.MuestraUHC,observaciones: obs,idExplotacion: expid,
			tecnico: tecid,horas: hras};
			$http.put('/api/muestras/'+muestraId,muestra).
			success(function(data,status,headers,config){
				var fallo = false;
				$log.log(modificaMuestras)
				for(i=0; i< modificaMuestras.length; i++){
					if(modificaMuestras[i] == "fenol"){
						val = [];
						for (j= 0; j<arrayFen.length; j++){
							val[j]=document.getElementById(arrayFen[j]).options.selectedIndex;	
						}
						fenologia = {idMuestra: data.id,muestra_a: val[0],muestra_b: val[1],muestra_c: val[2],
						muestra_d: val[3],muestra_e: val[4],muestra_f: val[5],muestra_a1: val[6],
						muestra_a2: val[7], muestra_a3: val[8],muestra_e1: val[9], muestra_e2: val[10],
						muestra_e3: val[11],muestra_f1: val[12]};
						if(fen == 0){
							$http.post('/api/muestras/fenologia/',fenologia).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								fallo = true && fallo;
							});
						}else{
							$http.put('/api/muestras/fenologia/'+fen,fenologia).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								fallo = true && fallo;
							});
						}
						
					}else if(modificaMuestras[i] == "tramp"){
						val = [];
						for (j= 0; j<arrayTmp.length; j++){
							val[j] =document.getElementById(arrayTmp[j]).value;	
							if(val[j] == ""){
								val[j] = 0;
							}
						}
					
						trampas = {idMuestra: data.id,carpocapsa: val[0]};
						if(trp == 0){
							$http.post('/api/muestras/trampas/',trampas).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								fallo = true && fallo;
							});

						}else{
							$http.put('/api/muestras/trampas/'+trp,trampas).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								fallo = true && fallo;
							});
						}
					
					
					}else if(modificaMuestras[i] == "insect"){
						val = [];
						for (j= 0; j<arrayIns.length; j++){
							val[j]=$scope.arrayInsectos[j].valor;
							if(val[j] == ""){
								val[j] = 0;
							}
							$log.log(val[j])
						}
						
						insectos = {idMuestra: data.id,coccinelidos: val[0],neuropteros: val[1],
						sirfidos: val[2],fitoseidos: val[3],scutellista: val[4],apanteles: val[5],
						aphytis: val[6]};
						if(insc == 0){
							$http.post('/api/muestras/insectos/',insectos).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								$log.log(data)
								fallo = true && fallo;
							});
						}else{
							$http.put('/api/muestras/insectos/'+insc,insectos).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								$log.log(data)
								fallo = true && fallo;
							});
						}
					}else if(modificaMuestras[i] == "enfe"){
						val = [];
						for (j= 0; j<arrayEnf.length; j++){
							val[j]=document.getElementById(arrayEnf[j]).value;	
							if(val[j] == ""){
								val[j] = 0;
							}
						}
					
						enfermedades = {idMuestra: data.id,bacteriosis: val[0],antracnosis: val[1]};
						if(enf == 0){
							$http.post('/api/muestras/enfermedades/',enfermedades).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								fallo = true && fallo;
							});	
						}else{
							$http.put('/api/muestras/enfermedades/'+enf,enfermedades).
							success(function(data,status,headers,config){
								fallo = false && fallo;
							}).error(function(data,status,headers,config){
								fallo = true && fallo;
							});		
						}							
					}
					
				}
				if(fen > 0){
					if(modificaMuestras.indexOf("fenol") == -1){
						$http.delete('/api/muestras/fenologia/'+fen);
					}
				}
				if(trp > 0){
					if(modificaMuestras.indexOf("tramp") == -1){
						$http.delete('/api/muestras/trampas/'+trp);
					}
				}
				if(insc > 0){
					if(modificaMuestras.indexOf("insect") == -1){
						$http.delete('/api/muestras/insectos/'+insc);
					}
				}
				if(enf > 0){
					if(modificaMuestras.indexOf("enfe") == -1){
						$http.delete('/api/muestras/enfermedades/'+enf);
					}
				}

					location.reload();
				
				
				
				
			}).
			error(function(data,status,headers,config){
				$log.log(data);
			});
		};
	$scope.cancelar = function(){
			$scope.modifica = false;
	};
	
	$scope.guardarMuestra = function(expid,tecid,tipoUs){
			
			f_m = document.getElementById("fecha_muestra").value;
			
			var obs = $scope.observaciones2;
			if( obs == null){
				obs = "Sin observaciones"
			}
			hras = $scope.horasMu;
			if(hras == null || hras == ''){
				hras = '0';
			}
			arrayFen = ["A","B","C","D","E","F","G","H","I"];
			arrayIns = ["I1","I2"];
			arrayTmp = ["P1","P2","P3","P4","P5","P6"];
			arrayEnf = ["E1","E2","E3"]
			arrayId = arrayFen.concat(arrayTmp).concat(arrayIns).concat(arrayEnf);
			modificaMuestras = [];
			for(i = 0; i < arrayId.length; i++){
				if(arrayFen.indexOf(arrayId[i]) != -1){
					value = document.getElementById(arrayId[i]).value;
					if (value > 0 && modificaMuestras.indexOf("fenol")){
	                    modificaMuestras.push("fenol");
					}
				}else if (arrayTmp.indexOf(arrayId[i]) != -1){
					
					value = document.getElementById(arrayId[i]).value;
					
					if(value > 0 && modificaMuestras.indexOf("tramp")){
						modificaMuestras.push("tramp")
					}		
				}else if (arrayIns.indexOf(arrayId[i]) != -1){
					
					value = document.getElementById(arrayId[i]).value;
					if(value > 0 && modificaMuestras.indexOf("insect")){
						modificaMuestras.push("insect")
					}	
				}else if (arrayEnf.indexOf(arrayId[i]) != -1){
					value = document.getElementById(arrayId[i]).value;
					if(value > 0 && modificaMuestras.indexOf("enfe")){
						modificaMuestras.push("enfe")
					}	
				}
			}
			
			muestra = {fecha_muestreo: f_m,idUHC: $scope.MuestraUHC,observaciones: obs,idExplotacion: expid,
			tecnico: tecid,horas: hras};
			$http.post('/api/muestras/',muestra).
			success(function(data,status,headers,config){
				var fallo = false;
				for(i=0; i< modificaMuestras.length; i++){
					if(modificaMuestras[i] == "fenol"){
						val = [];
						for (j= 0; j<arrayFen.length; j++){
							val[j]=document.getElementById(arrayFen[j]).value;	
						}
						fenologia = {idMuestra: data.id,muestra_a: val[0],muestra_b: val[1],muestra_c: val[2],
						muestra_d: val[3],muestra_e: val[4],muestra_f: val[5],muestra_g: val[6],
						muestra_h: val[7], muestra_i: val[8]};
						$http.post('/api/muestras/fenologia/',fenologia).
						success(function(data,status,headers,config){
							fallo = false && fallo;
						}).error(function(data,status,headers,config){
							fallo = true && fallo;
						});
						
					}else if(modificaMuestras[i] == "tramp"){
						val = [];
						for (j= 0; j<arrayTmp.length; j++){
							val[j]=document.getElementById(arrayTmp[j]).value;	
						}
						trampas = {idMuestra: data.id,carpocapsa_p1: val[0],carpocapsa_p2: val[0],carpocapsa_p3: val[0],carpocapsa_p4: val[0],carpocapsa_p5: val[0],carpocapsa_p6: val[0]};

						$http.post('/api/muestras/trampas/',trampas).
						success(function(data,status,headers,config){
							fallo = false && fallo;
						}).error(function(data,status,headers,config){
							fallo = true && fallo;
						});
					
					
					}else if(modificaMuestras[i] == "insect"){
						val = [];
						for (j= 0; j<arrayIns.length; j++){
							val[j]=$scope.arrayInsectos[j].valor;	
							$log.log(val[j])
						}
						
						insectos = {idMuestra: data.id,coccinelidos: val[0],neuropteros: val[1]};
						$log.log(insectos)
						$http.post('/api/muestras/insectos/',insectos).
						success(function(data,status,headers,config){
							fallo = false && fallo;
						}).error(function(data,status,headers,config){
							$log.log(data)
							fallo = true && fallo;
						});
					}else if(modificaMuestras[i] == "enfe"){
						val = [];
						for (j= 0; j<arrayEnf.length; j++){
							val[j]=document.getElementById(arrayEnf[j]).value;	
						}
					
						enfermedades = {idMuestra: data.id,bacteriosis: val[0],antracnosis: val[1],antracnosis_2: val[1]};
						$http.post('/api/muestras/enfermedades/',enfermedades).
						success(function(data,status,headers,config){
							fallo = false && fallo;
						}).error(function(data,status,headers,config){
							fallo = true && fallo;
						});			
					}
				}
				if (fallo == false){
					window.location = "/"+tipoUs+"/muestreo/"+data.id;
				}
				
				
			}).
			error(function(data,status,headers,config){
				$log.log(data);
			});
		};

	$scope.fenologia = function(){
		$scope.muestraInsectos = false;
		$scope.muestraTrampas = false;
		$scope.muestraFenologia = true;
		$scope.muestraEnfermedades = false;
		document.getElementById(elementoId).className ="list-group-item";
		document.getElementById("fenol").className ="list-group-item active";
		elementoId = "fenol";
		document.getElementById("tablaMuestras").tHead.innerHTML ="<tr><th>Fenología (Flor masculina/femenina)</th><th width='90'></th></tr>";
	};
	$scope.insectos = function(){
		$scope.muestraInsectos = true;
		$scope.muestraTrampas = false;
		$scope.muestraFenologia = false;
		$scope.muestraEnfermedades = false;
		document.getElementById(elementoId).className ="list-group-item";
		document.getElementById("insect").className ="list-group-item active";
		elementoId = "insect";
		document.getElementById("tablaMuestras").tHead.innerHTML ="<tr><th>Insectos auxiliares</th><th width='90'></th></tr>";
	};
	$scope.trampas = function(){
		$scope.muestraInsectos = false;
		$scope.muestraTrampas = true;
		$scope.muestraFenologia = false;
		$scope.muestraEnfermedades = false;
		document.getElementById(elementoId).className ="list-group-item";
		document.getElementById("tramp").className ="list-group-item active";
		elementoId = "tramp";
		document.getElementById("tablaMuestras").tHead.innerHTML ="<tr><th>Plagas</th><th width='90'></th></tr>";
	};
	$scope.enfermedades = function(){
		$scope.muestraInsectos = false;
		$scope.muestraTrampas = false;
		$scope.muestraFenologia = false;
		$scope.muestraEnfermedades = true;
		document.getElementById(elementoId).className ="list-group-item";
		document.getElementById("enferm").className ="list-group-item active";
		elementoId = "enferm";
		document.getElementById("tablaMuestras").tHead.innerHTML ="<tr><th>Enfermedades</th><th width='90'></th></tr>";
	};

	
	}]);
	
	administrador.controller('UsuarioController',['$http','$log','$scope',function($http,$log,$scope){
		
		$scope.guardaUsuario = function(idUsuario){
			usuario = document.getElementById("nuevoUsuario").value;
			
			$http.get('/api/usuarios/').success(function(data){
				fallo = false;
				for (i = 0; i < data.length; i++){
					if(data[i].username == usuario){
						fallo = true;
						break;
					}
				}
				if(fallo == true){
					error = document.getElementById("errorUsuario").innerHTML = "El usuario ya existe";
				}else{
					$http.get('/api/usuarios/'+idUsuario).success(function(data){
						$http.put('/api/usuarios/'+idUsuario,{username: usuario,first_name: data.first_name, last_name: data.last_name, is_staff: data.is_staff,
							is_active: data.is_active,perfil: data.perfil}).
							success(function(data,status,headers,config){
								window.location = "/";
						});
					});
				}
			});
			;
		};
	}]);
	
	administrador.controller('Dashboard',['$http','$log','$scope',function($http,$log,$scope){
		$scope.exp = true;
		$scope.tec = false;
		$scope.maq = false;
		//$scope.explotacionSeleccionada = 1;
		$scope.muestraMuestreos = true;
		$scope.muestraNoAnyo = true;
		$scope.SexoSelect = "Masculino";
		var arrayFertilizacion = [];
		var arrayRiego = [];
		var arrayCultivo = [];
		var arrayPoda = [];
		var arrayRecoleccion = [];
		var arrayAplicacion = [];
		var arrayAnalisis = [];
		var arrayAnyos = [];
		var arrayFenologia = [];
		var arrayInsectos = [];
		var arrayTrampas = [];
		var arrayEnfermedades = [];
		$scope.cultivos = [];
		$scope.Inputoperaciones = [];
		$scope.uhcs = [];
		$scope.tipoOperaciones = [];
		$scope.parcelas = [];
		$scope.cultivoID = [];
		$scope.inputOperacionId = [];
		
		this.tab = 1;
		
		this.selectTab = function(setTab){
			this.tab = setTab;
		};
		this.isSelected = function(checkTab){
			return this.tab === checkTab;
		};
	
		$scope.datosArray = function(id){
			$http.get('/api/explotaciones/'+id).success(function(data){
				$scope.UHCSelect = data.uhcs[0].id;
				$scope.uhcs = data.uhcs;
				//$scope.explotacionSeleccionada = data.id;
				
				for(i = 0; i<data.uhcs.length; i++){			
						operaciones = data.uhcs[i].operaciones;
						aplicaciones = data.uhcs[i].aplicaciones;
						analisis = data.uhcs[i].analisis;
						muestreo = data.uhcs[i].muestreo;
						
						uhc = data.uhcs[i];
						for(j = 0; j<operaciones.length; j++){
							tecnico = operaciones[j].TecnicoNombre+" "+operaciones[j].TecnicoApellido1+" "+operaciones[j].TecnicoApellido2;
							horas = operaciones[j].horas;
							if(operaciones[j].tipoOp == "FERTILIZACION-ENMIENDA"){	
								horas = operaciones[j].horas;
								anyo = operaciones[j].fecha_operacion.substring(0,4);
								for(k = 0; k< arrayFertilizacion.length; k++){
									if (anyo == arrayFertilizacion[k].anyo){
										if (uhc.id == arrayFertilizacion[k].iduhc){

										arrayFertilizacion[k].list[0] = Math.round((arrayFertilizacion[k].list[0]+parseFloat(operaciones[j].fertilizacion[0].nitrogeno)) * 100) / 100;
										arrayFertilizacion[k].list[1] = Math.round((arrayFertilizacion[k].list[1]+parseFloat(operaciones[j].fertilizacion[0].fosforo))*100)/100;
										arrayFertilizacion[k].list[2] = Math.round((arrayFertilizacion[k].list[2]+parseFloat(operaciones[j].fertilizacion[0].potasio))*100)/100;
										arrayFertilizacion[k].list[3] = Math.round((arrayFertilizacion[k].list[3]+parseFloat(operaciones[j].fertilizacion[0].abono_aplicado))*100)/100;
										break;
										}else{
											var list2 = {id:"",anyo:"",anyo2:"",uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
											list2.anyo = anyo;
											list2.anyo2 = anyo;
											list2.id = operaciones[j].id;
											list2.list.push(parseFloat(operaciones[j].fertilizacion[0].nitrogeno));
											list2.list.push(parseFloat(operaciones[j].fertilizacion[0].fosforo))
											list2.list.push(parseFloat(operaciones[j].fertilizacion[0].potasio))
											list2.list.push(parseFloat(operaciones[j].fertilizacion[0].abono_aplicado))
											arrayFertilizacion.push(list2);
											break;
										}
									}
								}
								if (k == arrayFertilizacion.length){
									var list2 = {id:"",anyo:"",anyo2:"",uhc_nombre:data.uhcs[i].nombre,iduhc:data.uhcs[i].id,tecnico:tecnico,horas:horas,list:[]}
									list2.anyo = anyo;
									list2.anyo2 = anyo;
									list2.id = operaciones[j].id;
									list2.list.push(parseFloat(operaciones[j].fertilizacion[0].nitrogeno));
									list2.list.push(parseFloat(operaciones[j].fertilizacion[0].fosforo))
									list2.list.push(parseFloat(operaciones[j].fertilizacion[0].potasio))
									list2.list.push(parseFloat(operaciones[j].fertilizacion[0].abono_aplicado))
									arrayFertilizacion.push(list2);
								}	
							}
							if(operaciones[j].tipoOp == "RIEGO"){
								anyo = operaciones[j].fecha_operacion.substring(0,4);
								for(k = 0; k< arrayRiego.length; k++){
									if (anyo == arrayRiego[k].anyo){
										if (uhc.id == arrayRiego[k].iduhc){
											arrayRiego[k].list[0] = Math.round((arrayRiego[k].list[0]+parseFloat(operaciones[j].riego[0].cantidad_agua)) * 100) / 100;
											arrayRiego[k].list[1] += 1;		
											break;
										}else{
											var list2 = {id:"",anyo:"",anyo2:"",uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
											list2.anyo = anyo;
											list2.anyo2 = anyo;
											list2.id = operaciones[j].id;
											list2.list.push(parseFloat(operaciones[j].riego[0].cantidad_agua));
											list2.list.push(1);
											arrayRiego.push(list2);
											break;
										}
									}
								}
								if (k == arrayRiego.length){
									var list2 = {id:"",anyo:"",anyo2:"",uhc_nombre:data.uhcs[i].nombre,iduhc:data.uhcs[i].id,tecnico:tecnico,horas:horas,list:[]}
									list2.anyo = anyo;
									list2.anyo2 = anyo;
									list2.id = operaciones[j].id;
									list2.list.push(parseFloat(operaciones[j].riego[0].cantidad_agua));
									list2.list.push(1);
									arrayRiego.push(list2);
								}	
								
							}
							if(operaciones[j].tipoOp == "LABORES DE SUELO"){
									fecha = new Date(operaciones[j].fecha_operacion);
									var list2 = {id:"",anyo:"",anyo2:fecha,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
									list2.id = operaciones[j].id;
									mes = String(parseInt(fecha.getMonth())+1);
									if(mes.length < 2){
										mes = "0"+mes;
									}
									dia = String(fecha.getDate());
									if(dia.length < 2){
										dia = "0"+dia;
									}
									list2.anyo = dia+"/"+mes+"/"+fecha.getFullYear();
									apero = operaciones[j].labores[0].apero;
									if(apero == "DISCOS" || apero == "VERTEDERA"){
										apero = "ARADO "+apero;
									}
									
									list2.list.push(apero);
									list2.list.push(operaciones[j].labores[0].superficie_labrada);
									arrayCultivo.push(list2);	
							}
							if(operaciones[j].tipoOp == "PODA"){
									fecha = new Date(operaciones[j].fecha_operacion);
									var list2 = {id:"",anyo:"",anyo2:fecha,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
									list2.id = operaciones[j].id;
									mes = String(parseInt(fecha.getMonth())+1);
									if(mes.length < 2){
										mes = "0"+mes;
									}
									dia = String(fecha.getDate());
									if(dia.length < 2){
										dia = "0"+dia;
									}
									list2.anyo = dia+"/"+mes+"/"+fecha.getFullYear();
									tipo = operaciones[j].poda[0].TipoPoda;
									if(tipo == "PRODUCCION"){ 
										tipo = "Poda de producción";
									}else if(tipo == "FORMACION"){
										tipo = "Poda de formación";
									}else if(tipo == "REJUVENECIMIENTO"){
										tipo = "Poda de rejuvenecimiento";
									}else if(tipo == "ACLAREO"){
										tipo = "Aclareo";
									}
									
									list2.list.push(tipo);
									list2.list.push(operaciones[j].poda[0].Duracion)
									arrayPoda.push(list2);
							}
							if(operaciones[j].tipoOp == "RECOLECCION"){
									fecha = new Date(operaciones[j].fecha_operacion);
									var list2 = {id:"",anyo:"",anyo2:fecha,anyo3:"",uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
									list2.id = operaciones[j].id;
									mes = String(parseInt(fecha.getMonth())+1);
									if(mes.length < 2){
										mes = "0"+mes;
									}
									dia = String(fecha.getDate());
									if(dia.length < 2){
										dia = "0"+dia;
									}
									list2.anyo = dia+"/"+mes+"/"+fecha.getFullYear();
									list2.anyo3 = String(fecha.getFullYear());
									if(arrayAnyos.indexOf(list2.anyo3) == -1){
										arrayAnyos.push(list2.anyo3);
									}
									metodo= operaciones[j].recoleccion[0].metodo_recol;
									list2.list.push(operaciones[j].recoleccion[0].superficie_recogida);
									list2.list.push(operaciones[j].recoleccion[0].total_recogido);
									list2.list.push(metodo);
									arrayRecoleccion.push(list2);	
							}
						}
						for(j = 0; j<aplicaciones.length; j++){
							tecnico = aplicaciones[j].TecnicoNombre+" "+aplicaciones[j].TecnicoApellido1+" "+aplicaciones[j].TecnicoApellido2;
							horas = aplicaciones[j].horas;
							fecha = new Date(aplicaciones[j].fecha_Aplicacion);
							var list2 = {id:"",anyo:"",anyo2:fecha,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
							list2.id = aplicaciones[j].id;
							mes = String(parseInt(fecha.getMonth())+1);
							if(mes.length < 2){
								mes = "0"+mes;
							}
							dia = String(fecha.getDate());
							if(dia.length < 2){
								dia = "0"+dia;
							}
							list2.anyo = dia+"/"+mes+"/"+fecha.getFullYear();
							list2.list.push(aplicaciones[j].superficie_tratada);
							list2.list.push(aplicaciones[j].gasto_caldo);
							arrayAplicacion.push(list2);	
						}
						for(j = 0; j<analisis.length; j++){
							tecnico = analisis[j].TecnicoNombre+" "+analisis[j].TecnicoApellido1+" "+analisis[j].TecnicoApellido2;
							horas = analisis[j].horas;
							fecha = new Date(analisis[j].fecha_muestra);
							var list2 = {id:"",anyo:"",anyo2:fecha,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,list:[]}
							list2.id = analisis[j].id;
							mes = String(parseInt(fecha.getMonth())+1);
							if(mes.length < 2){
								mes = "0"+mes;
							}
							dia = String(fecha.getDate());
							if(dia.length < 2){
								dia = "0"+dia;
							}
							list2.anyo = dia+"/"+mes+"/"+fecha.getFullYear();
							list2.list.push(analisis[j].tipo);
							arrayAnalisis.push(list2);	
						}
						for(j = 0; j<muestreo.length; j++){
							
							tecnico = muestreo[j].TecnicoNombre+" "+muestreo[j].TecnicoApellido1+" "+muestreo[j].TecnicoApellido2;
							horas = muestreo[j].horas;
							fechaFen = new Date(muestreo[j].fecha_muestreo);
							
							mes = String(parseInt(fechaFen.getMonth())+1);
							if(mes.length < 2){
								mes = "0"+mes;
							}
							dia = String(fechaFen.getDate());
							if(dia.length < 2){
								dia = "0"+dia;
							}
							
							fenologia = muestreo[j].fenologia;
							insectos = muestreo[j].insectos;
							trampas = muestreo[j].trampas;
							enfermedades = muestreo[j].enfermedades;
							if (fenologia.length > 0){
								fenologia = fenologia[0]
								var list2 = {id:"",anyo:"",anyo2:fechaFen,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,sexo:'Masculino',a:"",
								b: "",c:"",d:"",e:"",f:"",a1:"",a2:"",a3:"",e1:"",e2:"",e3:"",f1:""}
								list2.id = muestreo[j].id;
								list2.anyo = dia+"/"+mes+"/"+fechaFen.getFullYear();
								
								list2.a = fenologia.muestra_a;
								list2.b = fenologia.muestra_b;
								list2.c = fenologia.muestra_c;
								list2.d = fenologia.muestra_d;
								list2.e = fenologia.muestra_e;
								list2.f = fenologia.muestra_f;
								list2.a1 = fenologia.muestra_a1;
								list2.a2 = fenologia.muestra_a2;
								list2.a3 = fenologia.muestra_a3;
								list2.e1 = fenologia.muestra_e1;
								list2.e2 = fenologia.muestra_e2;
								list2.e3 = fenologia.muestra_e3;
								list2.f1 = fenologia.muestra_f1;
								arrayFenologia.push(list2);
							}
							if (insectos.length > 0){
								insectos = insectos[0]
								var list2 = {id:"",anyo:"",anyo2:fechaFen,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,sexo:'Masculino',a:"",
								b: "",c:"",d:"",e:"",f:"",a1:"",a2:"",a3:"",e1:"",e2:"",e3:"",f1:""}
								list2.id = muestreo[j].id;
								list2.anyo = dia+"/"+mes+"/"+fechaFen.getFullYear();
								
								list2.a = insectos.coccinelidos;
								list2.b = insectos.neuropteros;
								list2.c = insectos.sirfidos;
								list2.d = insectos.fitoseidos;
								list2.e = insectos.scutellista;
								list2.f = insectos.apanteles;
								list2.a1 = insectos.aphytis;
								

								arrayInsectos.push(list2);
							}if (trampas.length > 0){
								trampas = trampas[0]
								var list2 = {id:"",anyo:"",anyo2:fechaFen,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,sexo:'Masculino',a:"",
								b: "",c:"",d:"",e:"",f:"",a1:"",a2:"",a3:"",e1:"",e2:"",e3:"",f1:""}
								list2.id = muestreo[j].id;
								list2.anyo = dia+"/"+mes+"/"+fechaFen.getFullYear();
								
								list2.a = trampas.carpocapsa;
								arrayTrampas.push(list2);
							}if (enfermedades.length > 0){
								enfermedades = enfermedades[0]
								var list2 = {id:"",anyo:"",anyo2:fechaFen,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,sexo:'Masculino',a:"",
								b: "",c:"",d:"",e:"",f:"",a1:"",a2:"",a3:"",e1:"",e2:"",e3:"",f1:""}
								list2.id = muestreo[j].id;
								list2.anyo = dia+"/"+mes+"/"+fechaFen.getFullYear();
								
								list2.a2 = enfermedades.bacteriosis;
								list2.a3 = enfermedades.antracnosis;
								arrayEnfermedades.push(list2);
							}}}});}
		
		$scope.inicia = function(id){
			if(id != null || id > 0 || id != ''){
				$scope.datosArray(id);
				$scope.datosExplotacion = arrayFertilizacion;
			}
			$http.get('/api/cultivo/').success(function(data){
				$scope.cultivos = data;
			});
			$http.get('/api/parcelas/').success(function(dataPar){
				$scope.parcelas = dataPar;
			});
			$http.get('/api/municipios').success(function(dataMun){	
					$scope.municipios = dataMun;
			});
			$http.get('/api/provincias').success(function(dataPro){	
					$scope.provincias = dataPro;
			});
			$http.get('/api/cultivo').success(function(datacult){	
					$scope.cultivos = datacult;
			});
		};
		$scope.iniciaConfig = function(){
			
			
			$http.get('/api/uhcs/').success(function(dataUhcs){
				$scope.uhcs = dataUhcs;
			});
			$http.get('/api/Tiposoperacion/').success(function(dataTipo){
				$scope.tipoOperaciones = dataTipo;
			});
			$http.get('/api/Inputoperacion/').success(function(dataInput){
				$scope.Inputoperaciones = dataInput;
			});
			$http.get('/api/parcelas/').success(function(dataPar){
				$scope.parcelas = dataPar;
			});
			$http.get('/api/municipios').success(function(dataMun){	
					$scope.municipios = dataMun;
			});
			$http.get('/api/provincias').success(function(dataPro){	
					$scope.provincias = dataPro;
			});
		};


		$scope.fertilizacion = function(panel){
		
			$scope.muestraOperaciones = false;
			$scope.muestraMuestreos = true;
			$scope.muestraNoAnyo = true;
			$scope.muestraCultivo = false;
			$scope.muestraCantidad = false;
			$scope.muestraAnyo = false;
			$scope.muestraOperacion = true;
			$scope.muestraSexo = false;
		    $scope.Muestras = false;
		
			panel.selectTab(1);
			document.getElementById("tipoOperacion").innerHTML = "Fertilización";
			document.getElementById("iconoPanel").className="fa fa-leaf fa-fw";
			document.getElementById("panelMio").className="panel panel-warning";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Temporada</th><th>UHC</th><th>UF Nitrógeno</th><th>UF Fósforo</th><th>UF Potasio</th><th>Abono aplicado(Kg)</th></tr>";
			$scope.datosExplotacion = arrayFertilizacion;
			
			
		};
		$scope.riego = function(panel){
		
			$scope.muestraOperaciones = false;
			$scope.muestraMuestreos = true;
			$scope.muestraNoAnyo = true;
			$scope.muestraCultivo = false;
			$scope.muestraCantidad = false;
			$scope.muestraAnyo = false;
			$scope.muestraOperacion = true;
			$scope.muestraSexo = false;
		    $scope.Muestras = false;
		
			panel.selectTab(2);
			document.getElementById("tipoOperacion").innerHTML = "Riego";
			document.getElementById("iconoPanel").className="fa fa-tint fa-fw";
			document.getElementById("panelMio").className="panel panel-info";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Temporada</th><th>UHC</th><th>Cantidad agua (m<sup>3</sup>/ha)</th><th>Nº de riegos</th></tr>";
			$scope.datosExplotacion = arrayRiego;
			
		};
		$scope.cultivo = function(panel){
		
			$scope.muestraOperaciones = false;
			$scope.muestraMuestreos = true;
			$scope.muestraNoAnyo = true;
			$scope.muestraCultivo = true;
			$scope.muestraCantidad = false;
			$scope.muestraAnyo = false;
			$scope.muestraOperacion = true;
			$scope.muestraSexo = false;
		    $scope.Muestras = false;

			panel.selectTab(3);
			document.getElementById("tipoOperacion").innerHTML = "Operaciones de Cultivo";
			document.getElementById("iconoPanel").className="fa fa-gear fa-fw";
			document.getElementById("panelMio").className="panel panel-warning";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Fecha operación</th><th>UHC</th><th>Apero empleado</th><th>Superficie labrada (ha)</th><th>Técnico</th><th>Horas dedicadas</th></tr>";
			$scope.datosExplotacion = arrayCultivo;	
			
		};
		$scope.poda = function(panel){
		
			$scope.muestraOperaciones = false;
			$scope.muestraMuestreos = true;
			$scope.muestraNoAnyo = true;
			$scope.muestraCultivo = true;
			$scope.muestraCantidad = false;
			$scope.muestraAnyo = false;
			$scope.muestraOperacion = true;
			$scope.muestraSexo = false;
		    $scope.Muestras = false;

			panel.selectTab(4);
			document.getElementById("tipoOperacion").innerHTML = "Poda";
			document.getElementById("iconoPanel").className="fa fa-cut fa-fw";
			document.getElementById("panelMio").className="panel panel-success";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Fecha operación</th><th>UHC</th><th>Tipo de poda</th><th>Duración (días)</th><th>Técnico</th><th>Horas dedicadas</th></tr>";
			$scope.datosExplotacion = arrayPoda;	
			
		};
		$scope.recoleccion = function(panel){
		
			$scope.muestraOperaciones = false;
			$scope.muestraMuestreos = true;
			$scope.muestraNoAnyo = false;
			$scope.muestraCultivo = true;
			$scope.muestraCantidad = false;
			$scope.muestraAnyo = true;
			$scope.muestraOperacion = true;
			$scope.muestraSexo = false;
		    $scope.Muestras = false;
			$scope.anyos = arrayAnyos;
			panel.selectTab(5);
			document.getElementById("tipoOperacion").innerHTML = "Recolección";
			document.getElementById("iconoPanel").className="fa fa-pagelines fa-fw";
			document.getElementById("panelMio").className="panel panel-success";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Fecha operación</th><th>UHC</th><th>Superficie recogida (ha)</th><th>Total recogido (kg)</th><th>Método</th><th>Técnico</th><th>Horas dedicadas</th></tr>";
			$scope.datosExplotacion = arrayRecoleccion;
		};
		
		$scope.cambiaAnyo = function(anyo){	
			cantidad = 0;
			$scope.muestraCantidad = true;
			
			for (i = 0; i < arrayRecoleccion.length; i++){
				if(arrayRecoleccion[i].anyo3 == anyo && arrayRecoleccion[i].iduhc == $scope.UHCSelect)
				{   
					$log.log(arrayRecoleccion[i].list[1]);
					cantidad += parseFloat(arrayRecoleccion[i].list[1]);
				}
			}
			
			
			$scope.totalRecogido = Math.round(cantidad * 10000) / 10000;
		};
		
		$scope.selectOperaciones = function(panel){
			$scope.muestraOperaciones = false;
			$scope.muestraCultivo = false;
			$scope.muestraMuestreos = true;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = true;
			$scope.muestraCantidad = false;
			$scope.muestraAplicacion = false;
			$scope.muestraAnalisis = false;
			$scope.muestraOperacion = true;
			$scope.muestraSexo = false;
			$scope.Muestras = false;
			panel.selectTab(1);
			document.getElementById("tipoOperacion").innerHTML = "Fertilización";
			document.getElementById("iconoPanel").className="fa fa-leaf fa-fw";
			document.getElementById("panelMio").className="panel panel-warning";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Temporada</th><th>UHC</th><th>UF Nitrógeno</th><th>UF Fósforo</th><th>UF Potasio</th><th>Abono aplicado(Kg)</th></tr>";
			$scope.datosExplotacion = arrayFertilizacion;
		};
		$scope.selectAnalisis = function(){
			$scope.muestraOperaciones = true;
			$scope.muestraCultivo = true;
			$scope.muestraMuestreos = true;
			$scope.muestraAplicacion = false;
			$scope.muestraAnalisis = true;
			$scope.muestraOperacion = false;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = true;
			$scope.muestraCantidad = false;
			$scope.muestraSexo = false;
			$scope.Muestras = false;
			document.getElementById("tipoOperacion").innerHTML = "Análisis";
			document.getElementById("iconoPanel").className="fa fa-flask fa-fw";
			document.getElementById("panelMio").className="panel panel-info";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Fecha análisis</th><th>UHC</th><th>Tipo</th><th>Técnico</th><th>Horas dedicadas</th></tr>";
			$scope.datosExplotacion = arrayAnalisis;
		};
		$scope.selectAplicaciones = function(){
			$scope.muestraOperaciones = true;
			$scope.muestraMuestreos = true;
			$scope.muestraCultivo = true;
			$scope.muestraAplicacion = true;
			$scope.muestraAnalisis = false;
			$scope.muestraOperacion = false;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = true;
			$scope.muestraCantidad = false;
			$scope.muestraSexo = false;
			$scope.Muestras = false;
			document.getElementById("tipoOperacion").innerHTML = "Aplicación";
			document.getElementById("iconoPanel").className="fa fa-fire-extinguisher fa-fw";
			document.getElementById("panelMio").className="panel panel-success";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th>Fecha aplicación</th><th>UHC</th><th>Superficie recogida (ha)</th><th>Gasto (l/ha)</th><th>Técnico</th><th>Horas dedicadas</th></tr>";
			$scope.datosExplotacion = arrayAplicacion;
		};
		$scope.selectMuestras = function(panel){
			$scope.muestraOperaciones = true;
			$scope.muestraMuestreos = false;
			$scope.Muestras = true;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = false;
			$scope.muestraSexo = true;
			$scope.inse = false;
			$scope.tram = false;
			$scope.brot = false;
			$scope.zeuz = false;
			$scope.enfe = false;
			$scope.SexoSelect = "Masculino";
			panel.selectTab(6);
			document.getElementById("tipoOperacion").innerHTML = "Fenología";
			document.getElementById("iconoPanel").className="fa fa-tree fa-fw";
			document.getElementById("panelMio").className="panel panel-success";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th data-toggle='tooltip' title='Receso'>R</th><th data-toggle='tooltip' title='Inicio de Elongación'>I.E.</th><th data-toggle='tooltip' title='Inicio Apertura Amentos'>I.A.M.</th><th data-toggle='tooltip' title='Inicio Emisión de Polen'>I.E.P.</th><th data-toggle='tooltip' title='Plena Emisión de Polen'>P.E.P.</th><th data-toggle='tooltip' title='Término Emisión de Polen'>T.E.P.</th></tr>";
			$scope.datosExplotacion = arrayFenologia;
		};
		
		$scope.insectos = function(panel){
			$scope.muestraOperaciones = true;
			$scope.muestraMuestreos = false;
			$scope.Muestras = true;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = false;
			$scope.muestraSexo = false;
			$scope.inse = true;
			$scope.tram = false;
			$scope.brot = false;
			$scope.zeuz = false;
			$scope.enfe = false;
			$scope.SexoSelect = "Masculino";
			panel.selectTab(7);
			document.getElementById("tipoOperacion").innerHTML = "Insectos Auxiliares";
			document.getElementById("iconoPanel").className="fa fa-bug fa-fw";
			document.getElementById("panelMio").className="panel panel-info";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th>Coccinélidos</th><th>Neurópteros</th><th>Sirfidos</th><th>Fitoseidos</th><th>Scutellista</th><th>Apanteles</th><th>Aphytis</th></tr>";
			$scope.datosExplotacion = arrayInsectos;
		};
		$scope.trampas = function(panel){
			$scope.muestraOperaciones = true;
			$scope.muestraMuestreos = false;
			$scope.Muestras = true;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = false;
			$scope.muestraSexo = false;
			$scope.SexoSelect = "";
			$scope.inse = false;
			$scope.tram = true;
			$scope.brot = false;
			$scope.zeuz = false;
			$scope.enfe = false;
			panel.selectTab(8);
			document.getElementById("tipoOperacion").innerHTML = "Plagas";
			document.getElementById("iconoPanel").className="fa fa-asterisk fa-fw";
			document.getElementById("panelMio").className="panel panel-warning";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th>Carpocapsa</th></tr>";
			$scope.datosExplotacion = arrayTrampas;
		};
		$scope.enfermedades = function(panel){
			$scope.muestraOperaciones = true;
			$scope.muestraMuestreos = false;
			$scope.Muestras = true;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = false;
			$scope.muestraSexo = false;
			$scope.SexoSelect = "";
			$scope.inse = false;
			$scope.tram = false;
			$scope.brot = false;
			$scope.zeuz = false;
			$scope.enfe = true;
			panel.selectTab(11);
			document.getElementById("tipoOperacion").innerHTML = "Enfermedades";
			document.getElementById("iconoPanel").className="fa fa-warning fa-fw";
			document.getElementById("panelMio").className="panel panel-danger";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th>Bacteriosis</th><th>Antracnosis</th></tr>";
			$scope.datosExplotacion = arrayEnfermedades;
		};


		
		$scope.cambiaSexo = function(sexo){	
		
			if(sexo == "Femenino"){
				document.getElementById("tableDashboard").tHead.innerHTML =
				"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th data-toggle='tooltip' title='Receso'>R</th><th data-toggle='tooltip' title='Inicio de Brotación'>I.B.</th><th data-toggle='tooltip' title='Hojas en Expansión'>H.E.</th><th data-toggle='tooltip' title='Flor Pistilada Pre-receptiva'>F.P.Pre</th><th data-toggle='tooltip' title='Flor Pistilada Receptiva'>F.P.Rec.</th><th data-toggle='tooltip' title='Flor Pistilada Post-receptiva'>F.P.Post.</th><th data-toggle='tooltip' title='Fruto Pequeño'>F.P.</th></tr>";
			}else{
				document.getElementById("tableDashboard").tHead.innerHTML =
				"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th data-toggle='tooltip' title='Receso'>R</th><th data-toggle='tooltip' title='Inicio de Elongación'>I.E.</th><th data-toggle='tooltip' title='Inicio Apertura Amentos'>I.A.M.</th><th data-toggle='tooltip' title='Inicio Emisión de Polen'>I.E.P.</th><th data-toggle='tooltip' title='Plena Emisión de Polen'>P.E.P.</th><th data-toggle='tooltip' title='Término Emisión de Polen'>T.E.P.</th></tr>";
			}
		
		};
		
		$scope.redirecciona = function(tipo){
			explotacionSeleccionada = document.getElementById("selectExplotacion").value;
			if(explotacionSeleccionada == 0){
					alert("Debe seleccionar una explotación")
			}else{
					if(tipo == 'admin'){
				window.location = "/administrador/explotacion/"+explotacionSeleccionada;
			}else{
				//window.location = "/tecnico/explotacion/"+explotacionSeleccionada;
				window.location = "/tecnicoExplotacion/"+explotacionSeleccionada;
			}
			}
			
		};
		
		$scope.guardarInput = function(){
			tipoSeleccionado = document.getElementById("tipoSeleccionado").value;
			nombreInput = document.getElementById("nombreInput").value;
			cantidad = document.getElementById("cantidad").value;
			unidad = document.getElementById("unidad").value;
			coefEmision = document.getElementById("coefEmision").value;
			unidadCoef = document.getElementById("unidadCoef").value;
			coefAsignacion = document.getElementById("coefAsignacion").value;
			costeUnitario = document.getElementById("costeUnitario").value;
			$http.get('/api/Tiposoperacion/'+tipoSeleccionado).
			success(function(data1){
				
				Input = {input : nombreInput,idTipoOp : tipoSeleccionado,cantidad : cantidad,unidad : unidad,coefEmision : coefEmision,unidadCoef : unidadCoef,coefAsignacion : coefAsignacion,costeUnitario : costeUnitario,nombreTipo: data1.nombre};

				$http.post('/api/Inputoperacion/',Input).
				success(function(data,status,headers,config){
					input = $scope.Inputoperaciones;
					input.push(data);
					$scope.Inputoperaciones = input;
					location.replace('/configuracion/');

				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
		
			}).
			error(function(data1,status,headers,config){
				$log.log("Error");
			});
			
		};
		$scope.cargarInput = function(id){
			$http.get('/api/Inputoperacion/'+id).
			success(function(data){

				$scope.inputOperacionId = data;
				
		
			}).
			error(function(data,status,headers,config){
				$log.log("Error");
			});
		};
		$scope.cargarUHC = function(id){
			$http.get('/api/uhcs/'+id).
			success(function(data){

				$scope.nombreUHC = data.nombre;
				
		
			}).
			error(function(data,status,headers,config){
				$log.log("Error");
			});
		};
		$scope.editUHC = function(id){
			$http.get('/api/uhcs/'+id).
						success(function(dataUHC){

							dataUHC.nombre = document.getElementById("nombreUHCEdit").value;

							
							$http.put('/api/uhcs/'+id,dataUHC).
							success(function(data,status,headers,config){
								location.reload();
							}).
							error(function(data,status,headers,config){
								$log.log(data);
							});	
						}).
						error(function(dataUHC,status,headers,config){
							$log.log("Error");
						});
		};
		$scope.editInput = function(id){
			
			input = document.getElementById("nombreInputEdit").value;
			idTipoOp = document.getElementById("tipoSeleccionadoEdit").value;
			coefEmision = document.getElementById("coefEmisionEdit").value;
			cantidad = document.getElementById("cantidadEdit").value;
			coefAsignacion = document.getElementById("coefAsignacionEdit").value;
			costeUnitario = document.getElementById("costeUnitarioEdit").value;
			unidad = document.getElementById("unidadEdit").value;
			unidadCoef = document.getElementById("unidadCoefEdit").value;
			
			location.replace('/EditaInput/'+id+'*'+input+'*'+idTipoOp+'*'+coefEmision+'*'+cantidad+'*'+coefAsignacion+'*'+costeUnitario+'*'+unidad+'*'+unidadCoef)

		};
		$scope.borrarInput = function(id){
			if (confirm("¿Desea eliminar este Input?") == true) {
				$http.delete('/api/Inputoperacion/'+id).
					success(function(data,status,headers,config){
						var index = 0;
						input = $scope.Inputoperaciones;
						for (i=0; i<input.length; i++){
							if(input[i].id == id){
								index = i;
								
							}
						}
						input.splice(index,1);
						$scope.Inputoperaciones = input;
						location.replace('/configuracion/');
					}).
					error(function(data,status,headers,config){
						$log.log(data);
						$log.log(status);
						$log.log(headers);
						$log.log(config);
					});
			}
				
		};
		
		$scope.cargarCultivo = function(id){
			$http.get('/api/cultivo/'+id).
			success(function(data){

				$scope.cultivoID = data;
				$scope.fechaFin = new Date(data.fecha_fin);
				$scope.fechaInicio = new Date(data.fecha_inicio);
				
		
			}).
			error(function(data,status,headers,config){
				$log.log("Error");
			});
		};
		$scope.borrarCultivo = function(id){
			$http.delete('/api/cultivo/'+id).
				success(function(data,status,headers,config){
					
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
		};
		$scope.guardarParcela = function(idexp){
			
			provinciaSeleccionada = document.getElementById("provinciaSeleccionada").value;
			municipioSeleccionado = document.getElementById("municipioSeleccionado").value;
			poli = document.getElementById("poligono").value;
			parce = document.getElementById("parcela").value;
			recin = document.getElementById("recinto").value;
			desc = document.getElementById("descripcion").value;
			sr = document.getElementById("sr").value;
			nombreParcela = document.getElementById("nombreParcela").value;
			cultivo = document.getElementById("cultivo").value;
			superficie = document.getElementById("superficie").value;

			while(String(poli).length < 3){
				poli = "0"+poli;
			}
			while(String(parce).length < 5){
				parce = "0"+parce;
			}
			while(String(recin).length < 5){
				recin = "0"+recin;
			}
			
			if($scope.descripcion == null){
				desc = "Sin descripción";
			}
			/*parcela = {nombre: $scope.nombreParcela,provincia: $scope.provinciaSeleccionada,municipio: $scope.municipioSeleccionado, poligono: poli,parcela: parce ,recinto: recin,superficie_hectareas: $scope.superficie, sr: $scope.sr, idUHC: $scope.ParcelaUHC,descripcion: desc,idExplotacion: idexp,idcultivo: $scope.ParcelaCultivo};*/
			
			location.replace('/crearParcela/'+ nombreParcela+'/'+provinciaSeleccionada+'/'+municipioSeleccionado+'/'+poli+'/'+parce+'/'+recin+'/'+superficie+'/'+sr+'/'+desc+'/'+idexp+'/'+cultivo)
			/*$http.post('/api/parcelas/',parcela).
			success(function(data,status,headers,config){
				alert("entra");
				parcelas = $scope.parcelas;
				parcelas.push(data);
				$scope.parcelas = parcelas;
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});*/
			
		};
		$scope.guardarCultivo = function(){
			fechaFin = document.getElementById("fechaFin").value;
			fechaIni = document.getElementById("fini").value;
			nombre = document.getElementById("nombreCultivo").value;
			descripcion = document.getElementById("descripcionCultivo").value;
			localizacion = document.getElementById("localizacionCultivo").value;


			cultivo = {nombre : nombre,fecha_inicio : fechaIni,fecha_fin : fechaFin,descripcion : descripcion,localizacion : localizacion};

			$http.post('/api/cultivo/',cultivo).
			success(function(data,status,headers,config){
				cultivo = $scope.cultivos;
				cultivo.push(data);
				$scope.cultivos = cultivo;
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
		};
		$scope.guardarUHC = function(idExp,idCultivo){

			nombre = document.getElementById("nombreUHC").value;
			uhc = {nombre : nombre,idExplotacion : idExp};
			$http.post('/api/uhcs/',uhc).
			success(function(data,status,headers,config){
		
				location.replace('/tecnicoCultivo/'+idCultivo)

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
			});
		};
		$scope.modificarCultivo = function(id){
			$http.get('/api/cultivo/'+id).
						success(function(data){


							data.nombre = document.getElementById("nombreCultivoEdit").value;
							data.fecha_inicio =document.getElementById("finiEdit").value;
							data.fecha_fin = document.getElementById("fechaFinEdit").value;
							data.descripcion = document.getElementById("descripcionCultivoEdit").value;
							data.localizacion =document.getElementById("localizacionCultivoEdit").value;
								
							
							$http.put('/api/cultivo/'+id,data).
							success(function(data,status,headers,config){
								location.reload();
							}).
							error(function(data,status,headers,config){
								$log.log(data);
							});	
						}).
						error(function(data,status,headers,config){
							$log.log("Error");
						});
		};
		$scope.cambiaCultivo = function(){
			idCultivo = document.getElementById("selectCultivo").value;
			location.replace('/tecnicoCultivo/'+idCultivo)
		}
		
		$scope.cambiaExplotacion = function(){
			
			alert("entra");
			/*arrayFertilizacion = [];
			arrayRiego = [];
			arrayCultivo = [];
			arrayPoda = [];
			arrayRecoleccion = [];
			arrayAnyos = [];
			arrayAplicacion = [];
		    arrayAnalisis = [];
			arrayFenologia = [];
		    arrayInsectos = [];
		    arrayTrampas = [];
		    arrayBrotes = [];
		    arrayZeuzera = [];
		    arrayEnfermedades = [];
			
			$scope.datosArray($scope.explotacionSeleccionada);
							
				if(document.getElementById("tipoOperacion").innerHTML == "Fertilización"){
					$scope.datosExplotacion = arrayFertilizacion;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Riego"){
					$scope.datosExplotacion = arrayRiego;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Operaciones de Cultivo"){
					$scope.datosExplotacion = arrayCultivo;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Poda"){
					$scope.datosExplotacion = arrayPoda;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Recolección"){
					$scope.datosExplotacion = arrayRecoleccion;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Aplicación"){
					$scope.datosExplotacion = arrayAplicacion;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Análisis"){
					$scope.datosExplotacion = arrayAnalisis;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Fenología"){
					$scope.datosExplotacion = arrayFenologia;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Insectos Auxiliares"){
					$scope.datosExplotacion = arrayInsectos;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Trampas"){
					$scope.datosExplotacion = arrayTrampas;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Muestreo Brotes / Frutos"){
					$scope.datosExplotacion = arrayBrotes;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Zeuzera"){
					$scope.datosExplotacion = arrayZeuzera;
				}else if(document.getElementById("tipoOperacion").innerHTML == "Enfermedades"){
					$scope.datosExplotacion = arrayEnfermedades;
				}*/
		};
		
	}]);
	
	
	
	
	
})();


