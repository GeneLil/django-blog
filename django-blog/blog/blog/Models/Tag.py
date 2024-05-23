"""Module for tag model"""
from django.db import models


class Tag(models.Model):
    """Class for tag model"""
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def get_tag_title(tag: Tag):
    """Getting tag title from tag"""
    return Tag.objects.get(id=tag.pk).title
