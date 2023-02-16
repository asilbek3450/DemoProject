from rest_framework import serializers

from core.utility import check_email_or_phone
from .models import User, UserConfirmation, VIA_PHONE, VIA_EMAIL
from shared.utils import phone_parser, send_email, send_phone_notification


class SignUpSerializer(serializers.ModelSerializer):
	
	guid = serializers.UUIDField(read_only=True)
	
	def __init__(self, *args, **kwargs):
		super(SignUpSerializer, self).__init__(*args, **kwargs)
		self.fields['email_phone'] = serializers.CharField(required=False)
	
	class Meta:
		model = User
		fields = (
			'guid',
			'auth_type',
			'auth_status',
		)
		extra_kwargs = {
			'auth_type': {'read_only': True, 'required': False},
			'auth_status': {'read_only': True, 'required': False},
		}
	
	def create(self, validated_data):
		user = super(SignUpSerializer, self).create(validated_data)
		print(user)
		if user.auth_type == VIA_EMAIL:
			code = user.create_verify_code(user.auth_type)
			print(code)
			send_email(user.email, code)
			print("email sending..")
		elif user.auth_type == VIA_PHONE:
			code = user.create_verify_code(user.auth_type)
			send_email(user.email, code)
		# send_phone_notification(user.phone_number, code)
		user.save()
		return user
	
	def validate(self, attrs):
		super(SignUpSerializer, self).validate(attrs)
		clear_data = self.auth_validate(attrs)
		return clear_data
	
	@staticmethod
	def auth_validate(attr):
		user_input = str(attr.get('email_phone')).lower()
		print(user_input)
		input_type = check_email_or_phone(user_input)
		if input_type == 'email':
			data = {
				'email': user_input,
				'auth_type': VIA_EMAIL,
			}
		elif input_type == 'phone':
			data = {
				'phone': attr.get('email_phone'),
				'auth_type': VIA_PHONE,
			}
		elif input_type is None:
			data = {
				'success': False,
				'message': 'You must send email or phone number',
			}
			raise serializers.ValidationError(data)
		else:
			data = {
				'success': False,
				'message': 'Must send email or phone number',
			}
			raise serializers.ValidationError(data)
		# data.update(password=attr.get('password'))
		return data
	
	def validate_email_phone(self, value):
		value = value.lower()
		
		if value and User.objects.filter(email=value).exists():
			data = {
				'success': False,
				'message': 'Email already exists',
			}
			raise serializers.ValidationError(data)
		
		if check_email_or_phone(value) == 'phone':
			if User.objects.filter(phone=value).exists():
				data = {
					'success': False,
					'message': 'Phone number already exists',
				}
				raise serializers.ValidationError(data)
			
		if check_email_or_phone(value) == "phone":  # 998991234567
			phone_parser(value, self.initial_data.get("country_code"))
		return value

	def to_representation(self, instance):
		data = super(SignUpSerializer, self).to_representation(instance)
		data.update(instance.tokens())
		return data
	