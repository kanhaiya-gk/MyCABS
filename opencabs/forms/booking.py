# from tkinter import Place
from django import forms
from django.conf import settings
from django.template.loader import render_to_string

from ..models import Booking, Rate, BOOKING_PAYMENT_METHOD_CHOICES_DICT, VehicleRateCategory, Place

import heapq

def dijkstra(graph, src):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[src] = 0
    pq = [(0, src)]
    print(graph)
    print("----------")

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

def find_minimum_time(from_places, to_places, vehicle_categories, times, src, dst):
    # graph = {}

    # Create the graph
    # for i in range(len(from_places)):
    #     if from_places[i] not in graph:
    #         graph[from_places[i]] = {}
    #     if to_places[i] not in graph:
    #         graph[to_places[i]] = {}
    #     graph[from_places[i]][to_places[i]] = times[i]

    min_times = {}
    for vc in set(vehicle_categories):
        # Filter times for the current vehicle category
        print(vc)
        print("++++++")
        graph = {}
        # filtered_times = [times[i] for i in range(len(times)) if vehicle_categories[i].name == vc.name]
        for i in range(len(from_places)):
            if vehicle_categories[i].name != vc.name:
                continue
            if from_places[i] not in graph:
                graph[from_places[i]] = {}
            if to_places[i] not in graph:
                graph[to_places[i]] = {}
            graph[from_places[i]][to_places[i]] = times[i]
        min_times[vc] = dijkstra(graph, src)
    return min_times

# # Example usage:
# from_places = ['A', 'A', 'B', 'B', 'C', 'D']
# to_places = ['B', 'C', 'C', 'D', 'D', 'E']
# vehicle_categories = ['car', 'car', 'truck', 'truck', 'bus', 'bus']
# times = [3, 5, 7, 10, 12, 15]

# src = 'A'
# dst = 'E'

# min_times = find_minimum_time(from_places, to_places, vehicle_categories, times, src, dst)
# print(min_times)

class BaseBookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class BookingTravelForm(BaseBookingForm):
    class Meta:
        model = Booking
        fields = (
            'source', 'destination', 'booking_type',
            'travel_date', 'travel_time', 'passengers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['booking_type'].widget = forms.RadioSelect()
        self.fields['booking_type'].widget.choices = self.fields['booking_type'].choices[1:]
        self.fields['booking_type'].widget.attrs = {'class': 'radio-inline'}
        self.fields['source'].queryset = self.fields['source'].queryset.order_by('name')
        self.fields['destination'].queryset = self.fields['destination'].queryset.order_by('name')



class BookingVehiclesForm(BaseBookingForm):
    class Meta:
        model = Booking
        fields = ('vehicle_type',)

    # def __init__(self, *args, **kwargs):
    #     source = kwargs.pop('source')
    #     destination = kwargs.pop('destination')
    #     booking_type = kwargs.pop('booking_type')
    #     super().__init__(*args, **kwargs)
    #     self.fields['vehicle_type'].widget = forms.RadioSelect()
    #     code = settings.ROUTE_CODE_FUNC(source.name, destination.name)
    #     choices = []
    #     for rate in Rate.objects.filter(code=code):
    #         label = render_to_string(
    #             'opencabs/partials/vehicle_rate_label.html',
    #             context={'rate': rate, 'booking_type': booking_type})
    #         choices.append((rate.vehicle_category_id, label))
    #     self.fields['vehicle_type'].choices = choices
    #     self.fields['vehicle_type'].widget.attrs = {'hidden': 'true'}
    
    def __init__(self, *args, **kwargs):
        source = kwargs.pop('source')
        destination = kwargs.pop('destination')
        booking_type = kwargs.pop('booking_type')
        super().__init__(*args, **kwargs)
        self.fields['vehicle_type'].widget = forms.RadioSelect()
        code = settings.ROUTE_CODE_FUNC(source.name, destination.name)
        src = source.name
        dst = destination.name
        all_rates = Rate.objects.all()
        fro = list([all_rate.source.name for all_rate in all_rates])
        to = list([all_rate.destination.name for all_rate in all_rates])
        vc = list([all_rate.vehicle_category for all_rate in all_rates])
        time = list([all_rate.oneway_time for all_rate in all_rates])
        min_times = find_minimum_time(fro, to, vc, time, src, dst)
        availabe_rates = []
        print(min_times)
        for vc, t in min_times.items():
            availabe_rates.append(Rate(source=source, destination=destination, vehicle_category = vc, oneway_time = t[dst]))
        choices = []
        for rate in availabe_rates:
        # for rate in available_rates:
            label = render_to_string(
                'opencabs/partials/vehicle_rate_label.html',
                context={'rate': rate, 'booking_type': booking_type})
            choices.append((rate.vehicle_category_id, label))
        self.fields['vehicle_type'].choices = choices
        self.fields['vehicle_type'].widget.attrs = {'hidden': 'true'}


class BookingContactInfoForm(BaseBookingForm):
    class Meta:
        model = Booking
        fields = ('customer_name', 'customer_mobile', 'customer_email',
                  'pickup_point', 'ssr')
        widgets = {
            'pickup_point': forms.Textarea(attrs={'rows': 3}),
            'ssr': forms.Textarea(attrs={'rows': 3})
        }

    def clean(self):
        cleaned_data = super().clean()
        customer_mobile = cleaned_data.get('customer_mobile')
        customer_email = cleaned_data.get('customer_email')

        if not customer_mobile and not customer_email:
            raise forms.ValidationError(
                'One of mobile and email is required.')


class BookingPaymentInfoForm(BaseBookingForm):
    class Meta:
        model = Booking
        fields = ('payment_method',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].choices = tuple([
            (item, BOOKING_PAYMENT_METHOD_CHOICES_DICT.get(item)) for item in settings.BOOKING_FORM_PAYMENT_MODES
            if BOOKING_PAYMENT_METHOD_CHOICES_DICT.get(item)
        ])
