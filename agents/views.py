import random
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizorAndLoginRequiredMixin
from django.core.mail import send_mail

class AgentListView(OrganizorAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organization=organisation)

class AgentCreateView(OrganizorAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_organizor = False
        user.is_agent = True
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()

        Agent.objects.create(
            user=user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject = "You are invited to be an agent",
            message = "You were added as agent on DJ CRM. Please login to start working.",
            from_email = "test@gmail.com",
            recipient_list = [user.email]
        )
        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(OrganizorAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organization=organisation)

class AgentUpdateView(OrganizorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organization=organisation)

class AgentDeleteView(OrganizorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    #queryset = Agent.objects.all()

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organization=organisation)
    
    def get_success_url(self):
        return reverse("agents:agent-list")