import re

from rest_framework.exceptions import ValidationError

email_regex = re.compile(
	r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@(["r"-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
phone_regex = re.compile(r'^998[0-9]{9}$')  # 998999999999


def check_email_or_phone(value):
	if re.fullmatch(email_regex, value):
		email_or_phone = "email"
	elif re.fullmatch(phone_regex, value):
		email_or_phone = "phone"
	else:
		data = {
			"success": False,
			'message': "Email yuki telefon raqamingiz notog'ri"
		}
		raise ValidationError(data)
	
	return email_or_phone
