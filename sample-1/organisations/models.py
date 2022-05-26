from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Organisation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    canonical_domain = models.CharField(max_length=255, unique=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', default="1")
    created_by = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Report(models.Model):
    organisation_id = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created = models.DateField()
    completed = models.DateField()
    cyberrisk = models.IntegerField()
    result = models.JSONField()

    def __str__(self):
        return self.organisation_id.name
