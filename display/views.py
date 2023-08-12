from django.shortcuts import render
from .models import CustomUser, Company, Updates

# Create your views here.
def home(request):
    cand = CustomUser.objects.get(username=request.user)
    upd = Updates.objects.filter(company__in=cand.companies_applied.all())
    date = Updates.objects.filter(date__date__gte=timezone.now().date())
    return render(request, 'MyAccount.html', {'updates':upd})


def companies(request):
    companies = Company.objects.all()
    return render(request, 'companies.html', {'companies':companies})

def company(request, pk):
    company = Company.objects.get(pk=pk)
    updates = Updates.objects.filter(company=company)
    return render(request, 'company.html', {'company':company, 'updates':updates})

def placement(request):
    return render(request, 'placement.html')

def about(request):
    return render(request, 'about.html')


def login(request):
    return render(request, 'Login.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request,'about.html')

def register(request):
    return render(request, 'Register.html')

def Dashboard(request):
    return render(request, 'MyAccount.html')


