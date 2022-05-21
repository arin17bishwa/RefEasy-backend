from django.db import models
from django.db.models.signals import post_save, pre_save


# Create your models here.

class Job(models.Model):
    DEPT_CHOICES = (
        ('HR', 'Human Resources'),
        ('ITS', 'IT'),
        ('FIN', 'Finances'),
        ('ENG', 'Engineering')
    )
    LOC_CHOICES = (
        ('IN-BAN', 'Bangalore, India'),
        ('US-TXS', 'Texas, USA'),
        ('KR-SEO', 'Seoul, South Korea')
    )
    POS_CHOICES = (
        ('INT', 'Intern'),
        ('FTE', 'Full-time')
    )
    title = models.CharField(max_length=64)
    department = models.CharField(max_length=5, choices=DEPT_CHOICES)
    location = models.CharField(max_length=16, choices=LOC_CHOICES)
    position_type = models.CharField(max_length=3, choices=POS_CHOICES)
    is_open = models.BooleanField(default=True)
    description = models.TextField()
    slug = models.SlugField(max_length=64, db_index=True, blank=True)
    last_edit = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def make_slug(self):
        return f"{self.id:08}"

    def __str__(self):
        return f"({self.title}, {self.department}, {self.location})"

    def __repr__(self):
        return self.__str__()

    class Meta:
        ordering = ('-last_edit', 'department', 'location')
        unique_together = ('title', 'department', 'location', 'position_type')


def post_save_job_slug(sender, instance, created, *args, **kwargs):
    if not instance or hasattr(instance, 'dirty_flag'):
        return
    instance.slug = instance.make_slug()
    try:
        instance.dirty_flag = True
        instance.save()
    finally:
        del instance.dirty_flag


post_save.connect(post_save_job_slug, Job)
