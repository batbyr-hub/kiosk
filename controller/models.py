# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100)
    is_active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ads'


class AllLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    userid = models.IntegerField()
    user_name = models.CharField(max_length=255)
    comment = models.TextField()
    processing = models.CharField(max_length=255)
    trans_id = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'all_log'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class AziinDugaar(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'aziin_dugaar'


class Bagts(models.Model):
    id = models.BigAutoField(primary_key=True)
    numbertype = models.CharField(max_length=255, blank=True, null=True)
    negj = models.CharField(max_length=255, blank=True, null=True)
    data = models.CharField(max_length=255, blank=True, null=True)
    honog = models.CharField(max_length=255, blank=True, null=True)
    nuhtsul = models.CharField(max_length=255, blank=True, null=True)
    une = models.IntegerField()
    is_active = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bagts'


class Cashlog(models.Model):
    money = models.CharField(max_length=255, blank=True, null=True)
    orders = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    kiosk = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING, blank=True, null=True)
    sim = models.ForeignKey('Sims', models.DO_NOTHING, blank=True, null=True)
    payment = models.CharField(max_length=255, blank=True, null=True)
    money_charged = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cashlog'


class Data(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    profile_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100)
    balance = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    price = models.IntegerField()
    sku = models.CharField(db_column='SKU', max_length=200)  # Field name made lowercase.
    is_active = models.IntegerField()
    hyazgaar = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'data'


class DataUsage(models.Model):
    data = models.ForeignKey(Data, models.DO_NOTHING)
    typeofservice = models.ForeignKey('Type0Fservice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'data_usage'
        unique_together = (('data', 'typeofservice'),)


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


class Jwt(models.Model):
    kiosk_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    device_id = models.CharField(max_length=255)
    jwt = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'jwt'


class KartInfo(models.Model):
    kiosk_id = models.IntegerField(blank=True, null=True)
    operation = models.CharField(max_length=10, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    trace_no = models.CharField(max_length=6, blank=True, null=True)
    db_ref_no = models.CharField(max_length=16, blank=True, null=True)
    rrn = models.CharField(max_length=12, blank=True, null=True)
    auth_code = models.CharField(max_length=6, blank=True, null=True)
    entry_mode = models.CharField(max_length=50, blank=True, null=True)
    terminal_id = models.CharField(max_length=8, blank=True, null=True)
    merchant_id = models.CharField(max_length=15, blank=True, null=True)
    merchant_name = models.CharField(max_length=50, blank=True, null=True)
    pan = models.CharField(max_length=25, blank=True, null=True)
    card_holder_name = models.CharField(max_length=40, blank=True, null=True)
    batch_no = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    app_name = models.CharField(max_length=50, blank=True, null=True)
    tc = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kart_info'


class Lottery(models.Model):
    kiosk = models.ForeignKey('Status', models.DO_NOTHING, blank=True, null=True)
    success = models.TextField(blank=True, null=True)
    billid = models.TextField(db_column='billId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField()
    mac_address = models.TextField(blank=True, null=True)
    register_number = models.CharField(max_length=255, blank=True, null=True)
    internal_code = models.TextField(blank=True, null=True)
    bill_type = models.CharField(max_length=255, blank=True, null=True)
    qr_data = models.TextField(blank=True, null=True)
    lottery = models.CharField(max_length=255, blank=True, null=True)
    paid = models.CharField(max_length=255, blank=True, null=True)
    vat = models.CharField(max_length=200, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    order = models.CharField(max_length=255, blank=True, null=True)
    ttd = models.TextField(blank=True, null=True)
    lottery_warning = models.TextField(blank=True, null=True)
    sales_type = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'lottery'


class Numbertype(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=100)
    is_active = models.IntegerField()
    price = models.IntegerField(blank=True, null=True)
    types_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'numbertype'


class Orders(models.Model):
    product_name = models.CharField(max_length=200, blank=True, null=True)
    product_profile_id = models.CharField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=200, blank=True, null=True)
    paid = models.CharField(max_length=200, blank=True, null=True)
    must_pay = models.CharField(max_length=200, blank=True, null=True)
    order_success = models.IntegerField()
    trans_id = models.CharField(max_length=200, blank=True, null=True)
    kiosk_name = models.CharField(max_length=200, blank=True, null=True)
    charge_user_id = models.IntegerField(blank=True, null=True)
    prepaid = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'orders'


class Prefix(models.Model):
    prefix = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Numbertype, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prefix'


class Prefixab(models.Model):
    prefix = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'prefixab'


class PricePlan(models.Model):
    code = models.CharField(max_length=255)
    type_id = models.CharField(max_length=255)
    bagts_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'price_plan'


class Qpay(models.Model):
    number = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    invoice_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'qpay'


class Setup(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    card_dispenser_comm_open_code = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'setup'


class Sims(models.Model):
    serial = models.CharField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=200, blank=True, null=True)
    is_sold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    number_price = models.CharField(max_length=100, blank=True, null=True)
    paid = models.CharField(max_length=200, blank=True, null=True)
    number_type = models.ForeignKey(Numbertype, models.DO_NOTHING, blank=True, null=True)
    is_number_created = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=200, blank=True, null=True)
    kiosk_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sims'


class Status(models.Model):
    device_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_carddispenser_active = models.IntegerField()
    sim_card_total = models.IntegerField()
    is_casher_active = models.IntegerField()
    cash_total = models.IntegerField()
    printer_counter = models.IntegerField()
    address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    card_dispenser_comm_open_code = models.IntegerField(blank=True, null=True)
    sales_id = models.CharField(max_length=255)
    sales_location_id = models.CharField(max_length=255)
    ruim_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'status'


class Type0Fservice(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'type0fservice'


class Unit(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    profile_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100)
    balance = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    price = models.IntegerField()
    sku = models.CharField(db_column='SKU', max_length=200)  # Field name made lowercase.
    is_active = models.IntegerField()
    honog = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'unit'


class UnitUsage(models.Model):
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    typeofservice = models.ForeignKey(Type0Fservice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'unit_usage'
        unique_together = (('unit', 'typeofservice'),)


class UsGroup(models.Model):
    name = models.CharField(unique=True, max_length=50)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'us_group'


class UsGroupPermission(models.Model):
    group = models.ForeignKey(UsGroup, models.DO_NOTHING, primary_key=True)
    permission = models.ForeignKey('UsPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'us_group_permission'
        unique_together = (('group', 'permission'),)


class UsPermission(models.Model):
    description = models.CharField(unique=True, max_length=255, blank=True, null=True)
    app_name = models.CharField(max_length=50, blank=True, null=True)
    module = models.CharField(max_length=50, blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'us_permission'


class UsUserGroup(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, primary_key=True)
    group = models.ForeignKey(UsGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'us_user_group'
        unique_together = (('user', 'group'),)


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_type = models.ForeignKey('UserType', models.DO_NOTHING, blank=True, null=True)
    username = models.CharField(unique=True, max_length=250)
    phone = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=255)
    pass_status = models.IntegerField(blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    salt = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    parent_id = models.BigIntegerField()
    status = models.ForeignKey('UserStatus', models.DO_NOTHING, blank=True, null=True)
    created_date = models.DateTimeField()
    created_user = models.BigIntegerField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    modified_user = models.BigIntegerField(blank=True, null=True)
    access_retry_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserConfirmation(models.Model):
    id = models.BigAutoField(primary_key=True)
    kiosk_name = models.CharField(max_length=255, blank=True, null=True)
    register = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_confirmation'


class UserLog(models.Model):
    reportid = models.BigAutoField(primary_key=True)
    module_name = models.CharField(max_length=200)
    action_name = models.CharField(max_length=100)
    user_id = models.BigIntegerField()
    ip_address = models.CharField(max_length=100)
    receive_content = models.TextField()
    status = models.CharField(max_length=100)
    status_reason = models.TextField()
    log_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_log'


class UserStatus(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_status'


class UserType(models.Model):
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'


class Users(models.Model):
    family_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    birthday = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    register = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    soum = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'users'
