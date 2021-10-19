from rest_framework import serializers

from users.models import Profile
from projects.models import Project, Review, Tag


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = serializers.StringRelatedField(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
    
    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['value']