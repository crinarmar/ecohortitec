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
	
	administrador.controller('Dashboard',['$http','$log','$scope',function($http,$log,$scope){
		$scope.exp = true;
		$scope.tec = false;
		$scope.maq = false;
		$scope.explotacionSeleccionada = 1;
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
		var arrayBrotes = [];
		var arrayZeuzera = [];
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
				$scope.explotacionSeleccionada = data.id;
				
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
							brotes = muestreo[j].brotes;
							zeuzera = muestreo[j].zeuzera;
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
							}if (brotes.length > 0){
								brotes = brotes[0]
								var list2 = {id:"",anyo:"",anyo2:fechaFen,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,sexo:'Masculino',a:"",
								b: "",c:"",d:"",e:"",f:"",a1:"",a2:"",a3:"",e1:"",e2:"",e3:"",f1:""}
								list2.id = muestreo[j].id;
								list2.anyo = dia+"/"+mes+"/"+fechaFen.getFullYear();
								
								list2.a = brotes.carpocapsa;
								list2.b = brotes.acaros;
								list2.c = brotes.pulgones;
								arrayBrotes.push(list2);
							}if (zeuzera.length > 0){
								zeuzera = zeuzera[0]
								var list2 = {id:"",anyo:"",anyo2:fechaFen,uhc_nombre:uhc.nombre,iduhc:uhc.id,tecnico:tecnico,horas:horas,sexo:'Masculino',a:"",
								b: "",c:"",d:"",e:"",f:"",a1:"",a2:"",a3:"",e1:"",e2:"",e3:"",f1:""}
								list2.id = muestreo[j].id;
								list2.anyo = dia+"/"+mes+"/"+fechaFen.getFullYear();
								
								list2.d = zeuzera.zeuzera;
								arrayZeuzera.push(list2);
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
			document.getElementById("tipoOperacion").innerHTML = "Trampas";
			document.getElementById("iconoPanel").className="fa fa-asterisk fa-fw";
			document.getElementById("panelMio").className="panel panel-warning";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th>Carpocapsa</th></tr>";
			$scope.datosExplotacion = arrayTrampas;
		};
		$scope.brotes = function(panel){
			$scope.muestraOperaciones = true;
			$scope.muestraMuestreos = false;
			$scope.Muestras = true;
			$scope.muestraAnyo = false;
			$scope.muestraNoAnyo = false;
			$scope.muestraSexo = false;
			$scope.SexoSelect = "";
			$scope.inse = false;
			$scope.tram = false;
			$scope.brot = true;
			$scope.zeuz = false;
			$scope.enfe = false;
			panel.selectTab(9);
			document.getElementById("tipoOperacion").innerHTML = "Muestreo Brotes / Frutos";
			document.getElementById("iconoPanel").className="fa fa-leaf fa-fw";
			document.getElementById("panelMio").className="panel panel-warning";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th>Carpocapsa</th><th>Ácaros</th><th>Pulgones</th></tr>";
			$scope.datosExplotacion = arrayBrotes;
		};
		$scope.zeuzera = function(panel){
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
			$scope.zeuz = true;
			$scope.enfe = false;
			panel.selectTab(10);
			document.getElementById("tipoOperacion").innerHTML = "Zeuzera";
			document.getElementById("iconoPanel").className="fa fa-asterisk fa-fw";
			document.getElementById("panelMio").className="panel panel-info";
			document.getElementById("tableDashboard").tHead.innerHTML =
			"<tr><th width='60'>Fecha</th><th width='20'>UHC</th><th>Técnico</th><th>Barrinador de la madera(Zeuzera pyrina)</th></tr>";
			$scope.datosExplotacion = arrayZeuzera;
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
			if(tipo == 'admin'){
				window.location = "/administrador/explotacion/"+$scope.explotacionSeleccionada;
			}else{
				window.location = "/tecnico/explotacion/"+$scope.explotacionSeleccionada;
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


			Input = {input : nombreInput,idTipoOp : tipoSeleccionado,cantidad : cantidad,unidad : unidad,coefEmision : coefEmision,unidadCoef : unidadCoef,coefAsignacion : coefAsignacion,costeUnitario : costeUnitario};

			$http.post('/api/Inputoperacion/',Input).
			success(function(data,status,headers,config){
				input = $scope.Inputoperaciones;
				input.push(data);
				$scope.Inputoperaciones = input;
				location.reload();

			}).
			error(function(data,status,headers,config){
				$log.log(data);
				$log.log(status);
				$log.log(headers);
				$log.log(config);
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
			$http.get('/api/Inputoperacion/'+id).
						success(function(data){

							data.input = document.getElementById("nombreInputEdit").value;
							data.idTipoOp = document.getElementById("tipoSeleccionadoEdit").value;
							data.coefEmision = document.getElementById("coefEmisionEdit").value;
							data.cantidad = document.getElementById("cantidadEdit").value;
							data.coefAsignacion = document.getElementById("coefAsignacionEdit").value;
							data.costeUnitario = document.getElementById("costeUnitarioEdit").value;
							data.unidad = document.getElementById("unidadEdit").value;
							data.unidadCoef = document.getElementById("unidadCoefEdit").value;
							
							$http.put('/api/Inputoperacion/'+id,data).
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
		$scope.borrarInput = function(id){
			$http.delete('/api/Inputoperacion/'+id).
				success(function(data,status,headers,config){
					var index = 0;
					input = $scope.Inputoperaciones;
					for (i=0; i<input.length; i++){
						if(input[i].id == id){
							index = i;
							alert(index)
						}
					}
					input.splice(index,1);
					$scope.Inputoperaciones = input;
					location.reload();
				}).
				error(function(data,status,headers,config){
					$log.log(data);
					$log.log(status);
					$log.log(headers);
					$log.log(config);
				});
				
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
			arrayFertilizacion = [];
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
				}
		};
		
	}]);
	
	
	
	
	
})();


