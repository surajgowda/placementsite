from django import forms
from .models import CustomUser, Company

class CompanyApplicationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['companies_applied']
        widgets = {
            'companies_applied': forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['companies_applied'].queryset = Company.objects.all()
