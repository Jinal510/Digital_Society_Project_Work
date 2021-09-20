from django.contrib import admin
from .models import *
# Register your models here.

class ChairmanAdmin(admin.ModelAdmin):
    list_display=('firstname','lastname','contact','city','work')
    list_display_links=("firstname",)
    list_editable=('city','work')
    list_per_page=5
    search_fields=('firstname',)
    list_filter=('city','work')

class MembersAdmin(admin.ModelAdmin):
    list_display=('firstname','lastname','contact','city','work')
    list_display_links=("firstname",)
    list_editable=('city','work')
    list_per_page=5
    search_fields=('firstname',)
    list_filter=('city','work')

class WatchmanAdmin(admin.ModelAdmin):
    list_display=('firstname','lastname','contact','city','work')
    list_display_links=("firstname",)
    list_editable=('city','work')
    list_per_page=5
    search_fields=('firstname',)
    list_filter=('city','work')

admin.site.register(User)
admin.site.register(Chairman,ChairmanAdmin)
admin.site.register(Members,MembersAdmin)
admin.site.register(Watchman,WatchmanAdmin)
admin.site.register(Myfamily)
admin.site.register(EditMyfamily)
admin.site.register(Events)
admin.site.register(Complain)
admin.site.register(Suggestions)
admin.site.register(Vistiors)
admin.site.register(NoticeBoard)
admin.site.register(Transaction)
admin.site.register(Rent)
admin.site.register(ChatBoard)

