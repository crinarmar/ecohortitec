# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre', models.CharField(max_length=200)),
                ('Apellido1', models.CharField(max_length=200)),
                ('Apellido2', models.CharField(max_length=200)),
                ('NIF', models.CharField(max_length=9)),
                ('Domicilio', models.CharField(max_length=250)),
                ('CP', models.CharField(max_length=5)),
                ('email', models.EmailField(max_length=75)),
                ('Telefono1', models.CharField(max_length=9)),
                ('Telefono2', models.CharField(max_length=9, blank=True)),
                ('Fax', models.CharField(max_length=9, blank=True)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('ropo', models.CharField(max_length=12, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_muestra', models.DateField()),
                ('tipo', models.CharField(default=b'SUELO', max_length=16, choices=[(b'SUELO', b'Suelo'), (b'AGUA', b'Agua'), (b'FOLIAR', b'Foliar'), (b'MULTIRRESIDUOS', b'Multirresiduos')])),
                ('horas', models.DecimalField(max_digits=5, decimal_places=2)),
                ('descripcion', models.TextField(blank=True)),
                ('laboratorio', models.CharField(max_length=200)),
                ('numero_informe', models.IntegerField()),
                ('fecha_emision', models.DateField()),
                ('observaciones', models.TextField(blank=True)),
                ('acciones', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Aplicacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_Aplicacion', models.DateField()),
                ('numero_orden_tratamiento', models.CharField(max_length=200)),
                ('fecha_Orden_tratamiento', models.DateField()),
                ('gasto_caldo', models.DecimalField(max_digits=11, decimal_places=2)),
                ('superficie_tratada', models.DecimalField(max_digits=5, decimal_places=2)),
                ('porcentaje', models.IntegerField()),
                ('distribucion_ap', models.CharField(max_length=200)),
                ('condiciones_aplicacion', models.CharField(max_length=200)),
                ('presion_tratamiento', models.DecimalField(max_digits=11, decimal_places=2)),
                ('velocidad_tratamiento', models.DecimalField(max_digits=11, decimal_places=2)),
                ('horas', models.DecimalField(max_digits=5, decimal_places=2)),
                ('hora_aplicacion', models.TimeField()),
                ('observaciones', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Aplicador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('apellido1', models.CharField(max_length=200, blank=True)),
                ('apellido2', models.CharField(max_length=200, blank=True)),
                ('dni', models.CharField(max_length=9)),
                ('fecha_validez', models.DateField()),
                ('fecha_expedicion', models.DateField()),
                ('razon_social', models.CharField(max_length=200)),
                ('Aplicador', models.CharField(default=2, max_length=1, choices=[(1, b'Empresa Aplicadora'), (2, b'Persona Fisica')])),
                ('Telefono', models.CharField(max_length=9, blank=True)),
                ('Fax', models.CharField(max_length=9, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DatosClimaticos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('EstacionClimatica', models.CharField(max_length=200)),
                ('Temperatura', models.DecimalField(max_digits=5, decimal_places=1)),
                ('TempMax', models.DecimalField(max_digits=5, decimal_places=1)),
                ('TempMin', models.DecimalField(max_digits=5, decimal_places=1)),
                ('TempMed', models.DecimalField(max_digits=5, decimal_places=1)),
                ('Humedad', models.IntegerField()),
                ('HumMax', models.IntegerField()),
                ('HumMin', models.IntegerField()),
                ('HumMed', models.IntegerField()),
                ('Precipitacion', models.DecimalField(max_digits=5, decimal_places=3)),
                ('fecha', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'documents/%Y/%m/%d')),
                ('filename', models.CharField(max_length=100)),
                ('idAnalisis', models.ForeignKey(related_name='documento', to='citagro.Analisis')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Explotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Razon_Social', models.CharField(max_length=200)),
                ('cif_nif', models.CharField(max_length=9)),
                ('Domicilio', models.CharField(max_length=250)),
                ('CP', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaquinaExplotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idExplotacion', models.ForeignKey(related_name='maquinarias', to='citagro.Explotacion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maquinaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero_roma', models.CharField(max_length=200)),
                ('fecha_adquisicion', models.DateField()),
                ('fecha_revision', models.DateField()),
                ('TipoMaquina', models.CharField(max_length=200)),
                ('MarcaModelo', models.CharField(max_length=200)),
                ('idAdmin', models.ForeignKey(related_name='maquinaria', to='citagro.Administrador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Muestreo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('detalles', models.TextField()),
                ('horas', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Multiresiduos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r_p_ma', models.CharField(max_length=200)),
                ('r_p_valor', models.DecimalField(max_digits=3, decimal_places=2)),
                ('r_p_umbral', models.DecimalField(max_digits=3, decimal_places=2)),
                ('analisis', models.ForeignKey(to='citagro.Analisis')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CodMunicipio', models.CharField(max_length=20)),
                ('CodCatastral', models.CharField(max_length=20)),
                ('Municipio', models.CharField(max_length=80)),
            ],
            options={
                'ordering': ['idProvincia', 'CodMunicipio'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='op_fertilizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_fert', models.CharField(default=b'COBERTERA', max_length=100, choices=[(b'COBERTERA', b'Abonado cobertera'), (b'FONDO', b'Abonado de fondo'), (b'ENMIENDAS', b'Enmiendas')])),
                ('modo_aplicacion', models.CharField(max_length=200, blank=True)),
                ('superficie_aplicada', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('n_orden_aplicacion', models.CharField(max_length=200, blank=True)),
                ('producto_comercial', models.CharField(max_length=200, blank=True)),
                ('composicion', models.CharField(max_length=200, blank=True)),
                ('riqueza_n', models.IntegerField()),
                ('riqueza_p', models.IntegerField()),
                ('riqueza_k', models.IntegerField()),
                ('riqueza_Ca', models.IntegerField(blank=True)),
                ('riqueza_Mg', models.IntegerField(blank=True)),
                ('riqueza_S', models.IntegerField(blank=True)),
                ('riqueza_otros', models.IntegerField(blank=True)),
                ('dosis', models.DecimalField(max_digits=10, decimal_places=2)),
                ('unidad_dosis', models.CharField(max_length=200)),
                ('nitrogeno', models.DecimalField(max_digits=5, decimal_places=2)),
                ('fosforo', models.DecimalField(max_digits=5, decimal_places=2)),
                ('potasio', models.DecimalField(max_digits=5, decimal_places=2)),
                ('empresa_distribuidora', models.CharField(max_length=200, blank=True)),
                ('justificacion', models.CharField(max_length=200, blank=True)),
                ('densidad', models.DecimalField(max_digits=10, decimal_places=2)),
                ('abono_aplicado', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='op_labores',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('apero', models.CharField(default=b'CULTIVADOR', max_length=100, choices=[(b'CULTIVADOR', b'Cultivador'), (b'DISCOS', b'Arado discos'), (b'VERTEDERA', b'Arado vertedera'), (b'DESBROZADOR', b'Desbrozador')])),
                ('distribucion', models.CharField(max_length=200, blank=True)),
                ('superficie_labrada', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('profundidad_labor', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('justificacion', models.CharField(max_length=200, blank=True)),
                ('empresa', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='op_poda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('TipoPoda', models.CharField(default=b'FORMACION', max_length=100, choices=[(b'FORMACION', b'Poda de formaci\xc3\xb3n'), (b'PRODUCCION', b'Poda de producci\xc3\xb3n'), (b'REJUVENECIMIENTO', b'Poda de rejuvenecimiento'), (b'ACLAREO', b'Aclareo')])),
                ('Duracion', models.IntegerField(blank=True)),
                ('Herramienta', models.CharField(max_length=200, blank=True)),
                ('Producto', models.CharField(max_length=200, blank=True)),
                ('Fecha_eliminacion', models.DateField()),
                ('Modo_eliminacion', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='op_recoleccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_lote', models.CharField(max_length=200)),
                ('metodo_recol', models.CharField(default=b'MANUAL', max_length=100, choices=[(b'MANUAL', b'Manual'), (b'MECANIZADO', b'Mecanizado')])),
                ('superficie_recogida', models.DecimalField(max_digits=10, decimal_places=2)),
                ('total_recogido', models.DecimalField(max_digits=10, decimal_places=2, blank=True)),
                ('rendimiento', models.DecimalField(max_digits=10, decimal_places=2, blank=True)),
                ('destrio', models.DecimalField(max_digits=5, decimal_places=2, blank=True)),
                ('id_lote_destino', models.CharField(max_length=200, blank=True)),
                ('tratamiento_cosecha', models.CharField(max_length=200, blank=True)),
                ('receptor_produccion', models.CharField(max_length=200, blank=True)),
                ('n_albaran', models.CharField(max_length=200, blank=True)),
                ('precio_agricultor', models.DecimalField(max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='op_riego',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sistema_riego', models.CharField(default=b'GOTEROS', max_length=100, choices=[(b'GOTEROS', b'Localizado: Goteros'), (b'ASPERSION', b'Aspersi\xc3\xb3n')])),
                ('procedencia_agua', models.CharField(max_length=200, blank=True)),
                ('calidad_agua', models.CharField(max_length=200, blank=True)),
                ('cantidad_agua', models.DecimalField(max_digits=10, decimal_places=2)),
                ('uf_nitro', models.CharField(max_length=200, blank=True)),
                ('justificacion_riego', models.CharField(max_length=200, blank=True)),
                ('clave', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('horas', models.DecimalField(max_digits=5, decimal_places=2)),
                ('fecha_operacion', models.DateField()),
                ('observaciones', models.TextField(blank=True)),
                ('tipoOp', models.CharField(default=b'PODA', max_length=100, choices=[(b'PODA', b'Poda'), (b'LABORES DE SUELO', b'Labores de suelo'), (b'FERTILIZACION-ENMIENDA', b'Fertiliz.-Enmienda.Correct'), (b'RIEGO', b'Riego'), (b'RECOLECCION', b'Recolecci\xc3\xb3n')])),
                ('idExplotacion', models.ForeignKey(related_name='operacionesExplotacion', to='citagro.Explotacion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('poligono', models.CharField(max_length=3)),
                ('parcela', models.CharField(max_length=5)),
                ('recinto', models.CharField(max_length=5)),
                ('superficie_hectareas', models.DecimalField(max_digits=11, decimal_places=6)),
                ('sr', models.CharField(default=b'SECANO', max_length=10, choices=[(b'SECANO', b'Secano'), (b'REGADIO', b'Regadio')])),
                ('descripcion', models.TextField()),
                ('idExplotacion', models.ForeignKey(related_name='parcelasExplotacion', to='citagro.Explotacion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('TipoUsuario', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Usuario Administrador'), (b'T', b'Usuario Tecnico')])),
                ('user', models.ForeignKey(related_name='perfil', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Producto_aplicado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('dosis', models.DecimalField(max_digits=11, decimal_places=2)),
                ('materia_activa', models.CharField(max_length=200)),
                ('riqueza', models.IntegerField()),
                ('objeto', models.CharField(max_length=200)),
                ('justific', models.CharField(max_length=200)),
                ('casa_comercial', models.CharField(max_length=200, blank=True)),
                ('n_registro', models.CharField(max_length=10)),
                ('empresa_distribuidora', models.CharField(max_length=200, blank=True)),
                ('observaciones', models.TextField(blank=True)),
                ('aplicacion', models.ForeignKey(related_name='productos', to='citagro.Aplicacion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CodProvincia', models.CharField(max_length=20)),
                ('Provincia', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['CodProvincia'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Nombre', models.CharField(max_length=200)),
                ('Apellido1', models.CharField(max_length=200)),
                ('Apellido2', models.CharField(max_length=200)),
                ('NIF', models.CharField(max_length=9)),
                ('Domicilio', models.CharField(max_length=250)),
                ('CP', models.CharField(max_length=5)),
                ('email', models.EmailField(max_length=75)),
                ('Telefono1', models.CharField(max_length=9)),
                ('Telefono2', models.CharField(max_length=9, blank=True)),
                ('Fax', models.CharField(max_length=9, blank=True)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('ropo', models.CharField(max_length=12, blank=True)),
                ('Municipio', models.ForeignKey(to='citagro.Municipio')),
                ('Provincia', models.ForeignKey(to='citagro.Provincia')),
                ('idAdmin', models.ForeignKey(related_name='tecnicos', to='citagro.Administrador')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UHC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('idExplotacion', models.ForeignKey(related_name='uhcs', to='citagro.Explotacion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuarioExplotacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idExplotacion', models.ForeignKey(related_name='usuarios', to='citagro.Explotacion')),
                ('idUsuario', models.ForeignKey(related_name='usuariosExplotaciones', to='citagro.Tecnico')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='parcela',
            name='idUHC',
            field=models.ForeignKey(related_name='parcelas', to='citagro.UHC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parcela',
            name='municipio',
            field=models.ForeignKey(to='citagro.Municipio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='parcela',
            name='provincia',
            field=models.ForeignKey(to='citagro.Provincia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operacion',
            name='idUHC',
            field=models.ForeignKey(related_name='operaciones', to='citagro.UHC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operacion',
            name='tecnico',
            field=models.ForeignKey(related_name='TecnicoOperacion', to='citagro.Tecnico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='op_riego',
            name='idOperacion',
            field=models.ForeignKey(related_name='riego', to='citagro.Operacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='op_recoleccion',
            name='idOperacion',
            field=models.ForeignKey(related_name='recoleccion', to='citagro.Operacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='op_poda',
            name='idOperacion',
            field=models.ForeignKey(related_name='poda', to='citagro.Operacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='op_labores',
            name='idOperacion',
            field=models.ForeignKey(related_name='labores', to='citagro.Operacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='op_fertilizacion',
            name='idOperacion',
            field=models.ForeignKey(related_name='fertilizacion', to='citagro.Operacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='municipio',
            name='idProvincia',
            field=models.ForeignKey(related_name='municipios', to='citagro.Provincia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='muestreo',
            name='idUHC',
            field=models.ForeignKey(to='citagro.UHC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='muestreo',
            name='tecnico',
            field=models.ForeignKey(related_name='TecnicoMuestra', to='citagro.Tecnico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maquinaexplotacion',
            name='idMaquina',
            field=models.ForeignKey(related_name='explotaciones', to='citagro.Maquinaria'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='explotacion',
            name='Localidad',
            field=models.ForeignKey(to='citagro.Municipio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='explotacion',
            name='Provincia',
            field=models.ForeignKey(to='citagro.Provincia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='explotacion',
            name='idAdmin',
            field=models.ForeignKey(related_name='explotaciones', to='citagro.Administrador'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datosclimaticos',
            name='idExplotacion',
            field=models.ForeignKey(related_name='datosClimaticos', to='citagro.Explotacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aplicador',
            name='idExplotacion',
            field=models.ForeignKey(related_name='aplicadores', to='citagro.Explotacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='aplicador',
            field=models.ForeignKey(to='citagro.Aplicador'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='idUHC',
            field=models.ForeignKey(related_name='aplicaciones', to='citagro.UHC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='maquinaria',
            field=models.ForeignKey(to='citagro.Maquinaria'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aplicacion',
            name='tecnico',
            field=models.ForeignKey(related_name='TecnicoAplicacion', to='citagro.Tecnico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analisis',
            name='idExplotacion',
            field=models.ForeignKey(related_name='analisisExplotacion', to='citagro.Explotacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analisis',
            name='idUHC',
            field=models.ForeignKey(related_name='analisis', to='citagro.UHC'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='analisis',
            name='tecnico',
            field=models.ForeignKey(related_name='TecnicoAnalisis', to='citagro.Tecnico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrador',
            name='Municipio',
            field=models.ForeignKey(to='citagro.Municipio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='administrador',
            name='Provincia',
            field=models.ForeignKey(to='citagro.Provincia'),
            preserve_default=True,
        ),
    ]
