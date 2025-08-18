from django.test import TestCase

from .models import Comment


def setUp(self):
    self.comment = Comment.objects.create(text='This is comment')
