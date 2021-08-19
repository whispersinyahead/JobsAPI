from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import CustomUser


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user} {self.object_id}"


class Job(models.Model):
    company_name = models.CharField(max_length=60)
    position = models.CharField(max_length=150)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs')
    likes = GenericRelation(Like)

    def total_likes(self):
        return self.likes.count()

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


class RatingStar(models.Model):
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'
        ordering = ['-value']


class Rating(models.Model):
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Star', related_name='ratings')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='Job', related_name='ratings')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.star} - {self.job}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

