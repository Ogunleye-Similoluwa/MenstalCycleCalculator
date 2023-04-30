import calendar

from dateutil.relativedelta import relativedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import  FormView
from django.contrib.auth.views import LoginView
from .models import Cycle
from datetime import  timedelta, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin


class MyLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('create')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("login")
        return super(RegisterPage, self).get(*args, **kwargs)


class CycleCreateView(LoginRequiredMixin, View):
    template_name = 'cycle_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        my_date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()

        my_day = int(request.POST['day'])

        date_list = [my_date]
        ovulation_list = []
        next_cycle = (my_date + timedelta(days=my_day))
        unsafe_list = []
        my_list = []
        for i in range(1, 13):
            next_month = date_list[-1] + timedelta(days=my_day)
            print(next_month)
            date_list.append(next_month)

            ovulation_date_1 = (next_month.day + 1) // 2
            last_day_of_month = calendar.monthrange(next_month.year, next_month.month)[1]
            print(last_day_of_month)
            print(ovulation_date_1)
            ovulation_day = min(ovulation_date_1, last_day_of_month)
            print(ovulation_day)

            ovulation_date = datetime(next_month.year, next_month.month, ovulation_day)

            ovulation_list.append(ovulation_date)

            fertile_date_1 = [
                unsafe_list.append(datetime(next_month.year, next_month.month, max(1, ovulation_day - count))) for count
                in range(1, 4)]

            fertile_date_2 = [unsafe_list.append(
                datetime(next_month.year, next_month.month, min(last_day_of_month, ovulation_day + count))) for count in
                              range(1, 4)]
            flow_list = [my_list.append(next_month + timedelta(days=i)) for i in range(0, 8)]

            context = {
                'next_cycle': next_cycle,
                'date': date_list,
                'ovulation_date': ovulation_list,
                'fertile_period': sorted(unsafe_list),
                'flow_date': my_list
            }
        return render(request, 'cycle_form.html', {'cycle': context})

    # context_list = []
    # for day in date_list:
    #     ovulation_date = day + relativedelta(day=day.day // 2)
    #     ovulation_date_str = ovulation_date.strftime("%Y-%m-%d")
    #
    #     fertile_start = ovulation_date - timedelta(days=3)
    #     fertile_end = ovulation_date + timedelta(days=3)
    #     my_list = [fertile_start + timedelta(days=i) for i in range((fertile_end - fertile_start).days + 1)]
    #
    #     fertile_dates = [m_date.strftime("%Y-%m-%d") for m_date in my_list]
    #
    #     context = {
    #         'day': day,
    #         'date': my_date_fresh,
    #         'fertile_dates': fertile_dates,
    #         'ovulation_date': ovulation_date,
    #     }
    #     context_list.append(context)
    # return render(request, 'cycle_form.html', {'context_list': context_list})


# class CycleListView(ListView):
#     model = Cycle
#     template_name = 'cycle_form.html'
#     context_object_name = "cycles"
#
#     def get_queryset(self):
#         return self.model.objects.all()


# class DeleteCycleView(DeleteView):
#     model = Cycle
#     context_object_name = "cycle"
#     template_name = "delete_cycle.html"
#     success_url = reverse_lazy("cycle_create")
#
#     def get_object(self):
#         return get_object_or_404(Cycle, pk=self.kwargs['pk'])
#
#     def delete(self, request, *args, **kwargs):
#         self.model = self.get_object()
#         self.model.delete()
#         return HttpResponseRedirect(self.get_success_url())

    # class CycleCreateView(View):
    #
    #     def get(self, request):
    #         return render(request, 'cycle_form.html')
    #
    #     def post(self, request):
    #         my_date_fresh = request.POST.get("date")
    #         my_day_fresh = request.POST.get("day")
    #
    #         my_date_str = str(my_date_fresh)
    #         my_date = datetime.strptime(my_date_str, "%Y-%m-%d")
    #         date_list = [my_date]
    #         flow_date_list = []
    #         for i in range(1, 12):
    #             next_month = date_list[-1] + timedelta(days=30)
    #             date_list.append(next_month)
    #         context_list = []
    #         for day in date_list:
    #             ovulation_date = day + relativedelta(day=day.day // 2)
    #             ovulation_date_str = ovulation_date.strftime("%Y-%m-%d")
    #
    #
    #             fertile_dates = [m_date.strftime("%Y-%m-%d") for m_date in my_list]
    #
    #             context = {
    #                 'day': day,
    #                 'date': my_date_fresh,
    #                 'fertile_dates': fertile_dates,
    #                 'ovulation_date': ovulation_date,
    #             }
    #             context_list.append(context)
    #         return render(request, 'cycle_form.html', {'context_list': context_list})
    #
    # class CycleListView(ListView):
    #     template_name = 'cycle_list.html'
    #     context_object_name = "cycles"
    #
    #     def get_queryset(self):
    #         return Cycle.objects.all()
    #
    # class DeleteCycleView(DeleteView):
    #     model = Cycle
    #     context_object_name = "cycle"
    #     template_name = "delete_cycle.html"
    #     success_url = reverse_lazy("cycle_create")
    #
    #     def get_object(self):
    #         return get_object_or_404(Cycle, pk=self.kwargs['pk'])
    #
    #     def delete(self, request, *args, **kwargs):
    #         self.model = self.get_object()
    #         self.model.delete()
    #         return HttpResponseRedirect(self.get_success_url())
