from django.db import models

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
    title = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return "{}".format(self.title)

class Thread(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category)

    def __str__(self):
        return "{}".format(self.title)

class Post(models.Model):
    content_text = models.TextField() # This is the place where we are taking post.
    sent_date = models.DateTimeField(auto_now_add=True) # This is for sent time.
    change_date = models.DateTimeField(auto_now=True)  # This is for change time.
    thread = models.ForeignKey(Thread) # This is for relation of posts and threads.--uu-
    like = models.PositiveSmallIntegerField(default=0) # This is the place where we are keeping like count.
    is_reported = models.BooleanField(default=False) # This field for reporting stuff

    def __str__(self):
        return "{} thread, {}. post".format(Thread.title, self.id)