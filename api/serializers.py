from django.contrib.auth import get_user_model
from rest_framework import serializers

from timecontrolapp.models import TimeControl, Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class TimecontrolSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TimeControl
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']


class ProfileCreateSerializer(serializers.ModelSerializer):
    position = serializers.CharField(source='profile.position')
    company = serializers.CharField(source='profile.company', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name',
                  'position', 'company']

    def create(self, validated_data):
        print(validated_data)
        position = validated_data.pop('profile').get('position')
        company = validated_data.pop('company')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        profile = Profile.objects.create(user=user, position=position,
                                         company=company)
        return user


class TestSerializer(serializers.Serializer):
    date = serializers.DateField()

