from django.db import migrations

def create_model_portfolios(apps, schema_editor):
    ModelPortfolio = apps.get_model('portfolios', 'ModelPortfolio')
    PortfolioLine = apps.get_model('portfolios', 'PortfolioLine')

    # Income Focused Portfolio
    income = ModelPortfolio.objects.create(name='Income Focused Portfolio')
    PortfolioLine.objects.create(portfolio=income, asset='BIL', target_pct=42.86)
    PortfolioLine.objects.create(portfolio=income, asset='LQD', target_pct=57.14)
    PortfolioLine.objects.create(portfolio=income, asset='SCHD', target_pct=0.00)

    # Growth Plan
    growth = ModelPortfolio.objects.create(name='Growth Plan')
    PortfolioLine.objects.create(portfolio=growth, asset='AGG', target_pct=25.40)
    PortfolioLine.objects.create(portfolio=growth, asset='IEFA', target_pct=42.86)
    PortfolioLine.objects.create(portfolio=growth, asset='VTI', target_pct=31.75)

    # Aggressive Strategy
    aggressive = ModelPortfolio.objects.create(name='Aggressive Strategy')
    PortfolioLine.objects.create(portfolio=aggressive, asset='TLT', target_pct=43.23)
    PortfolioLine.objects.create(portfolio=aggressive, asset='VEA', target_pct=17.47)
    PortfolioLine.objects.create(portfolio=aggressive, asset='SPY', target_pct=39.30)

def delete_model_portfolios(apps, schema_editor):
    ModelPortfolio = apps.get_model('portfolios', 'ModelPortfolio')
    ModelPortfolio.objects.filter(name__in=[
        'Income Focused Portfolio', 'Growth Plan', 'Aggressive Strategy'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_model_portfolios, delete_model_portfolios),
    ]
