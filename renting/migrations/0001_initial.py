# Generated by Django 2.2.3 on 2019-11-02 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentingOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=8, null=True)),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('cod', 'Cash On Delivery'), ('delivered', 'Delivered'), ('refunded', 'Refunded'), ('order_complete', 'Order Complete')], max_length=40)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('total_days_on_rent', models.IntegerField(blank=True, null=True)),
                ('total_days_out', models.IntegerField(blank=True, null=True)),
                ('total_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_renting_order', to='billing.BillingProfile')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]