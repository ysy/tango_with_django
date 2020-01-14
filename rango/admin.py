from django.contrib import admin

#from rango import models
#from rango import models

import rango.models

class PageAdmin(admin.ModelAdmin):
    fields = ["category", "title", "url", "views"]

admin.site.register(rango.models.Page, PageAdmin)
admin.site.register(rango.models.Category)
#admin.site.register(Category)
