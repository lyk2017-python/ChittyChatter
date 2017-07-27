from django.contrib import admin
from forum.models import Category, Thread, Post

class ThreadInline(admin.TabularInline):
    model = Thread
    extra = 0

class PostInline(admin.TabularInline):
    model = Post
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'title']
    search_fields = ['title']
    list_display_links = ['id', 'title']
    inlines = [ThreadInline]

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_reported', 'category']
    list_display_links = ['id', 'title', 'is_reported', 'category']
    search_fields = ['title', 'is_reported', 'category']
    list_filter = ['title', 'is_reported']
    inlines = [PostInline]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_text', 'sent_date','change_date', 'like', 'is_reported', 'thread']
    list_display_links = ['id', 'content_text', 'sent_date', 'change_date', 'like', 'is_reported', 'thread']
    list_filter = ['sent_date', 'like', 'is_reported']
    search_fields = ['thread', 'is_reported']
    fieldsets = [
        (
            "Bilgiler",
            {
                "fields": [
                    'content_text',
                    'thread',
                    ('like', 'is_reported'),
            ]
        },
    )
]



