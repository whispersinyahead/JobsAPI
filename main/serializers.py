from rest_framework import serializers

from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image', )


class JobSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Job
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ImageSerializer(instance.images.all(), many=True).data
        action = self.context.get('action')
        if action == 'list':
            representation.pop('description')
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        job = Job.objects.create(author=request.user, **validated_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, job=job)
        return job

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, job=instance)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(
            author=request.user, **validated_data
        )
        return comment