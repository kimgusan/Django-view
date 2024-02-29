from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Member
from post.models import Post, PostFile


class PostWriteView(View):
    def get(self, request):
        return render(request, 'post/write.html')

    @transaction.atomic
    def post(self, request):
        data = request.POST
        # input 태그 하나 당 파일 1개 일 때
        file = request.FILES
        # input 태그 하나에 여러 파일일 때 (multiple), getlist('{input태그 name 값}')
        # files = request.FILES.getlist('upload-file')

        member = Member(**request.session['member'])

        data = {
            'post_title': data['post-title'],
            'post_content': data['post-content'],
            'member': member
        }

        post = Post.objects.create(**data)

        #input 태그의 name 값이 key 이다.
        for key in file:
            PostFile.objects.create(post=post, path=file[key])

        return redirect(post.get_absolute_url())

class PostDetailView(View):
    def get(self, request):

        post = Post.objects.get(id=request.GET['id'])

        post.post_view_count += 1
        post.save(update_fields=['post_view_count'])

        context = {
            'post': post,
            'post_files': list(post.postfile_set.all())
        }
        return render(request, 'post/detail.html', context)

    # 위에 강사님 코드는 쿼리 스트링으로 id 값을 가져오기 때문에 별도로 post_id 값을 전달받지 않았음
    # def get(self, request, post_id):
    #     post = Post.objects.get(id=post_id)
    #
    #     post.post_view_count += 1
    #     post.save(update_fields=['post_view_count'])
    #
    #     context = {
    #         'post': post
    #     }
    #
    #     return render(request, 'post/detail.html', context)


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
        return render(request, 'post/list.html')

class PostListAPI(APIView):
    # 페이징 처리
    def get(self, request, page):
        row_count = 5

        offset = (page - 1) * row_count
        limit = page * row_count
        columns = [
            'id',
            'post_title',
            'post_content',
            'post_view_count',
            'member_name'
        ]
        posts = Post.enabled_objects.annotate(member_name=F('member__member_name')).values(*columns)[offset:limit]

        has_next = Post.enabled_objects.filter()[limit:limit + 1].exists()

        post_info = {
            'posts': posts,
            'hasNext': has_next
        }

        return Response(post_info)


