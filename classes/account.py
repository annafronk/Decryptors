from TAScheduler.models import User as UserModel, PublicInfo, PrivateInfo
from typing import Dict


def create_account(data: Dict[str, any]):
    if __has_required_fields(data) and get_user_model(data.get('email')) is None:
        new_user_model = UserModel.objects.create(
            email=data.get('email'),
            password=data.get('password'),
            account_type=data.get('account_type')
        )

        PublicInfo.objects.create(
            user_id=new_user_model,
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )

        PrivateInfo.objects.create(
            user_id=new_user_model
        )

        return Account(new_user_model)
    else:
        return None


def delete_account(user_id):
    try:
        user_delete = UserModel.objects.get(id=user_id)
        user_delete.delete()
        return True
    except UserModel.DoesNotExist:
        return False


def edit_account(user_id, data: Dict[str, any]):
    try:
        user = UserModel.objects.get(id=user_id)
        account = Account(user)
        account.set_first_name(data.get('first_name', account.get_first_name()))
        account.set_last_name(data.get('last_name', account.get_last_name()))
        account.set_address(data.get('address', account.get_address()))
        account.set_phone_number(data.get('phone_number', account.get_phone_number()))
        account.set_office_hours(data.get('office_hours', account.get_office_hours()))
        account.user_model.save()
        account.public_info_model.save()
        account.private_info_model.save()
        return account
    except UserModel.DoesNotExist:
        return None


def __has_required_fields(data: Dict[str, any]):
    required_fields = {"email", "password", "account_type", "first_name", "last_name"}
    return required_fields.issubset(data.keys())


def valid_login(email_attempt: str, password_attempt: str):
    user = get_user_model(email_attempt)
    if user is not None and user.password == password_attempt:
        return True
    else:
        return False


def get_user_model(email_attempt):
    try:
        user = UserModel.objects.get(email=email_attempt)
        return user
    except UserModel.DoesNotExist:
        return None


def get_account(email_attempt):
    try:
        user_model = UserModel.objects.get(email=email_attempt)
        account = Account(user_model)
        return account
    except UserModel.DoesNotExist:
        return None


def get_account_by_id(user_id):
    try:
        user_model = UserModel.objects.get(id=user_id)
        account = Account(user_model)
        return account
    except UserModel.DoesNotExist:
        return None


def account_list():
    accounts = UserModel.objects.all()
    account_objects = [Account(user_model) for user_model in accounts]
    return account_objects


class Account:
    def __init__(self, user_model: UserModel):
        self.user_model = user_model
        self.public_info_model = PublicInfo.objects.get(user_id=user_model)
        self.private_info_model = PrivateInfo.objects.get(user_id=user_model)

    def get_email(self):
        return self.user_model.email

    def get_office_hours(self):
        return self.public_info_model.office_hours

    def set_office_hours(self, new_office_hours):
        self.public_info_model.office_hours = new_office_hours
        self.public_info_model.save()

    def get_first_name(self):
        return self.public_info_model.first_name

    def set_first_name(self, new_first_name):
        self.public_info_model.first_name = new_first_name
        self.public_info_model.save()

    def get_last_name(self):
        return self.public_info_model.last_name

    def set_last_name(self, new_last_name):
        self.public_info_model.last_name = new_last_name
        self.public_info_model.save()

    def get_address(self):
        return self.private_info_model.address

    def set_address(self, new_address):
        self.private_info_model.address = new_address
        self.private_info_model.save()

    def get_phone_number(self):
        return self.private_info_model.phone_number

    def set_phone_number(self, new_phone_number):
        self.private_info_model.phone_number = new_phone_number
        self.private_info_model.save()

    def get_primary_key(self):
        return self.user_model.pk

    def get_account_type(self):
        return self.user_model.account_type
