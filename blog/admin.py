from django.contrib import admin
from .models import Article, Category, IPAddress, Ads

# Admin header change
admin.site.site_header = "وبلاگ جنگویی من"

# Register your models here.


def make_published(ModelAdmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = "منتشر شد."
    else:
        message_bit = "منتشر شدند."
    ModelAdmin.message_user(
        request, " {} مقاله {}".format(rows_updated, message_bit))


make_published.short_description = "انتشار مقالات منتخب شده"


def make_draft(ModelAdmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "بیش نویس شد."
    else:
        message_bit = "بیش نویس شدند."
    ModelAdmin.message_user(
        request, " {} مقاله {}".format(rows_updated, message_bit))


make_draft.short_description = "بیش نویس مقالات منتخب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'author',
                    'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'is_special', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ['status', '-publish']
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
admin.site.register(IPAddress)
admin.site.register(Ads)
