from django.shortcuts import render, HttpResponse
from .models import Lead
from .forms import LeadForm

def lead_list(request):
    leads = Lead.objects.all()

    context = {
        'leads': leads
    }
    return render(request, "leads/lead_list.html", context)

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead':lead
    }
    return render(request, 'leads/lead_detail.html', context)

def lead_create(request):
    form = LeadForm()
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            print("The form has been validated")
            print(form.cleaned_data )
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create.html', context)
