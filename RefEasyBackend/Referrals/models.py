from tkinter import CASCADE
from django.db import models

from Jobs.models import Job
from Users.models import Applicant, Employee

from django.db.models.signals import post_save

# Create your models here.


class Referral(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    ref_emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    status = models.CharField(choices=(('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('In-Process', 'In-Process')), max_length=30)

    created_at = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last updated', auto_now=True)

    def __str__(self):
        return f"{self.applicant} is referred by {self.ref_emp} for {self.job}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ('-updated_at', 'applicant', 'ref_emp')
        unique_together = ('job', 'ref_emp', 'applicant')



