from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ledger.models import Account, RiskProfile
from .models import ModelPortfolio
from .utils import fetch_nav
from django.contrib import messages

DRIFT_THRESHOLD = Decimal('5.0')

@login_required
def portfolio_list(request):
    profile = RiskProfile.objects.filter(user=request.user).order_by('-created_at').first()
    if not profile:
        return render(request, 'portfolios/no_profile.html')
    portfolios = ModelPortfolio.objects.filter(name__icontains=profile.investor_type)
    account = Account.objects.get(user=request.user)
    total_value = Decimal(account.balance)
    results = []
    for p in portfolios:
        lines = []
        current_values = []
        for line in p.lines.all():
            price = fetch_nav(line.asset)
            if price is None:
                continue
            invested_amt = (line.target_pct / Decimal('100')) * total_value
            shares = invested_amt / Decimal(price)
            current_val = shares * Decimal(price)
            lines.append({
                'asset': line.asset,
                'target_pct': line.target_pct,
                'current_val': round(current_val, 2),
            })
            current_values.append(current_val)
        portfolio_current_total = sum(current_values)
        max_drift = Decimal('0')
        for ln in lines:
            if portfolio_current_total == 0:
                actual_pct = Decimal('0')
            else:
                actual_pct = (ln['current_val'] / portfolio_current_total) * Decimal('100')
            drift = abs(actual_pct - ln['target_pct'])
            ln['actual_pct'] = round(actual_pct, 2)
            ln['drift'] = round(drift, 2)
            if drift > max_drift:
                max_drift = drift
        results.append({
            'portfolio': p,
            'lines': lines,
            'rebalance': max_drift > DRIFT_THRESHOLD,
            'max_drift': round(max_drift, 2),
        })
    return render(request, 'portfolios/list.html', {
        'results': results,
    })



@login_required
def manual_rebalance(request):
    account = Account.objects.get(user=request.user)
    risk_profile = RiskProfile.objects.filter(user=request.user).last()
    if not risk_profile:
        return redirect('risk_profile')

    portfolio = ModelPortfolio.objects.filter(name__icontains=risk_profile.investor_type).first()
    if not portfolio:
        return redirect('portfolio_list')

    target_allocation = []
    current_allocation = []
    suggestions = []

    total_value = Decimal('0.0')
    actual_values = {}

    for line in portfolio.lines.all():
        nav = fetch_nav(line.asset)
        if nav is None:
            continue
        invested_amt = (line.target_pct / Decimal('100')) * account.balance
        shares = invested_amt / Decimal(nav)
        current_val = shares * Decimal(nav)
        actual_values[line.asset] = current_val
        total_value += current_val

    for line in portfolio.lines.all():
        nav = fetch_nav(line.asset)
        if nav is None or line.asset not in actual_values:
            continue
        current_val = actual_values[line.asset]
        if total_value == 0:
            actual_pct = Decimal('0')
        else:
            actual_pct = (current_val / total_value) * Decimal('100')
        actual_pct = (current_val / total_value) * Decimal('100')
        drift = round(actual_pct - line.target_pct, 2)
        target_allocation.append({
            'asset': line.asset,
            'target_pct': line.target_pct
        })
        current_allocation.append({
            'asset': line.asset,
            'actual_pct': round(actual_pct, 2)
        })
        suggestions.append({
            'asset': line.asset,
            'drift': drift,
            'action': 'Sell' if drift > 0 else 'Buy',
            'amount': abs(drift)
        })

    paired_allocation = zip(target_allocation, current_allocation)

    return render(request, 'portfolios/manual_rebalance.html', {
        'portfolio': portfolio,
        'target_allocation': target_allocation,
        'current_allocation': current_allocation,
        'suggestions': suggestions,
        'paired_allocation': paired_allocation
    })



@login_required
def apply_manual_rebalance(request):
    if request.method == 'POST':
        account = Account.objects.get(user=request.user)
        profile = RiskProfile.objects.filter(user=request.user).last()
        portfolio = ModelPortfolio.objects.filter(name__icontains=profile.investor_type).first()

        for line in portfolio.lines.all():
            field_name = f"target_{line.asset}"
            new_target = request.POST.get(field_name)
            if new_target:
                try:
                    new_target = new_target.replace(',', '.')
                    line.target_pct = Decimal(new_target)
                    line.save()
                except:
                    messages.error(request, f"Invalid input for {line.asset}.")
        messages.success(request, "Manual rebalancing changes applied.")
        return redirect('portfolio_list')
    return redirect('dashboard')