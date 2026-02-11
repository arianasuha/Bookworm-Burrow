from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Genre, Book, ReviewPost, Reaction, Comment

# --- CUSTOM USER ADMIN ---
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for the custom email-based User model."""
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']

    # fieldsets controls the "Edit User" page layout
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'image_url', 'slug')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # add_fieldsets controls the "Add User" page layout
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')


# --- GENRE ADMIN WITH APPROVAL ACTION ---
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved', 'slug')
    list_filter = ('is_approved',)
    search_fields = ('name',)
    actions = ['approve_genres']

    def approve_genres(self, request, queryset):
        queryset.update(is_approved=True)
    approve_genres.short_description = "Approve selected genres"


# --- BOOK ADMIN ---
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug')
    search_fields = ('title', 'author')
    # Helps you filter books by genre quickly
    list_filter = ('genres',)


# --- REVIEW POST ADMIN ---
@admin.register(ReviewPost)
class ReviewPostAdmin(admin.ModelAdmin):
    list_display = ('review_title', 'book', 'reviewer', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    # Use double underscore (__) to search fields in related models
    search_fields = ('review_title', 'book__title', 'reviewer__email')
    readonly_fields = ('slug', 'review_date')


# --- SIMPLE REGISTRATIONS FOR INTERACTIONS ---
admin.site.register(Reaction)
admin.site.register(Comment)