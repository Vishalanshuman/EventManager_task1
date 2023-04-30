from django.urls import path
from .views import UserCreateView, LoginView, CreateEventView, EventRetrieveUpdateDeleteView


urlpatterns = [
    path('register/', UserCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # event
    path('v3/app/events', CreateEventView.as_view(),name='create_event'),
    path('v3/app/events/<int:id>', EventRetrieveUpdateDeleteView.as_view(),name='get_event'),


]
