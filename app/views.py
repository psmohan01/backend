from django.shortcuts import render

# Create your views here.
from .serializers import ContactSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CareerApplication



@api_view(['POST'])
def contact_api(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "Contact saved"})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def career_apply(request):
    CareerApplication.objects.create(
        name=request.POST.get('name'),
        email=request.POST.get('email'),
        position=request.POST.get('position'),
        message=request.POST.get('message'),
        resume=request.FILES.get('resume')
    )
    return Response({
        "message": "Application submitted successfully"
    })
