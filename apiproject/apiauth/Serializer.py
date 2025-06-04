from rest_framework import serializers
from .models import Auth

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = [
            "id",
            "titre",
            "artiste",
            "date_de_production",
            "nombre_de_pistes",
            "duree_en_minutes"
        ]