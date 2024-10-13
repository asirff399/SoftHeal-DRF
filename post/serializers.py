from rest_framework import serializers
from .models import Post,PostType,Donation

class PostSerializer(serializers.ModelSerializer):
    post_type = serializers.SlugRelatedField(slug_field='name', queryset=PostType.objects.all())

    class Meta:
        model = Post
        fields = ['id','name','description','image','target','collected','post_type','created_on',]
        read_only_fields = ['id','created_on',]

class DonationSerializer(serializers.ModelSerializer):
    post_name = serializers.CharField(source='post.name', read_only=True)
    post_image = serializers.CharField(source='post.image', read_only=True)
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Donation
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = '__all__'