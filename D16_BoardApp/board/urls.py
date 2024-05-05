from django.urls import path
from .views import (
    AdvertisementListView,
    CreateAdvertisementView,
    AdvertisementDetailView,
    AdvertisementEditView,
    AdvertisementDeleteView,
    PrivateResponsesView,
    AcceptResponseView,
    ResponseDeleteView
)

urlpatterns = [
    path('advertisements/', AdvertisementListView.as_view(), name='advertisements_list'),
    path('advertisements/create/', CreateAdvertisementView.as_view(), name='create_advertisement'),
    path('advertisements/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('advertisements/<int:pk>/edit/', AdvertisementEditView.as_view(), name='advertisement_edit'),
    path('advertisements/<int:pk>/delete/', AdvertisementDeleteView.as_view(), name='advertisement_delete'),
    path('responses/', PrivateResponsesView.as_view(), name='responses_list'),
    path('accept_response/', AcceptResponseView.as_view(), name='accept_response'),
    path('responses/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
]
