import uuid
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.db import models
from .utils import get_group_name


# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=(('HR', 'HR'), ('NHR', 'Non-HR'), ('APP', 'Applicant')), max_length=5)
    referral_link = models.CharField(max_length=64, blank=True)
    eligible = models.BooleanField(default=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    def get_referral_link(self):
        joined_name = ''.join(map(lambda x: x.title(), str(self.user.name).split(' ')))
        return f'{joined_name}-{self.uuid}'

    def __str__(self):
        return f"({self.user.name},{self.uuid},{self.email})"


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=(('HR', 'HR'), ('NHR', 'Non-HR'), ('APP', 'Applicant')), max_length=5)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    def __str__(self):
        return f'{self.user}'


def post_save_userGroup(sender, instance, *args, **kwargs):
    if not instance.groups.exists():
        if instance.is_superuser:
            group_name = 'HR'
        else:
            group_name = get_group_name(instance.email)
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


post_save.connect(post_save_userGroup, sender=User)
