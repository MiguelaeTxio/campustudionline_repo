# /home/MiguelAeTxio/CampuStudiOnline/favorites_prototype/admin.py
from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import TestFolder

class TestFolderAdmin(TreeAdmin):
    form = movenodeform_factory(TestFolder)

admin.site.register(TestFolder, TestFolderAdmin)
