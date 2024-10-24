from django.urls import path
from .views import EventCreateView, EventDetailView, EventListView, ParticipantCreateView, EventDeleteView

urlpatterns = [
    path('', EventCreateView.as_view(), name='event_create'),
    path('my-page/', EventListView.as_view(), name='my_page'),
    path('event/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('event/<slug:slug>/participate/', ParticipantCreateView.as_view(), name='event_participate'),
    path('event/<slug:slug>/delete/', EventDeleteView.as_view(), name="event_delete"),
]