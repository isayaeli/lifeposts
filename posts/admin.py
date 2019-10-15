from django.contrib import admin
from posts.models import Post,Comment

admin.site.site_header = "Lifebook Admin"

admin.site.register(Post)
admin.site.register(Comment)
