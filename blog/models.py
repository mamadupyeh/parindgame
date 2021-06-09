from django.db import models
from django.urls import reverse
from account.models import User
from django.utils.html import format_html
from django.utils import timezone
from extensions.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


# Create your models here.

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="ادرس ایبی")


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='childen', verbose_name="عبارت زیر دسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name="ادرس دسته بندی")
    status = models.BooleanField(
        default=True, verbose_name="ایا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="بوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title

    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'بیش نویس'),
        ('p', 'منتشر شده'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                               related_name='articels', verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=100, unique=True,
                            verbose_name="ادرس مقاله")
    category = models.ManyToManyField(
        Category, verbose_name="دسته بندی", related_name="articels")
    description = models.TextField(verbose_name="محتوای مقاله")
    thumbnail = models.ImageField(
        upload_to="images", verbose_name="تصویر مقاله")
    publish = models.DateTimeField(
        default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(
        default=False, verbose_name="مقاله ویژه")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(
        IPAddress, through="ArticleHite", blank=True, related_name="hits", verbose_name="بازدید ها")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:home")

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width=60 height=60 style='border-radius: 5px;' src='{}'>".format(self.thumbnail.url))
    thumbnail_tag.short_description = "عکس مقاله"

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"

    objects = ArticleManager()


class ArticleHite(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class AdsManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Ads(models.Model):
    STATUS_CHOICES = (
        ('d', 'بیش نویس'),
        ('p', 'منتشر شده'),

    )
    thumbnail = models.ImageField(
        upload_to="images", verbose_name="تصویر تبلیغ")
    publish = models.DateTimeField(
        default=timezone.now, verbose_name="زمان انتشار")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")
    adsss = AdsManager()
