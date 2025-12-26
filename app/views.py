from django.shortcuts import render

# Create your views here.
from .serializers import ContactSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CareerApplication
from rest_framework import status
from .serializers import CareerApplicationSerializer


@api_view(['POST'])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Contact saved"})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def career_apply(request):
    serializer = CareerApplicationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Application submitted successfully"},
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

