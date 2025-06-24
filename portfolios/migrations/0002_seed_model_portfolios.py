from django.db import migrations, models
import decimal


def create_model_portfolios(apps, schema_editor):
    ModelPortfolio = apps.get_model('portfolios', 'ModelPortfolio')
    PortfolioLine = apps.get_model('portfolios', 'PortfolioLine')

    portfolios_data = {
        "Aggressive": {
            "SPY": 39.3,
            "VEA": 17.47,
            "TLT": 43.23
        },
        "Growth": {
            "VTI": 31.75,
            "IEFA": 42.86,
            "AGG": 25.4
        },
        "Income": {
            "SCHD": 0.0,
            "LQD": 57.14,
            "BIL": 42.86
        }
    }

    for name, lines in portfolios_data.items():
        portfolio = ModelPortfolio.objects.create(name=name)
        for asset, target_pct in lines.items():
            PortfolioLine.objects.create(
                portfolio=portfolio,
                asset=asset,
                target_pct=decimal.Decimal(str(target_pct))
            )


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_model_portfolios),
    ]
