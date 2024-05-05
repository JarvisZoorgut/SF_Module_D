from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail
from django.contrib import messages

from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm
from .filters import ResponseFilter


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'board/advertisements_list.html'
    context_object_name = 'advertisements'
    ordering = '-created_at'
    paginate_by = 4


class CreateAdvertisementView(CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/create_advertisement.html'
    success_url = reverse_lazy('advertisement_detail')

    def get_success_url(self):
        return reverse_lazy('advertisement_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AdvertisementDetailView(FormMixin, DetailView):
    model = Advertisement
    template_name = 'board/advertisement_detail.html'
    form_class = ResponseForm

    def get_success_url(self):
        return reverse_lazy('advertisement_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = self.object
            response.user = request.user
            response.save()
            messages.success(request, 'Отклик успешно отправлен!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AdvertisementEditView(UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/edit_advertisement.html'

    def get_success_url(self):
        return reverse_lazy('advertisement_detail', kwargs={'pk': self.object.pk})
    

class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    template_name = 'board/delete_advertisement.html'
    success_url = reverse_lazy('advertisements_list')


class PrivateResponsesView(ListView):
    model = Response
    template_name = 'board/responses_list.html'
    context_object_name = 'responses'
    # paginate_by = 10

    def get_queryset(self):
        queryset = Response.objects.all()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        return self.filterset.qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class AcceptResponseView(View):
    def post(self, request):
        response_id = request.POST.get('response_id')
        response = get_object_or_404(Response, pk=response_id)
        if response.advertisement.creator == request.user:
            # Помечаем отклик как принятый
            response.accepted = True
            response.save()
        return redirect('responses_list')

class ResponseDeleteView(DeleteView):
    model = Response
    success_url = reverse_lazy('responses_list')