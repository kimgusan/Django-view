from django.db import models

from member.models import Member
from post.managers import PostManager


class Post(models.Model):
    post_title = models.CharField(max_length=50, null=False, blank=False)
    post_content = models.CharField(max_length=50, null=False, blank=False)
    post_view_count = models.BigIntegerField(default=0, null=False, blank=False)
    post_status = models.BooleanField(default=True)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)

    objects = models.Manager()
    enabled_objects = PostManager()

    class Meta:
        db_table = 'tbl_post'
        ordering = ['-id']


    # 게시글 상세보기
    def get_absolute_url(self):
        return f'/post/detail/?id={self.id}'

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, null=False, blank=False)
    # image path
    path = models.ImageField(upload_to='post/%Y/%m/%d', null=False, blank=False)

    class Meta:
        db_table = 'tbl_post_file'