from django.contrib.auth.models import User
from rest_framework import generics,exceptions,status
from rest_framework.response import Response
from .serializers import UserSerializer,BlogSerializer,CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .models import Blog,Category
from .quey import filter_by_author,filter_by_category,filter_by_date,filter_by_tags

class RegisterView(generics.CreateAPIView):
    def post(self, request):
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Please provide username, email, and password'})

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            return Response({'error': str(e)})

        return Response(UserSerializer(user).data)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, **kwargs):
        data = self.queryset.all()
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)

class CategoryListView(generics.ListCreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BlogListView(generics.ListCreateAPIView,generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes= [IsAuthenticated]

    lookup_field = 'id'
    
    def get(self, request, **kwargs):
        params = self.request.query_params
        date = params.get("date") 
        author = params.get("author")
        category = params.get("category")
        tags = params.get("tags")

        data = self.queryset.filter(filter_by_author(author),filter_by_category(category),filter_by_tags(tags),filter_by_date(date))

        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)


    def post(self, request):
        data = request.data.copy()
        data["author"] = self.request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        curent_user = self.request.user
        data = request.data.copy()

        if not curent_user == instance.author:
            raise exceptions.PermissionDenied()
        
        serializer = self.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        curent_user = self.request.user

        if not curent_user == instance.author:
            raise exceptions.PermissionDenied()
    
        instance.delete()
        
        return Response(status=status.HTTP_200_OK)