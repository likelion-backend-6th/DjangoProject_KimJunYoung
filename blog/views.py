from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post


# Create your views here.

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 5
	template_name = 'blog/post/list.html'


def post_list(request):
	post_list = Post.published.all()
	# 페이지당 3개의 게시물로
	paginator = Paginator(post_list, 5)
	page_number = request.GET.get('page', 1)
	try:
		posts = paginator.page(page_number)
	except EmptyPage:
		# page_number가 범위를 벗어난 경우 결과릐 마지막 페이지 제공
		posts = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		# page_number가 정수가 아닌 경우 첫번째 페이지 제공
		posts = paginator.page(1)
	return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
	post = get_object_or_404(
		Post,
		status=Post.Status.PUBLISHED,
		slug=post,
		publish__year=year,
		publish__month=month,
		publish__day=day,
	)
	# 해당 포스트글에 대한 모든 활성 댓글들 가져오기 위한 쿼리셋 추가 related_name속성을 사용함
	comments = post.comments.filter(active=True)
	# 댓글폼 인스턴스 생성
	form = CommentForm()
	return render(request, 'blog/post/detail.html', {'post': post,
													 'comments': comments,
													 'form': form})


def post_share(request, post_id):
	# id로 글 검색
	post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
	sent = False
	if request.method == 'POST':
		# 폼이 제출되었음
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# 폼 필드 유효한지 검사후
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f"{cd['name']} 님이 {post.title}을(를) 추천합니다."
			message = f"{post.title}을(를) {post_url}에서 읽어보세요.\n\n" \
					  f"{cd['name']}의 의견 : {cd['comments']}"
			send_mail(subject, message, 'jklo0220@gmail.com', [cd['to']])

			# sent = True
		print(post.get_absolute_url())
		return redirect(post.get_absolute_url())
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


# 댓글 뷰 (request POST 만 받음)
@require_POST
def post_comment(request, post_id):
	post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
	comment = None
	form = CommentForm(data=request.POST)
	if form.is_valid():
		# commit=False를 사용하면 db에 저장하지 않고 Comment객체를 생성함
		comment = form.save(commit=False)
		# 댓글에 게시물 할당
		comment.post = post
		# DB저장
		comment.save()
	return render(
		request,
		'blog/post/comment.html',
		{'post': post,
		 'form': form,
		 'comment': comment
		 }
	)



