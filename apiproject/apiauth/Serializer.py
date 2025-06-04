from rest_framework import serializers
from .models import CustomUser

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "nom",
            "prenom",
            "date_creation",
            "dernier_login",
            "role"
        ]