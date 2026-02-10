from django.contrib import admin
from .models import Comment, CommentLike, Notification, CommentEditHistory


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_author_name', 'content_preview', 'content_object', 'parent', 'is_approved', 'is_pinned', 'created_at')
    list_filter = ('is_approved', 'is_pinned', 'created_at', 'content_type')
    search_fields = ('content', 'author__username', 'author__email', 'guest_name')
    list_editable = ('is_approved', 'is_pinned')
    date_hierarchy = 'created_at'
    raw_id_fields = ('author', 'parent')
    readonly_fields = ('created_at', 'updated_at', 'get_thread_depth')
    
    fieldsets = (
        ('Content', {
            'fields': ('content_type', 'object_id', 'content', 'is_pinned')
        }),
        ('Author', {
            'fields': ('author', 'guest_name', 'guest_email')
        }),
        ('Threading', {
            'fields': ('parent', 'get_thread_depth')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_edited')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_author_name(self, obj):
        return obj.get_author_display_name()
    get_author_name.short_description = 'Author'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def get_thread_depth(self, obj):
        return obj.get_thread_depth()
    get_thread_depth.short_description = 'Thread Depth'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'comment__content')
    date_hierarchy = 'created_at'
    raw_id_fields = ('user', 'comment')
    readonly_fields = ('created_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'message_preview', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('recipient', 'sender', 'comment')
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected notifications as unread"


@admin.register(CommentEditHistory)
class CommentEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('comment', 'edited_by', 'edited_at', 'content_preview')
    list_filter = ('edited_at',)
    search_fields = ('comment__content', 'previous_content', 'edited_by__username')
    date_hierarchy = 'edited_at'
    raw_id_fields = ('comment', 'edited_by')
    readonly_fields = ('edited_at',)
    
    def content_preview(self, obj):
        return obj.previous_content[:50] + '...' if len(obj.previous_content) > 50 else obj.previous_content
    content_preview.short_description = 'Previous Content'
