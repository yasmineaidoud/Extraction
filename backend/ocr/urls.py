from django.urls import path
from .api import retreive_facture, upload_image,download_facture_file,download_facture_file_json

urlpatterns = [
    path("factures/", retreive_facture, name="get_factures"),
    path("upload/", upload_image, name="upload_factures"),
    path('download/', download_facture_file, name='download_facture'),
    path('downloadjson/', download_facture_file_json, name='download_facture_json')
    ]
