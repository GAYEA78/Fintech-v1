# Generated by Django 4.2 on 2025-06-13 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ledger', '0003_kycdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(choices=[('none', 'No experience'), ('some', 'Some experience'), ('experienced', 'Experienced')], max_length=12)),
                ('goals', models.CharField(choices=[('preservation', 'Capital preservation'), ('income', 'Steady income'), ('growth', 'Growth')], max_length=12)),
                ('time_horizon', models.IntegerField(help_text='Years you plan to invest')),
                ('risk_tolerance', models.CharField(choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')], max_length=8)),
                ('investor_type', models.CharField(blank=True, help_text='Aggressive / Growth / Income', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
