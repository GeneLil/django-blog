from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
    
    

def get_tag_title(tag: Tag):
        return Tag.objects.get(id=tag.pk).title