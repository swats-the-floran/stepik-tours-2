from random import randint as rnd

from django.shortcuts import render, Http404
from django.views import View

from .data import title, subtitle, description, departures, tours


class MainView(View):

    def get(self, request, *args, **kwargs):

        rand_tours = {}
        while len(rand_tours) != 6:
            index = rnd(1, len(tours))
            if index not in rand_tours:
                rand_tours[index] = tours[index]

        context = {
            'title': title,
            'page_title': title,
            'subtitle': subtitle,
            'description': description,
            'departures': departures,
            'tours': rand_tours,
        }

        return render(request, 'tours/index.html', context=context)


class DepartureView(View):

    def get(self, request, departure, *args, **kwargs):

        departure_tours = {key: value for key, value in tours.items() if value['departure'] == departure}
        list_tour = departure_tours.values()
        price_min = min(list_tour, key=lambda x: x['price'])
        price_max = max(list_tour, key=lambda x: x['price'])
        nights_min = min(list_tour, key=lambda x: x['nights'])
        nights_max = max(list_tour, key=lambda x: x['nights'])

        context = {
            'title': title,
            'page_title': title,
            'departures': departures,
            'departure': departures[departure],
            'tours': departure_tours,
            'price_min': price_min['price'],
            'price_max': price_max['price'],
            'nights_min': nights_min['nights'],
            'nights_max': nights_max['nights'],
        }

        return render(request, 'tours/departure.html', context=context)


class TourView(View):

    def get(self, request, id, *args, **kwargs):

        if id not in tours:
            raise Http404

        tour = tours[id]

        context = {
            'page_title': tour['title'] + ' ' + tour['stars'] + ' ★',
            'title': title,
            'tour_departure': departures[tour['departure']],
            'departures': departures,
            'tour': tour,
        }

        return render(request, 'tours/tour.html', context=context)
