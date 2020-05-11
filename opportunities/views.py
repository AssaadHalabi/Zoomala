from django.shortcuts import render,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Opportunity
from django.http import HttpResponseForbidden
from .forms import OpportunityForm
from django.urls import reverse


OpportunityListContext= None


class OpportunitiesListView(LoginRequiredMixin,ListView):
    
    template_name = "opportunities/opportunities.html"
    success_url='./'
    paginate_by= 25

    def get_queryset(self):
        searchParams = self.request.GET.get('q', None)
        if searchParams !=None:
            return Opportunity.objects.search_by_generic(searchParams)
        return Opportunity.objects.all().order_by('-date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        searchParams = self.request.GET.get('q', None)
        context['opportunities']= self.get_queryset()
        context['searchParams']= searchParams
        OpportunityListContext = context
        return context

        
class OpportunityCreateView(CreateView):
    template_name= 'opportunities/opportunity_create.html'
    form_class= OpportunityForm
    queryset = Opportunity.objects.all()

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.recruiter = self.request.user.username
        self.object.save()
        return super().form_valid(form)

class OpportunityUpdateView(UpdateView):
    template_name= 'opportunities/opportunity_create.html'
    form_class= OpportunityForm
    queryset = Opportunity.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Opportunity,id=id_)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.recruiter = self.request.user.username
        self.object.save()
        return super().form_valid(form)


class OpportunityDetailView(DetailView):
    model = Opportunity
    template_name = "opportunities/opportunity_detail.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Opportunity,id=id_)



class OpportunityDeleteView(DeleteView):
    model = Opportunity
    template_name = "opportunities/opportunity_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Opportunity,id=id_)

    def get_success_url(self):
        return reverse("opportunities:searchOpportunities")







