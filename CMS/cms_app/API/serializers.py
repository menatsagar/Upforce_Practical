# django imports
import re

from django.conf import settings
from rest_framework import serializers
from cms_app.models import User, Post, Like
from dataclasses import field

class UserSerializer(serializers.ModelSerializer):
    user_total_posts = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "name", "email", "password", "user_total_posts"]

    def get_user_total_posts(self,obj):
        return obj.user_all_posts.count()

class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=60, required=True)
    name = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=128, required=True)
    
    def validate_email(self, value):
        """
        Check if the email address is already in use by another user.
        """
        if settings.ENABLE_VALIDATIONS:
            if not re.match(settings.EMAIL_REGEX, value):
                raise serializers.ValidationError("Invalid E-mail address format.")
        return value

    def validate_password(self, value):
        """
        Check if the password meets the complexity requirements.
        """
        if settings.ENABLE_VALIDATIONS:
            if not re.match(settings.PASSWORD_REGEX, value):
                raise serializers.ValidationError(
                    "Password must contain atleast 8 char, 1 uppercase letter, 1 lowercase letter, 1 digit and 1 special char."
                )
        return value
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_password(self, value):
        """
        Check if the password meets the complexity requirements.
        """
        if settings.ENABLE_VALIDATIONS:
           
            if not re.match(settings.PASSWORD_REGEX, value):
                raise serializers.ValidationError(
                    "Password must contain atleast 8 char, 1 uppercase letter, 1 lowercase letter, 1 digit and 1 special char."
                )
        return value
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    
    owner = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field='name', many=False)
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model = Post    
        fields = ['id', 'title','owner','description','content', 'is_public', 'total_likes'] 
    def get_total_likes(self, obj):
        return obj.likes_on_post.count()
    

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields ='__all__' 
   

class PostUpdateSerializer(serializers.ModelSerializer):
        
        class Meta:
            model=Post
            fields = ['title','description','content', 'is_public']  

class LikeSerializer(serializers.ModelSerializer):
    
    user = serializers.SlugRelatedField(queryset = User.objects.all(), slug_field='name', many=False)
    post = serializers.SlugRelatedField(queryset = Post.objects.all(), slug_field='title', many=False)
    
    class Meta:
        model = Like    
        fields = ['id', 'user', 'post'] 
    

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields ='__all__' 
   

class LikeUpdateSerializer(serializers.ModelSerializer):
        
        class Meta:
            model=Like
            fields = ['title','description','content', 'is_public']  

