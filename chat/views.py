from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView

from .forms import ComposeForm
from .models import Thread, ChatMessage
from profiles.models import Profile


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['threads']= self.get_queryset()
        otherProfiles = []
        myThreads = Thread.objects.by_user(self.request.user).order_by('-timestamp')
        for myThread in myThreads:
            if myThread.first.username == self.request.user.username:
                otherProfiles.append(Profile.objects.get(user__username=myThread.second.username))
            else:
                otherProfiles.append(Profile.objects.get(user__username=myThread.first.username))
        
        context['otherProfiles'] = otherProfiles
        return context


# def inbox(request):
#     return render(request, 'chat/inbox.html')


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    
    def get_success_url(self):
        return reverse("chat:thread" , kwargs={'username':self.kwargs.get("username")})

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['username']= self.kwargs.get("username")
        # context['username'] = str([x for x in self.kwargs.items()])
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)


