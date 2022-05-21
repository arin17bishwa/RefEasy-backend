from tkinter import CASCADE
from django.db import models

from Jobs.models import Job
from Users.models import Applicant, Employee

from django.db.models.signals import post_save

# Create your models here.


class Referral(models.Model):
    STATUS_CHOICES = (
        ('L01', 'Level- 1'),
        ('L02', 'Level- 2'),
        ('L03', 'Level- 3'),
        ('L04', 'Level- 4'),
        ('L05', 'Level- 5'),
        ('ACC', 'Accepted'),
        ('REJ', 'Rejected'),
    )
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    ref_emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30)

    created_at = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='last updated', auto_now=True)

    def __str__(self):
        return f"{self.applicant} is referred by {self.ref_emp} for {self.job}"

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ('-updated_at', 'applicant', 'ref_emp')
        unique_together = ('job', 'ref_emp', 'applicant')



