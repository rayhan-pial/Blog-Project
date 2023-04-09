from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Blog,Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
    

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(BlogSerializer, self).to_representation(instance)
        representation['total_word_of_description'] = len(instance.description.split())
        summery = instance.description.split('.')[0:2]
        representation['summery'] = f"{'.'.join(summery)} ....."
        return representation
