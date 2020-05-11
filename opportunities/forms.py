from django.forms import ModelForm
from .models import Opportunity
from django.urls import reverse


class OpportunityForm(ModelForm):
    
    class Meta:
        model = Opportunity
        fields = ['title', 'jobType' , 'image', 'location','link', 'company']

        



    


