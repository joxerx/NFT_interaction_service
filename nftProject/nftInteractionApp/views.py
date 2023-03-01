from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import TokenSerializer

from .models import Token


class TokenAPIViewList(APIView):
    def get(self, request):
        tokens = Token.objects.all()
        return Response(TokenSerializer(tokens, many=True).data)