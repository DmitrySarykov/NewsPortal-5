from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .filters import SearchFilter 
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from datetime import datetime

from .models import *
 
class NewsList(ListView):
    model = Post  
    template_name = 'news_list.html' 
    context_object_name = 'news_list'
    ordering = ['-date']
    paginate_by = 10
    queryset = Post.objects.order_by('-date') 

class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.add_post', )

class NewsDetailView(DetailView):
    model = Post  
    template_name = 'news_detail.html' 
    context_object_name = 'news'

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news_edit.html'
    form_class = PostForm
    permission_required = ('news.change_post', )
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'news'
    permission_required = ('news.delete_post', )

class SearchListView(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())
        return context

class CategoryView(DetailView):
    model = Category  
    template_name = 'category_detail.html' 
    context_object_name = 'category'


class SubscribeView(View):
    def get(self, request, *args, **kwargs):
        category=Category.objects.get(pk=kwargs['pk'])
        user = request.user
        category.subscribers.add(user)
    
        return redirect('category_detail',category.pk)
    # отправляем письмо
    # send_mail( 
    #     subject=f'Новый подписчик',
    #     message=f'Пользователь {user.username} подписался на категорию {category}', 
    #     from_email=None,
    #     recipient_list=[user.email]
    # )  
    

        