from django.shortcuts import render, redirect, get_object_or_404
from .models import Device, Data
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import random
from django.http import HttpResponseRedirect
from .forms import ModifyDevicesForm
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
)
import json
import datetime

# Create your views here.


def home(request):

    form = ModifyDevicesForm(user=request.user)

    context = {
        'form': form,

    }

    return render(request, 'sensor/home.html', context)


def generate(request):
    rand = random.randint(1, 100000)
    newID = Device.objects.create(device_id=rand, owner=request.user)

    if newID.validate_unique():
        Device.save(newID)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeviceListView(ListView):
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)
    model = Device
    template_name = 'sensor/home.html'
    context_object_name = 'devices'


class DeviceDetailView(DetailView):
    model = Device


    def get_context_data(self, **kwargs):
        context = super(DeviceDetailView, self).get_context_data(**kwargs)
        queryset = Data.objects.all().filter(device__owner=self.request.user, device_id=self.object)
        dates = [da.date_posted for da in queryset]
        temp = [obj.temp for obj in queryset]
        water = [obj.water for obj in queryset]
        humidity = [obj.humidity for obj in queryset]

        context['date'] = json.dumps(dates, default=datetime_handler)
        context['temp'] = json.dumps(temp)
        context['water'] = json.dumps(water)
        context['humidity'] = json.dumps(humidity)
        return context


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


class DeviceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Device
    success_url = '/sensor'


    def test_func(self):
        device = self.get_object()
        if self.request.user == device.owner:
            return True
        return False


