from django.contrib import admin
from .models import Post

# Register your models here.
# admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','is_pinned', 'create_time')
    list_link = ('id','title')
    search_fields = ('title','create_time')
    list_per_page = 25

admin.site.register(Post, PostAdmin)