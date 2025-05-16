import os
from django.http import FileResponse, JsonResponse

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

import cv2
import numpy as np
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .add_to_database import image_to_database
from .models import Facture, Produit
from .serializers import FactureSerializer


@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_image(request):
    image_file = request.FILES.get("image")
    if not image_file:
        return JsonResponse({"error": "No image file provided"}, status=400)
    try:
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        cv_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if cv_image is None:
            return JsonResponse({"error": "Could not decode image"}, status=400)
        facture_data, products = image_to_database(cv_image)
        return JsonResponse({"facture_data": facture_data, "products": products}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["GET"])
def retreive_facture(request):
    facture = Facture.objects.all()
    serializer = FactureSerializer(facture, many=True)
    return JsonResponse({"facture": serializer.data, "success": True}, status=200, safe=False)

@api_view(["GET"])
def download_facture_file(request):
    app_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(app_dir, 'facture_resultss.csv')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='facture_resultss.csv')
        return response
    else:
        return JsonResponse({"error": "File not found", "success": False}, status=404)
    
@api_view(["GET"])
def download_facture_file_json(request):
    app_dir = os.path.dirname(os.path.abspath(__file__)) 
    file_path = os.path.join(app_dir, 'facture_resultss.json')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename='facture_resultss.json')
        return response
    else:
        return JsonResponse({"error": "File not found", "success": False}, status=404)