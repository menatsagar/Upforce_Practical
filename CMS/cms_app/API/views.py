from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from cms_app.models import User, Post, Like
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from cms_app.API.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    PostSerializer, 
    PostCreateSerializer, 
    PostUpdateSerializer,
    LikeSerializer,
    LikeCreateSerializer,
    LikeUpdateSerializer
   
)

from rest_framework.parsers import MultiPartParser , JSONParser
from rest_framework.pagination import PageNumberPagination




class UserAPIView(APIView):

    def get_object(self, pk):
        try:
           user =  User.objects.get(pk = pk)
           return user        
        except User.DoesNotExist:
              raise Http404
    def get(self,request, id):
        
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):    
        
        serializer = UserCreateSerializer( data= request.data)       
        if serializer.is_valid():
            serializer.save()
            return Response( {'message':'User Created Successfully'},status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,id):
        user = self.get_object(id)
        serializer = UserUpdateSerializer(user,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User Info updated successfully'},status=status.HTTP_202_ACCEPTED)
       
        return Response(serializer.errors,status = status.HTTP_304_NOT_MODIFIED)            

    def delete(self,request,id):
        try:
            user = self.get_object(id)
            user.delete()
            return Response({'message':'User Deleted Successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist :
            return Response({'message':'User not found'},status = status.HTTP_400_BAD_REQUEST)

  


class PostAPIView(APIView):
   
    def get_object(self, pk):
        try:
           post =  Post.objects.get(pk = pk)
           return post        
        except Post.DoesNotExist:
              raise Http404
    def get(self,request, id):
        
        post = self.get_object(id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
         
        serializer = PostCreateSerializer( data= request.data)

        if serializer.is_valid():
                serializer.save()
                return Response({'message':'Post has been Created Successfully'},status = status.HTTP_201_CREATED)
           
     
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,post_id, user_id):
        post = self.get_object(post_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e :
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        if post.owner == user:
            serializer = PostUpdateSerializer(post,data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Post has been Updated Successfully'}, status=status.HTTP_202_ACCEPTED)
        
            return Response(serializer.errors,status = status.HTTP_304_NOT_MODIFIED)            
        return Response({'message':'You can not update others post'}, status=status.HTTP_200_OK)
        
    def delete(self, request,post_id, user_id):
        try:
            post = self.get_object(id)
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist as e :
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
            if post.owner == user:
                post.delete()
                return Response({'message':'Post has been Deleted Successfully'},status = status.HTTP_200_OK)
        except Post.DoesNotExist as e :
            return Response(e, status=status.HTTP_200_OK)


class LikeAPIView(APIView):
    def get_object(self, pk):
        try:
           like =  Like.objects.get(pk = pk)
           return like        
        except Like.DoesNotExist:
              raise Http404
    def get(self,request, id):
        
        like = self.get_object(id)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
         
        serializer = LikeCreateSerializer( data= request.data)

        if serializer.is_valid():
                serializer.save()
                return Response({'message':'Like Created'},status = status.HTTP_201_CREATED)
           
     
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,id):
        like = self.get_object(id)
        serializer = LikeUpdateSerializer(like, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'like Updated'}, status=status.HTTP_202_ACCEPTED)
       
        return Response(serializer.errors,status = status.HTTP_304_NOT_MODIFIED)            

    def delete(self,request,id):
        try:
            like = self.get_object(id)
            like.delete()
            return Response({'message':'like Deleted'},status = status.HTTP_200_OK)
        except Like.DoesNotExist as e :
            return Response(e, status=status.HTTP_200_OK)
        
        
class GetPostsListAPI(APIView):

       
    def get(self,request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as e:
            user = None

        public_post_list  = Post.objects.filter(is_public=True)
        if user:
            user_private_posts = Post.objects.filter(is_public=False, owner=user) 
            post_list = public_post_list | user_private_posts
        else:

            post_list = public_post_list
        serializer = PostSerializer(post_list, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)