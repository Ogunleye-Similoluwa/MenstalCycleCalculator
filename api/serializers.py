from rest_framework import serializers
from menstral_app.models import *
from datetime import date, datetime, timedelta


class DayAndDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = ['day', 'date', "ovulation_date", "fertile_dates"]

#     ovulation_date = serializers.SerializerMethodField(method_name="get_ovulation_period")
#
#     fertile_dates = serializers.SerializerMethodField(method_name="get_fertile_dates")
#
#     def get_ovulation_period(self, cycle: Cycle):
#         my_date = int(cycle.date.day) // 2
#         new_date = datetime(cycle.date.year, cycle.date.month, my_date)
#
#         return new_date
#
#     def get_fertile_dates(self, cycle: Cycle):
#         ovulation_day_first = (cycle.date.day // 2)
#         unsafe_days = []
#
#         for days in range(0, 3):
#             ovulation_day_first -= 1
#
#             unsafe_days.append(datetime(cycle.date.year, cycle.date.month, ovulation_day_first))
#
#         ovulation_day_last = round(cycle.date.day // 2)
#         for days in range(0, 3):
#             ovulation_day_last += 1
#             unsafe_days.append(datetime(cycle.date.year, cycle.date.month, ovulation_day_last))
#         return sorted(unsafe_days)
#
#
# class ImportantDaysSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImportantDays
#         fields = ["ovulation_date", "fertile_dates"]
