from django.contrib import admin

from news.models import User_profile, News, Author, Category, Likes

admin.site.register(User_profile)
admin.site.register(News)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Likes)