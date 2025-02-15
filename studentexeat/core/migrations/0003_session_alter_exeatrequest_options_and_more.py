# Generated by Django 5.1.4 on 2024-12-16 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_exeatrequest_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(choices=[('2024/2025', '2024/2025'), ('2025/2026', '2025/2026'), ('2026/2027', '2026/2027'), ('2027/2028', '2027/2028'), ('2028/2029', '2028/2029'), ('2029/2030', '2029/2030'), ('2030/2031', '2030/2031'), ('2031/2032', '2031/2032'), ('2032/2033', '2032/2033'), ('2033/2034', '2033/2034'), ('2034/2035', '2034/2035'), ('2035/2036', '2035/2036'), ('2036/2037', '2036/2037'), ('2037/2038', '2037/2038'), ('2038/2039', '2038/2039'), ('2039/2040', '2039/2040'), ('2040/2041', '2040/2041'), ('2041/2042', '2041/2042'), ('2042/2043', '2042/2043'), ('2043/2044', '2043/2044'), ('2044/2045', '2044/2045'), ('2045/2046', '2045/2046'), ('2046/2047', '2046/2047'), ('2047/2048', '2047/2048'), ('2048/2049', '2048/2049'), ('2049/2050', '2049/2050'), ('2050/2051', '2050/2051'), ('2051/2052', '2051/2052'), ('2052/2053', '2052/2053'), ('2053/2054', '2053/2054'), ('2054/2055', '2054/2055'), ('2055/2056', '2055/2056'), ('2056/2057', '2056/2057'), ('2057/2058', '2057/2058'), ('2058/2059', '2058/2059'), ('2059/2060', '2059/2060'), ('2060/2061', '2060/2061'), ('2061/2062', '2061/2062'), ('2062/2063', '2062/2063'), ('2063/2064', '2063/2064'), ('2064/2065', '2064/2065'), ('2065/2066', '2065/2066'), ('2066/2067', '2066/2067'), ('2067/2068', '2067/2068'), ('2068/2069', '2068/2069'), ('2069/2070', '2069/2070')], max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='exeatrequest',
            options={'ordering': ['-created_at'], 'verbose_name': 'ExeatRequest', 'verbose_name_plural': 'ExeatRequests'},
        ),
        migrations.AddField(
            model_name='student',
            name='guardian_phone',
            field=models.CharField(default=9035077050, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='name',
            field=models.CharField(default='Lagbaja', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exeatrequest',
            name='session',
            field=models.ForeignKey(default=0.9995061728395062, on_delete=django.db.models.deletion.CASCADE, to='core.session'),
            preserve_default=False,
        ),
    ]
