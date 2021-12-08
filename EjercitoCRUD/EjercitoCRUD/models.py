# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ArmaTomada(models.Model):
    id_arma_tomada = models.BigAutoField(primary_key=True)
    id_arma = models.ForeignKey('Armas', models.DO_NOTHING, db_column='id_arma')
    momento_toma = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'arma_tomada'


class Armas(models.Model):
    id_arma = models.BigAutoField(primary_key=True)
    nombre_arma = models.CharField(max_length=100)
    danio = models.BigIntegerField()
    tipo_arma = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'armas'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HombresCaidos(models.Model):
    id_deceso = models.BigAutoField(primary_key=True)
    id_soldado = models.ForeignKey('Soldados', models.DO_NOTHING, db_column='id_soldado')
    fecha_de_deceso = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'hombres_caidos'


class NuevasIncorporaciones(models.Model):
    id_incorporacion = models.BigAutoField(primary_key=True)
    id_soldado = models.ForeignKey('Soldados', models.DO_NOTHING, db_column='id_soldado')
    fecha_incorporacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'nuevas_incorporaciones'


class Soldados(models.Model):
    id_soldado = models.BigAutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=50)
    id_arma_tomada = models.ForeignKey(ArmaTomada, models.DO_NOTHING, db_column='id_arma_tomada', blank=True, null=True)
    herido = models.BooleanField()
    vivo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'soldados'
