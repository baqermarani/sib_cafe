from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('personal_id', 'full_name', 'email', 'phone_number', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
                personal_id=validated_data['personal_id'],
                email=validated_data['email'],
                full_name=validated_data['full_name'],
                phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, value):
        if value.lower() == 'admin':
            raise serializers.ValidationError('Username cannot be admin')
        return value


class UserLoginSerializer(serializers.Serializer):

    personal_id = serializers.CharField(max_length=8)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        personal_id = data['personal_id']
        password = data['password']
        user = authenticate(personal_id=personal_id, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'full_name': user.full_name,
                'personal_id': user.personal_id,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
