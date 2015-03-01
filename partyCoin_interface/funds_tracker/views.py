#from django.shortcuts import render
from django.views import generic
from funds_tracker.models import Donation

# Create your views here.


class IndexView(generic.ListView):
    model = Donation
    template_name = 'funds_tracker/index.html'
    context_object_name = 'all_donations'

    def get_queryset(self):
        return Donation.objects.order_by('year')
