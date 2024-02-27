from django.urls import path, include

from post.views import PostWriteView, PostDetailView, PostUpdateView, PostDeleteView, PostListView

app_name = 'post'

urlpatterns = [
    path('write/', PostWriteView.as_view(), name='write'),
    path('detail/<int:post_id>/', PostDetailView.as_view(), name='detail'),
    path('update/<int:post_id>/', PostUpdateView.as_view(), name='update'),
    path('delete/<int:post_id>/', PostDeleteView.as_view(), name='delete'),
    path('list/', PostListView.as_view(), name='list')
]
