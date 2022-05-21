import shortuuid
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, pre_save
from django.db import models
from .utils import get_group_name

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False, max_length=32)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=(('HR', 'HR'), ('NHR', 'Non-HR'), ('APP', 'Applicant')), max_length=5)
    referral_link = models.CharField(max_length=64, blank=True)
    eligible = models.BooleanField(default=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    def make_referral_link(self):
        email_initial = str(self.email).split('@')[0]
        return f'{email_initial}-{self.uuid}'

    def __str__(self):
        return f"({self.email},{self.uuid})"


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(choices=(('HR', 'HR'), ('NHR', 'Non-HR'), ('APP', 'Applicant')), max_length=5)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    def __str__(self):
        return f'{self.user}'


def post_save_userGroup(sender, instance, created, *args, **kwargs):
    if created and not instance.groups.exists():
        if instance.is_superuser:
            group_name = 'HR'
        else:
            group_name = get_group_name(instance.email)
        group, created = Group.objects.get_or_create(name=group_name)
        instance.groups.add(group)


def pre_save_employee_trial(sender, instance, *args, **kwargs):
    if not instance.referral_link:
        instance.referral_link = instance.make_referral_link()


post_save.connect(post_save_userGroup, sender=User)
pre_save.connect(pre_save_employee_trial, sender=Employee)
