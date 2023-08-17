from django.shortcuts import render, redirect
from .models import CustomUser, Company, Updates, Notifications
import pytz
from datetime import datetime
from django.utils import timezone
from .forms import CompanyApplicationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        print(request.POST['username'],request.POST['password'])
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('user')
            login(request, user)
            return redirect('MyAccount') 
        else:
            # Invalid login
            return render(request, 'Login.html', {'error': 'Invalid username or password'})

    return render(request, 'Login.html')
    
def home(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user)
        now = timezone.now()
        upd = Updates.objects.filter(company__in=user.companies_applied.all())
        updates = Updates.objects.filter(
            company__in=user.companies_applied.all(),
            date__gte=now
        ).order_by('-date')  # Order by date in descending order
        return render(request, 'MyAccount.html', {'getready': updates,'applied':upd})
    else:
        # Handle case where user is not authenticated
        return render(request, 'placement.html')

@login_required
def companies(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies':companies})

@login_required
def company(request, pk):
    company = Company.objects.get(pk=pk)
    updates = Updates.objects.filter(company=company)
    return render(request, 'company.html', {'company':company, 'updates':updates})

def about(request):
    return render(request, 'about.html')

@login_required
def notifications(request):
    notif = Notifications.objects.all()
    return render(request, 'notifications.html', {'notif':notif})

@login_required
def update_companies_applied(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    
    if request.method == 'POST':
        form = CompanyApplicationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Companies applied updated successfully!')
            return redirect('MyAccount') 
    else:
        form = CompanyApplicationForm(instance=user)
    
    return render(request, 'update_companies.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('Login')

