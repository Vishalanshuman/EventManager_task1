from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .models import Event
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import generics, status, mixins
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer, LoginSerializer, EventSerializer

# Create your views here.

class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def post(self, request:Request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'message':'Register successfully',
                'data':serializer.data
            }
            return Response(data= serializer.data, status= status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request:Request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(data={"message":"Login successfully."}, status=status.HTTP_200_OK)
        return Response(data={'message':'Invalid Username or Password'}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request:Request):
        response = {
            'user':str(request.user),
            'auth':str(request.auth)
        }
        return Response(data=response, status=status.HTTP_200_OK)
    

class CreateEventView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    def get_queryset(self):
        queryset = Event.objects.all()
        event_id = self.request.query_params.get('id')
        event_type = self.request.query_params.get('type')

        if event_id:
            queryset = queryset.filter(id=event_id)
        elif event_type:
            queryset = queryset.filter(type=event_type)

        return queryset

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self,request:Request, *args, **kwargs):
        serializer  = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner = request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventRetrieveUpdateDeleteView(generics.GenericAPIView):
    serializer_class=EventSerializer
    permission_classes=[IsAuthenticated]
    def get(self,request:Request, *args, **kwargs):
        event = Event.objects.get(id=kwargs.get('id'))
        serializer = self.serializer_class(event, many=False)
        if serializer:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        response = {
                "message":"Event is not found for this id."
            }
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    def put(self, request:Request, *args,**kwargs):
        event = Event.objects.get(id=kwargs.get('id'))
        if event:
            serializer = self.serializer_class(event, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(owner = request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
                "message":"Event is not found for this id."
            }
        return Response(data=response, status=status.HTTP_200_OK)

    def delete(self, request:Request, *args,**kwargs):
        event = Event.objects.get(id=kwargs.get('id'))
        if event:
            event.delete()
            return Response(data={'message':'Event deleted successfully.'}, status=status.HTTP_200_OK)
        return Response(data={'message':'Event is not found for this id.'}, status=status.HTTP_400_BAD_REQUEST) 


class CustomPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 5

class EventTypeView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    pagination_class=[CustomPagination]

    def get(self, request:Request, *args, **kwargs):
        events = Event.objects.filter(type=Q(kwargs.get('type')))
        serializer = self.serializer_class(events, many=True)
        if serializer:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={'message':'Quering type is not found.'}, status=status.HTTP_404_NOT_FOUND)
    

# class EventListView(generics.ListAPIView):
#     serializer_class = EventSerializer

#     def get_queryset(self):
#         type_param = self.request.query_params.get('type')
#         queryset = Event.objects.all()
#         if type_param:
#             queryset = queryset.filter(type=type_param)
#         return queryset