from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from member.models import Member
from post.models import Post


class PostWriteView(View):
    def get(self, request):
        return render(request, 'post/write.html')

    @transaction.atomic
    def post(self, request):
        data = request.POST

        member = Member(**request.session['member'])

        data = {
            'post_title': data['post-title'],
            'post_content': data['post-content'],
            'member': member
        }

        post = Post.objects.create(**data)

        return redirect(post.get_absolute_url())

class PostDetailView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        post.post_view_count += 1
        post.save(update_fields=['post_view_count'])

        context = {
            'post': post
        }

        return render(request, 'post/detail.html', context)


class PostUpdateView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        context = {
            'post': post
        }

        return render(request, 'post/update.html', context)

    def post(self,request, post_id):
        data=request.POST

        data= {
            'post_title': data['post-title'],
            'post_content': data['post-content'],
        }

        post = Post.objects.get(id=post_id)
        post.post_title = data['post_title']
        post.post_content = data['post_content']
        # post.save(update_fields=['post_title', 'post_content'])
        post.save()

        return redirect(post.get_absolute_url())



class PostDeleteView(View):
    @transaction.atomic
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        post.delete()
        return redirect('/post/list')

# 강사님이 쿼리 스트링으로 값을 받아오는 코드
# class PostDeteteView(View):
#     def get(self, request):
#         Post.objects.filter(id=request.GET['id']).update(post_status=False)
#         # post = Post.objects.get(id=request.GET['id'])
#         # post.status = False
#         # post.save(update_fields=['status'])

class PostListView(View):
    def get(self, request):
        # 페이징 처리
        row_count = 5
        page = request.GET.get('page')
        if page is None:
            page = 1

        offset = (page -1) * row_count
        limit= page * row_count

        posts = Post.enabled_objects.all()[offset:limit]
        return render(request, 'post/list.html',{'posts': posts})