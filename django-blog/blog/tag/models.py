from django.db import models


class Tag(models.Model):
    """Class for tag model"""
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def get_tag_title(tag: Tag):
    """Getting tag title from tag"""
    return Tag.objects.get(id=tag.pk).title

def get_tags_titles(tags):
    """Getting list of tags titles"""
    tags_titles = []
    for tag in tags.all():
        tags_titles.append(get_tag_title(tag))
    return tags_titles