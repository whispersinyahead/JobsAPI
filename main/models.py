from django.db import models

from account.models import CustomUser


class Job(models.Model):
    company_name = models.CharField(max_length=60)
    position = models.CharField(max_length=150)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return self.position


class CodeImage(models.Model):
    image = models.ImageField(upload_to='images')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body

    class Meta:
        ordering = ('-created', )