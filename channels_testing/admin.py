from django.contrib import admin
from .models import NewGroupsModel,ChatMeChatStoringModel


class NewGroupsAdmin(admin.ModelAdmin):
    list_display=['Unique_Id','Groups_Name','Person_Name','Group_Host','Total_No_Of_Person','No_Of_Active_Members','Group_Status','Person_Status']

class ChatMeChatStoreAdmin(admin.ModelAdmin):
    list_display=['Unique_Id','Groups_Name','Person_Name','ChatMe_Message','Message_Sequence']


admin.site.register(NewGroupsModel,NewGroupsAdmin)
admin.site.register(ChatMeChatStoringModel,ChatMeChatStoreAdmin)
