from django.contrib import admin
import rango.models


class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")
    list_filter = ['category']
    search_fields = ['title']
    # fields = ["category", "title", "url", "views"]


class CategoryAdmim(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(rango.models.Page, PageAdmin)
admin.site.register(rango.models.Category, CategoryAdmim)
admin.site.register(rango.models.UserProfile)

# admin.site.register(Category)
