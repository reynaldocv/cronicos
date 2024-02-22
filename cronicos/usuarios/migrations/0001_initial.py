# Generated by Django 4.2.10 on 2024-02-20 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('aCIE', models.CharField(default='xx.xx', max_length=5, primary_key=True, serialize=False)),
                ('aEnfermedad', models.CharField(max_length=100)),
                ('aShort', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.CharField(default='xxxxx', max_length=5, primary_key=True, serialize=False)),
                ('especialidad', models.CharField(default='xxxxx', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.CharField(default='0', max_length=1, primary_key=True, serialize=False)),
                ('hospital', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('dni', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('sexo', models.BooleanField(default=True)),
                ('nacimiento', models.DateField(default='1950-01-01')),
                ('historia', models.CharField(default='', max_length=100)),
                ('direccion', models.CharField(default='', max_length=50)),
                ('celular', models.CharField(default='', max_length=15)),
                ('muerto', models.BooleanField(default=False)),
                ('fechaMuerto', models.DateField(default='2030-01-01')),
                ('observacionMuerto', models.CharField(default='Muerto sin ninguna observación.', max_length=100)),
                ('dm', models.BooleanField(default=False)),
                ('fechaDm', models.DateField(default='1980-01-01')),
                ('hta', models.BooleanField(default=False)),
                ('fechaHta', models.DateField(default='1980-01-01')),
                ('status', models.CharField(default=True, max_length=1)),
                ('observacion', models.CharField(default='', max_length=100)),
                ('hospital', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='usuarios.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Referencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default='1900-01-01')),
                ('atendido', models.BooleanField(default=False)),
                ('observacion', models.CharField(default='', max_length=50)),
                ('dni', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente')),
                ('especialidad', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='usuarios.especialidad')),
            ],
        ),
        migrations.CreateModel(
            name='Pie',
            fields=[
                ('id', models.CharField(default='xxxxxxxx-xx-xxxx', max_length=20, primary_key=True, serialize=False)),
                ('data', models.DateField(default='1900-01-01')),
                ('conLesion', models.BooleanField(default=False)),
                ('observacion', models.CharField(default='', max_length=50)),
                ('dni', models.ForeignKey(default='00000000', on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Mosare',
            fields=[
                ('id', models.CharField(default='xxxxxxxx-xxxx', max_length=14, primary_key=True, serialize=False)),
                ('data', models.DateField(default='1900-01-01')),
                ('creatinina', models.CharField(default='', max_length=6)),
                ('tfge', models.CharField(default='', max_length=6)),
                ('albuminuria', models.CharField(default='', max_length=6)),
                ('creatinuria', models.CharField(default='', max_length=6)),
                ('tasa', models.CharField(default='', max_length=20)),
                ('tasaDescripcion', models.CharField(default='', max_length=20)),
                ('dni', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Ekg',
            fields=[
                ('id', models.CharField(default='xxxxxxxx-xx-xxxx', max_length=20, primary_key=True, serialize=False)),
                ('data', models.DateField(default='1900-01-01')),
                ('esNormal', models.BooleanField(default=True)),
                ('observacion', models.CharField(default='', max_length=50)),
                ('dni', models.ForeignKey(default='00000000', on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Atencion',
            fields=[
                ('id', models.CharField(default='xxxxxxxx-xx-xxxx', max_length=20, primary_key=True, serialize=False)),
                ('dotacion', models.CharField(max_length=1)),
                ('fecha', models.DateField(default='1900-01-01')),
                ('acto', models.CharField(max_length=10)),
                ('presion', models.CharField(max_length=10)),
                ('hemotest', models.CharField(default='', max_length=10)),
                ('peso', models.CharField(default='', max_length=10)),
                ('talla', models.CharField(default='', max_length=10)),
                ('perimetro', models.CharField(default='', max_length=5)),
                ('morisky', models.CharField(default='0', max_length=1)),
                ('imc', models.CharField(max_length=20)),
                ('imcDescripcion', models.CharField(default='', max_length=30)),
                ('edad', models.CharField(default='0', max_length=5)),
                ('observacion', models.CharField(default='', max_length=100)),
                ('dni', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='usuarios.paciente')),
            ],
        ),
    ]