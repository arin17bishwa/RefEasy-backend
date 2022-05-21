from tkinter import CASCADE
from django.db import models

from Jobs.models import Job
from Users.models import Applicant, Employee

from django.db.models.signals import post_save

# Create your models here.


class Referral(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    ref_emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    status = models.CharField(choices=(('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('In-Process', 'In-Process')), max_length=30)
    slug = models.SlugField(max_length=64, db_index=True)

    created_at = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last updated', auto_now=True)

    def __str__(self):
        return f"{self.applicant} is referred by {self.employee} for {self.job}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ('-updated_at', 'applicant', 'ref_emp')
        unique_together = ('job', 'ref_emp', 'applicant')


def post_save_referral_slug(sender, instance, created, *args, **kwargs):
    if not instance or hasattr(instance, 'dirty_flag'):
        return
    instance.slug = instance.make_slug()
    try:
        instance.dirty_flag = True
        instance.save()
    finally:
        del instance.dirty_flag

post_save.connect(post_save_referral_slug, Referral)

