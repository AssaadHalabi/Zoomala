from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.db.models import Q
from PIL import Image



class Opportunity_Query_set(models.QuerySet):
    def search_by_type(self, query):
        typeLookup =  Q(jobType__icontains= query)
        return self.filter(typeLookup).distinct()

    def search_by_location(self, query):
        Lookup =  Q(location__icontains= query)
        return self.filter(Lookup).distinct()

    def search_by_tags(self, query):
        Lookup =  Q(tags__icontains= query)
        return self.filter(Lookup).distinct()

    def search_by_generic(self, query):
        Lookup =  Q(title__icontains= query) | Q(tags__icontains= query) | Q(location__icontains= query) |  Q(jobType__icontains= query)
        return self.filter(Lookup).distinct()
    


class OpportunityManager(models.Manager):

    def get_queryset(self):
        return Opportunity_Query_set(self.model, using=self._db)

    def search_by_type(self, query):
        return self.get_queryset().search_by_type(query)

    def search_by_location(self, query):
        return self.get_queryset().search_by_location(query)

    def search_by_tags(self, query):
       return self.get_queryset().search_by_tags(query)

    def search_by_generic(self, query):
        return self.get_queryset().search_by_generic(query)


class Opportunity(models.Model):

    title = models.CharField(_("title"), max_length=100)
    jobType = models.CharField(_("type"), max_length=30)
    # salary = models.DecimalField(_("salary"), max_digits=5, decimal_places=1, blank=True, null=True)
    tags = models.CharField(_("tags"), max_length=100, blank=True)
    date = models.DateField(_("pub_date"), auto_now_add=True)
    image = models.ImageField(_("opImage"), upload_to='opportunities', default='defaultJobImg.jpg')
    # description = models.CharField(_("description"), max_length=200, blank=True)
    location = models.CharField(_("location"), max_length=50)
    link = models.CharField(_("link"), max_length=2000)
    company = models.CharField(_("company"), max_length=30, blank=True)

    objects = OpportunityManager()





    
