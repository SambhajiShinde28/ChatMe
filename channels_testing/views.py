from django.shortcuts import render
from channels_testing.models import NewGroupsModel
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import secrets
import string

from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async,async_to_sync
import json


hostGroupName=''
hostPersonName=''
permitionPerson='NotPermited'


def HomeApp(req):
    return render(req,"index.html")


def generate_random_alphanumeric(length):
    alphabet = string.ascii_letters + string.digits
    data= ''.join(secrets.choice(alphabet) for _ in range(length))
    return data


def GroupData(req):

    global hostGroupName
    global hostPersonName
    global permitionPerson

    result="None"

    userTypeData=req.POST.get('user-type')

    if userTypeData == 'New-Group':
        userName=req.POST.get('user-name')
        groupName=generate_random_alphanumeric(60)
        group=NewGroupsModel.objects.filter(Groups_Name=groupName).first()

        uniqueId=generate_random_alphanumeric(70)
        uniqueIdSearch=NewGroupsModel.objects.filter(Unique_Id=uniqueId).first()

        if NewGroupsModel.objects.count() == 0 or group == None and uniqueIdSearch == None:
            if userName != "":

                saveGroupName = NewGroupsModel(Unique_Id=uniqueId,Groups_Name=groupName, Person_Name=userName,Group_Host='Host',Person_Status='Live',Group_Status='Active')
                saveGroupName.save()

                req.session['newGroupData']={
                    'userName': userName,
                    'groupName': groupName,
                    'groupStatus':"Active",
                    'groupHost':'Host',
                    'personStatus':'Live',
                    'uniqueId':uniqueId
                }

                result="Completed9f8"
            else:
                result="EmptyFieldsj78n"

        else:
            GroupData()

    elif userTypeData == 'Existing-Group':

        joinUserName=req.POST.get('join-user-name')
        joinGroupCode=req.POST.get('meeting-code')

        if joinUserName != '' and joinGroupCode != '':
            
            joinGroup=NewGroupsModel.objects.filter(Groups_Name=joinGroupCode).first()

            uniqueId=generate_random_alphanumeric(70)
            uniqueIdSearch=NewGroupsModel.objects.filter(Unique_Id=uniqueId).first()
            
            if NewGroupsModel.objects.count() == 0 or joinGroup != None and uniqueIdSearch == None:

                saveGroupName = NewGroupsModel(Unique_Id=uniqueId,Groups_Name=joinGroupCode, Person_Name=joinUserName, Group_Host='Member',Person_Status='Live',Group_Status='Active')
                saveGroupName.save()

                req.session['newGroupData']={
                    'userName': joinUserName,
                    'groupName': joinGroupCode,
                    'groupStatus':"Active",
                    'groupHost':'member',
                    'personStatus':'Live',
                    'uniqueId':uniqueId,
                }
               
                result="Completed9f8"
            
            else:
                result="CodeFailj9z39e"


        else:
            result="EmptyFieldsj78n"

    else:
        result="Failhs93n"
    
    return JsonResponse({'result': result})


def LiveChatApp(req):
    varifyingUser=req.session['newGroupData']
    return render(req,"meet.html",{'userName':varifyingUser['userName'], 'groupName':varifyingUser['groupName']})


