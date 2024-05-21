from applibrary.models import *
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.views import APIView


class BookSerializer(ModelSerializer):
    category_name = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'name', 'author_name', 'category_name', 'book_published_date', 'stock', 'published']

    def get_category_name(self, obj):
        return obj.category.name

    def get_author_name(self, obj):
        return obj.author.name


class ReserveSerializer(ModelSerializer):
    class Meta:
        model = Reserve
        fields = '__all__'
        read_only_fields = ['user']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserIdentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserIdent
        fields = ['full_name', 'personal_number', 'birth_date', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user_ident = UserIdent.objects.create(user=user, **validated_data)
            return user_ident
        else:
            raise serializers.ValidationError(user_serializer.errors)


class Get10PopularBookSerializer(serializers.ModelSerializer):
    lease_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'category', 'book_published_date', 'stock', 'lease_count']