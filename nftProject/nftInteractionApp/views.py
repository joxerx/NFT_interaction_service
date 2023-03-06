import random
import string

from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TokenSerializer
from .models import Token

from .connection import Connection


class TokenListAPIView(APIView):
    """Show tokens list, saved in database"""
    def get(self, request):
        tokens = Token.objects.all()
        return Response(TokenSerializer(tokens, many=True).data)


class TokenTotalSupplyAPIView(APIView):
    """Get tokens total supply at blockchain using contract's method"""
    def get(self, request):
        total_supply = Connection.contract_instance.functions.totalSupply().call()
        return Response({'result': total_supply})
        # TODO: add connection check and connection retries if failed
        # TODO: if connection unavailable after 10 retries rise exception


class TokenCreateAPI(APIView):
    """Allows you to create new NFT token at eth blockchain using Mint method.
    You should check the owner's address before minting"""
    def post(self, request):
        rand_string = ''.join(random.choice(string.digits + string.ascii_letters) for letter in range(20))

        request.data['tx_hash'] = rand_string
        request.data['unique_hash'] = rand_string

        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        txn_hash = Connection.send_transaction(Connection(),
            owner=request.data['owner'],
            unique_hash=request.data['unique_hash'],
            media_url=request.data['media_url']
        )

        data = {'tx_hash': txn_hash.hex()}
        instance = serializer.save()
        serializer = TokenSerializer(instance, data=data, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)
