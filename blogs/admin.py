from django.contrib import admin
from .models import Post,Comment

# Register your models here.
# admin.site.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','is_pinned','score', 'create_time')
    list_link = ('id','title')
    search_fields = ('title','create_time')
    list_per_page = 25

    exclude = ('author','create_time','update_time')
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'detail', 'create_time')

    list_link = ('id','title')
    list_per_page = 25
    exclude = ('author','create_time','update_time')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)