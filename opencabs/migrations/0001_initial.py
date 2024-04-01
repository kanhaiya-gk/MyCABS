# Generated by Django 2.2.7 on 2021-10-25 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_point', models.TextField(blank=True, default='', max_length=200)),
                ('booking_type', models.CharField(choices=[('OW', 'One way'), ('RT', 'Round trip')], max_length=2)),
                ('travel_date', models.DateField()),
                ('travel_time', models.TimeField()),
                ('vehicle_count', models.PositiveIntegerField(blank=True, default=1)),
                ('passengers', models.IntegerField(blank=True, default=1)),
                ('customer_name', models.CharField(db_index=True, max_length=100, verbose_name='Name')),
                ('customer_mobile', models.CharField(blank=True, db_index=True, default='', max_length=20, verbose_name='Mobile')),
                ('customer_email', models.EmailField(blank=True, db_index=True, default='', max_length=254, verbose_name='Email')),
                ('ssr', models.TextField(blank=True, default='', help_text='Special service request', max_length=200, verbose_name='Special service request')),
                ('status', models.CharField(choices=[('0', 'Request'), ('1', 'Confirmed'), ('2', 'Declined'), ('3', 'Attempt')], default='0', max_length=1)),
                ('payment_method', models.CharField(blank=True, choices=[('POA', 'Pay on arrival'), ('ONL', 'Online'), ('', '')], default='', max_length=3, null=True)),
                ('payment_status', models.CharField(blank=True, choices=[('NP', 'Not paid'), ('PR', 'Partial'), ('PD', 'Paid')], default='NP', max_length=3, null=True)),
                ('payment_done', models.PositiveIntegerField(blank=True, default=0)),
                ('payment_due', models.PositiveIntegerField(blank=True, default=0)),
                ('revenue', models.IntegerField(blank=True, default=0)),
                ('last_payment_date', models.DateTimeField(blank=True, null=True)),
                ('accounts_verified', models.BooleanField(db_index=True, default=False)),
                ('booking_id', models.CharField(blank=True, db_index=True, editable=False, max_length=20, unique=True)),
                ('total_fare', models.PositiveIntegerField(blank=True, default=0)),
                ('fare_details', models.TextField(blank=True, default='{}')),
                ('distance', models.PositiveIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('mobile', models.CharField(db_index=True, max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicles')),
                ('passengers', models.IntegerField(blank=True, default=4)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, default='', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleRateCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, unique=True)),
                ('description', models.TextField(blank=True, default='', max_length=200)),
                ('tariff_per_km', models.PositiveIntegerField()),
                ('tariff_after_hours', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencabs.VehicleCategory')),
                ('features', models.ManyToManyField(blank=True, to='opencabs.VehicleFeature')),
            ],
            options={
                'unique_together': {('name', 'category')},
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('number', models.CharField(db_index=True, max_length=20, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='opencabs.VehicleCategory')),
                ('driver', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opencabs.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='BookingVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_paid', models.BooleanField(default=False)),
                ('driver_pay', models.PositiveIntegerField(blank=True, default=0)),
                ('driver_invoice_id', models.CharField(blank=True, max_length=50)),
                ('extra_info', models.TextField(blank=True, default='')),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opencabs.Booking')),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opencabs.Driver')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='opencabs.Vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking_destination', to='opencabs.Place'),
        ),
        migrations.AddField(
            model_name='booking',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking_source', to='opencabs.Place'),
        ),
        migrations.AddField(
            model_name='booking',
            name='vehicle_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='booking', to='opencabs.VehicleRateCategory'),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('opencabs.booking',),
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oneway_price', models.PositiveIntegerField()),
                ('oneway_distance', models.PositiveIntegerField(blank=True, default=0)),
                ('oneway_driver_charge', models.PositiveIntegerField()),
                ('roundtrip_price', models.PositiveIntegerField(blank=True, default=0)),
                ('roundtrip_distance', models.PositiveIntegerField(blank=True, default=0)),
                ('roundtrip_driver_charge', models.PositiveIntegerField(blank=True, default=0)),
                ('code', models.CharField(blank=True, db_index=True, editable=False, max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rate_destination', to='opencabs.Place')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rate_source', to='opencabs.Place')),
                ('vehicle_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rate', to='opencabs.VehicleRateCategory')),
            ],
            options={
                'unique_together': {('code', 'vehicle_category')},
            },
        ),
    ]
