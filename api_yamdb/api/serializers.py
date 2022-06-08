from urllib import request
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Comment, Review, User


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSlugSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class TitleGeneralSerializer(serializers.ModelSerializer):

    category = CategorySerializer(required=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(
        source='reviews_title__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = TitleGeneralSerializer(many=False, read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Review
        fields = ['id', 'title', 'author', 'text', 'score', 'pub_date']

    def validate(self, data):
        if self.context['view'].action == 'create':
            author = self.context['request'].user
            title = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                    title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Отзыв уже есть')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    review = ReviewSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date', 'review']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        lookup_field = 'username'
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
        # read_only_fields = ('role',)

    def validate_email(self, email):
        if self.context['view'].action == 'create':
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'E-mail уже используется')
        return email

    def patch(self, validated_data):
        if self.context['role'] == User.USER:
            profile_data = validated_data.pop('role')
            user = User.objects.create(**validated_data)
            User.objects.create(user=user, **profile_data)
        return user
        
        
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, username):
        if self.context.get('username') == username:
            raise serializers.ValidationError(
                'username уже используется')
        if username == 'me':
            raise serializers.ValidationError(
                'Регистрация с таким username запрещена')
        return username


# class AdminSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'bio',
#             'role'
#         )
#         lookup_field = 'username'
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=User.objects.all(),
#                 fields=['username', 'email']
#             )
#         ]

#     def validate_email(self, email):
#         if self.context['view'].action == 'create':
#             if User.objects.filter(email=email).exists():
#                 raise serializers.ValidationError(
#                     'E-mail уже используется')
#         return email
