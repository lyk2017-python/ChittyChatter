from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

"""
 ________________________
<      Don't Panic!      >
 ------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/
    Medusa Rocks ^^
"""

class Category(models.Model):

    """We are keeping our category's titles in that model."""

    title = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(null=True,unique=True,blank=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Thread(models.Model):

    """We are using this model for keeping threads and their variables in database and
    we have a ForeignKey in here. One side of this relation connects to a category and
    other side connects to threads."""

    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    is_reported = models.BooleanField(default=False)
    slug = models.SlugField(null=True,unique=True,blank=True)
    likes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "{}".format(self.title)

class Post(models.Model):

    """We are using this model for keeping posts and their variables in database and
    we have a ForeignKey in here. One side of this relation connects to a thread and
    other side connects to posts.

    content_text provides our content's text. I think it explains himself enough.
    I'm kinda bored and i really dont know what should i write here. In next commit
    i'm gonna delete all this stuff but its a really small easter egg for later.

    Gecenin bir yarısı ne yazsam harbiden bulamadım buralara. Yarın düzelteceğim umarım.
                                                                                -g3vxy buradaydı.
    """

    content_text = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(Thread)
    like = models.PositiveSmallIntegerField(default=0)
    is_reported = models.BooleanField(default=False)
    username = models.CharField(max_length=15,null=False)

    def __str__(self):
        return "{} thread, post id = {}".format(Thread.id, self.id)

@receiver(pre_save, sender=Thread)
@receiver(pre_save, sender=Category)
def slugifier(sender, instance,*args, **kwargs):
    if hasattr(sender, "title"):
        instance.slug = slugify(instance.title)

    else:
        raise AttributeError("Slug Error")
    return instance
