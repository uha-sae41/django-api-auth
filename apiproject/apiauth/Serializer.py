from rest_framework import serializers
from .models import CustomUser

class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "password",
            "nom",
            "prenom",
            "date_creation",
            "dernier_login",
            "role"
        ]

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            nom=validated_data.get('nom', ''),
            prenom=validated_data.get('prenom', ''),
            role=validated_data.get('role', 'client')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user