from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# create a account model and manager to handle custom user model

class MyAccountManager(BaseUserManager):
    #to create normal user
    def create_user(self,first_name,last_name,username,email,phone_number,password=None):
        if not email:
            raise ValueError('User must have an Email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name= first_name,
            last_name = last_name,
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #to create superuser
    def create_superuser(self,first_name,last_name,email,username,phone_number,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.IntegerField()

    #required fields for creating custom user model
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login  = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #set login field of admin page, to login with email
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True






