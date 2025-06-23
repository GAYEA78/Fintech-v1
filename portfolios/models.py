from django.db import models

class ModelPortfolio(models.Model):

    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PortfolioLine(models.Model):

    portfolio  = models.ForeignKey(ModelPortfolio, on_delete=models.CASCADE, related_name='lines')
    asset      = models.CharField(max_length=10, help_text="Ticker symbol, e.g. SPY")
    target_pct = models.DecimalField(max_digits=5, decimal_places=2, help_text="e.g. 60.00 for 60%")

    class Meta:
        unique_together = ('portfolio','asset')

    def __str__(self):
        return f"{self.portfolio.name}: {self.asset} {self.target_pct}%"
