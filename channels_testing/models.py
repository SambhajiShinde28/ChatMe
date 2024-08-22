from django.db import models

class NewGroupsModel(models.Model):
    Unique_Id=models.TextField()
    Groups_Name=models.TextField()
    Person_Name=models.TextField()
    Group_Host=models.TextField()
    Total_No_Of_Person=models.TextField()
    No_Of_Active_Members=models.TextField()
    Group_Status=models.TextField()
    Person_Status=models.TextField()

class ChatMeChatStoringModel(models.Model):
    Unique_Id=models.TextField()
    Groups_Name=models.TextField()
    Person_Name=models.TextField()
    ChatMe_Message=models.TextField()
    Message_Sequence=models.TextField()


