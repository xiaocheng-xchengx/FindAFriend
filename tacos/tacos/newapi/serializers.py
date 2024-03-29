from django.contrib.auth.models import User
from rest_framework import serializers
from findafriend.models import Page, UserProfile, Chat 
from rest_framework.serializers import ( CharField, EmailField, HyperlinkedIdentityField,
    SerializerMethodField, ValidationError )
from django.contrib.auth.validators import UnicodeUsernameValidator

from rest_framework_jwt.settings import api_settings

from datetime import datetime


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserProfile
		fields = ('user', 'first_name', 'last_name', 'university', 'hometown', 'picture')


class UserSerializer(serializers.HyperlinkedModelSerializer):
	profile = ProfileSerializer(many=True)
	
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups', 'profile')



class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	email = EmailField(label='Email Address', write_only=True)
	email2 = EmailField(label='Confirm Email', write_only=True)

	class Meta:
	    model = User
	    fields = ['username','email','email2','password', 'token']
	    extra_kwargs = {"password": {"write_only": True} }

	def validate(self, data):
	    return data

	def validate_email(self, value):
	    data = self.get_initial()
	    email1 = data.get("email2")
	    email2 = value
	    if email1 != email2:
	        raise ValidationError("The emails do not match.")
	    user_qs = User.objects.filter(email=email2)
	    if user_qs.exists():
	        raise ValidationError("This user has already registered.")
	    return value

	def validate_email2(self, value):
	    data = self.get_initial()
	    email1 = data.get("email")
	    email2 = value
	    if email1 != email2:
	        raise ValidationError("The emails do not match.")
	    return value

	def create(self, validated_data):
	    username = validated_data['username']
	    email = validated_data['email']
	    password = validated_data['password']
	    user_obj = User(
	            username = username,
	            email = email
	        )
	    user_obj.set_password(password)
	    # send email activation
	    user_obj.save()
	    payload = jwt_payload_handler(user_obj)
	    token = jwt_encode_handler(payload) 
	    validated_data['token'] = token
	    return validated_data

class UserLoginSerializer(serializers.HyperlinkedModelSerializer):
	token = CharField(allow_blank=True, read_only=True)
	username = CharField()

	class Meta:
	    model = User
	    fields = ['username','password', 'token']
	    extra_kwargs = {"password": {"write_only": True} }

	def validate(self, data):
	    # only validate the username
	    username = data['username']
	    password = data['password']
	    # check username against user model (2 separate querysets)
	    user_a = User.objects.filter(username__iexact=username)
	    user_b = User.objects.filter(email__iexact=username)
	    # here we join both querysets (pipeline in django)
	    user_qs = (user_a | user_b).distinct()
	    if user_qs.exists() and user_qs.count() == 1:
	        user_obj = user_qs.first() # User.objetcs.get(id=1) ...
	        # check the password against the user
	        # check the raw password against the hashed password in DB
	        # WE DONT WANT TO STORE THE RAW PASSWORD ANYWHERE
	        password_passes = user_obj.check_password(password)
	        if not user_obj.is_active:
	            raise ValidationError("This user is inactive.")
	        # HTTPS
	        if password_passes:
	            # here we should do something with the token
	            data['username'] = user_obj.username
	            # data['email'] = user_obj.email
	            payload = jwt_payload_handler(user_obj)
	            token = jwt_encode_handler(payload) 
	            data['token'] = token
	            return data
	    raise ValidationError("Invalid Credentials")


class PageSerializer(serializers.HyperlinkedModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    creator = serializers.CharField(source='creator.username')
    class Meta:
            model = Page
            fields = ('title', 'creator', 'description', 'timeCreated', 'members', 'typeOfGroup')


class PageCreateSerializer(serializers.HyperlinkedModelSerializer):
    # In our json, creator is username instead of foreign key
    creator = serializers.CharField()
    
    class Meta:
            model = Page
            fields = ('title', 'creator', 'description', 'typeOfGroup')


    def create(self, validated_data):
        currentTime = str(datetime.now())
        # For example: "2011-05-03 17:45:35.177000"
        currentTime = currentTime[:16]
        # "2011-05-03 17:45:35" Django requires the space to be "T"
        currentTime = currentTime.replace(' ', 'T')
        page_obj = Page(
                title = validated_data['title'],
                creator = User.objects.get( username = validated_data['creator'] ),
                description = validated_data['description'],
                timeCreated = currentTime,
                typeOfGroup = validated_data['typeOfGroup']
            )
        page_obj.save()
        # Find the user in our database, and add the user to the "members" of the newly created object
        page_obj.members.add(User.objects.get( username = validated_data['creator'] ))
        return validated_data


class PageTitleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Page
		fields = ('title', 'members')

class UserToUsernameSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'url')

class ChatSerializer(serializers.HyperlinkedModelSerializer):
	sender = UserToUsernameSerializer()
	recipient = PageTitleSerializer()
	class Meta:
		model = Chat
		fields = ('sender', 'recipient', 'messageContent', 'timestamp')

