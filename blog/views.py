from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .forms import EmailPostForm
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
	return render(request, 'blog/post/detail.html', {'post': post})


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

