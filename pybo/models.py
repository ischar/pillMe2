from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, userId, userName, userPhoneNumber, password=None, ):
        user = self.model(
            userId=userId,
            userName=userName,
            userPhoneNumber=userPhoneNumber,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, userId, userName, userPhoneNumber, password=None, ):
        user = self.create_user(
            userId=userId,
            # userPassword=userPassword,
            userName=userName,
            userPhoneNumber=userPhoneNumber,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(
        max_length = 25,
        unique=True,
    )
    userName = models.CharField(max_length=25, null=False)
    userPhoneNumber = models.CharField(max_length=25, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['userName','userPhoneNumber']

    def __str__(self):
        return self.get_email_field_name
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin



class Friend(models.Model):
    userId = models.CharField(max_length=25, null=False)
    userName = models.CharField(max_length=25, null=False)
    userFriend = models.CharField(max_length=25, null=False)
    userFriendId = models.CharField(max_length=25, null=False)