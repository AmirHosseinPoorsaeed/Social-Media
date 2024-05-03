from django.contrib import admin
from django.utils.safestring import mark_safe

from social.blog.models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'owner', 'count_likes', 'datetime_created',)
    readonly_fields = ('image_preview',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        CommentInline,
    ]

    @admin.display(description='Image')
    def image_preview(self, post: Post):
        return mark_safe(f'<img src="{post.image.url}" width="150" height="100" />')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'count_likes', 'datetime_created',)
