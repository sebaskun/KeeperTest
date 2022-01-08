from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Bookmark(models.Model):
	title = models.CharField(max_length=360, verbose_name="Title")
	url = models.CharField(max_length=500, verbose_name="URL")
	created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True, editable=False)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	private = models.BooleanField()

	def __str__(self):
		return f'f{self.owner.username} - {self.title}'

	class Meta:
		verbose_name = "Bookmark"
		verbose_name_plural = "Bookmarks"
