# /home/MiguelAeTxio/CampuStudiOnline/favorites_prototype/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse
from treebeard.mp_tree import MP_Node

class TestFolder(MP_Node):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_folders'
    )

    def get_absolute_url(self):
        return reverse('favorites_prototype:folder_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.user.username}'s Folder: {self.name}"


