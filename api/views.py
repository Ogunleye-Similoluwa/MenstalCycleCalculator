from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, ListAPIView
from .serializers import *
from menstral_app.models import *
from rest_framework.response import Response
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


class DayDateView(ListCreateAPIView):
    queryset = Cycle.objects.all()
    serializer_class = DayAndDateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        my_date_fresh = request.POST.get("date")
        my_day_fresh = request.POST.get("day")
        my_day = int(my_day_fresh)

        my_date = datetime.strptime(my_date_fresh, "%Y-%m-%d")

        date_list = [my_date]
        day_list = [my_day_fresh]
        formatted_date = []
        my_dict = {}
        for i in range(1, 12):
            next_month = date_list[-1] + timedelta(days=30)

            print(next_month)
            date_list.append(next_month)

        instances = []
        unsafe_days = []
        for day in date_list:
            my_date_1 = int(day.day) // 2
            ovulation_day_first = day.day // 2
            ovulation_day_last = day.day // 2
            new_date = datetime(day.year, day.month, my_date_1)
            instances.append(Cycle(day=day.day, date=day, ovulation_date=new_date))

            for days in range(0, 3):
                ovulation_day_first -= 1

                unsafe_days.append(datetime(day.year, day.month, ovulation_day_first))

            for days in range(0, 3):
                ovulation_day_last += 1
                unsafe_days.append(datetime(day.year, day.month, ovulation_day_last))
            instances.append(Cycle(day=day.day, date=day, ovulation_date=new_date))
        Cycle.objects.bulk_create(instances)

        # Return all fields of the created cycles
        # created_cycles = Cycle.objects.filter(date__in=date_list)
        # serializer = self.get_serializer(created_cycles, many=True)
        return self.list(request,*args, **kwargs)


class DeleteDate(DestroyAPIView):
    queryset = Cycle.objects.all()
    serializer_class = DayAndDateSerializer

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
