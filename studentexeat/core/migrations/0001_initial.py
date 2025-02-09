# Generated by Django 5.1.4 on 2024-12-15 08:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.CharField(choices=[('Accounting', 'Accounting'), ('Biochemistry', 'Biochemistry'), ('Biotechnology', 'Biotechnology'), ('Business Administration', 'Business Administration'), ('Computer Science', 'Computer Science'), ('Economics', 'Economics'), ('International Relations', 'International Relations'), ('Law', 'Law'), ('Mass Communication', 'Mass Communication'), ('Mathematics', 'Mathematics'), ('Medical Lab Science', 'Medical Lab Science'), ('Microbiology', 'Microbiology'), ('Nursing', 'Nursing'), ('Physiotherapy', 'Physiotherapy'), ('Political Science', 'Political Science'), ('Public Health', 'Public Health')], max_length=50)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('student_id', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=10)),
                ('guardian_email', models.EmailField(max_length=254)),
                ('dept', models.CharField(choices=[('Accounting', 'Accounting'), ('Biochemistry', 'Biochemistry'), ('Biotechnology', 'Biotechnology'), ('Business Administration', 'Business Administration'), ('Computer Science', 'Computer Science'), ('Economics', 'Economics'), ('International Relations', 'International Relations'), ('Law', 'Law'), ('Mass Communication', 'Mass Communication'), ('Mathematics', 'Mathematics'), ('Medical Lab Science', 'Medical Lab Science'), ('Microbiology', 'Microbiology'), ('Nursing', 'Nursing'), ('Physiotherapy', 'Physiotherapy'), ('Political Science', 'Political Science'), ('Public Health', 'Public Health')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='ExeatRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('evidence', models.ImageField(help_text='Supporting proof', upload_to='evidence/')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('approved_by_student_affairs', models.BooleanField(default=False)),
                ('approved_by_hod', models.BooleanField(default=False)),
                ('approved_by_warden', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
            options={
                'verbose_name': 'ExeatRequest',
                'verbose_name_plural': 'ExeatRequests',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('StudentAffairs', 'Student Affairs'), ('HeadOfDepartment', 'Head of Department'), ('HallWarden', 'Hall Warden')], max_length=20)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserRole',
                'verbose_name_plural': 'UserRoles',
            },
        ),
    ]
