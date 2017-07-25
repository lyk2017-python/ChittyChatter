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

"""

class Post(models.Model):
    post_title = models.CharField(max_length=50) # Medusa rocks. ^^
    post_text = models.TextField() # This is the place where we are taking post.
    post_stime = models.DateTimeField(auto_now_add=True) # This is for sent time.
    post_ctime = models.DateTimeField()  # This is for change time.
    post_thread = models.ManyToOneRel() # This is for relation of posts and threads.
    post_like = models.PositiveSmallIntegerField() # This is the place where we are keeping like count.
    post_is_reported = models.BooleanField(default=False) # This field for reporting stuff.