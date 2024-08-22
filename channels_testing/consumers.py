from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync,sync_to_async 
from channels_testing.models import NewGroupsModel,ChatMeChatStoringModel

from channels.db import database_sync_to_async
import json
from django.contrib.sessions.models import Session
from channels.sessions import SessionMiddlewareStack


class ChatMe(AsyncConsumer):

    groupname=""
    username=''
    code=''
    user=''
    password=''

    connectedUsers={}
    liveUsersList=[]
    offlineUsersList=[]

    historicalChat=[]


    noOfActiveMembers=''


    async def websocket_connect(self,e):

        self.groupname = self.scope['url_route']['kwargs']['path']
        self.user = self.scope['url_route']['kwargs']['name']

        groupVarifying = await self.send_databases_data("user-varifying")
        nameVarifying = await self.send_databases_data("name-varifying")

        if self.groupname == groupVarifying and self.user == nameVarifying:

            await self.channel_layer.group_add(self.groupname,self.channel_name) 

            uniqueId = await self.getUniqueId()
            await self.groupAndPersonStatus(uniqueId,'PersonStatus','Live')
            await self.groupAndPersonStatus(uniqueId,'GroupStatus','status')
            await self.get_Total_No_Of_ConnectedandDisconnected_users(self.groupname,"Active users")
            
            self.connectedUsers['msg']= 'none'
            self.connectedUsers['adminRequest']= 'none'
            self.connectedUsers['requestType']= 'no of user diaplay'

            await self.channel_layer.group_send(self.groupname,{
                'type':'connecteduser.message',
                'message': json.dumps(self.connectedUsers),
            })    

            self.noOfActiveMembers=len(self.liveUsersList)
            await self.send_databases_data("activeandtotal-members-store")

            await self.get_stored_chat(self.groupname)
            await self.channel_layer.group_send(self.groupname,{
                'type':'historical.storedchat',
                'message': json.dumps({'previousData':self.historicalChat,'requestType':'Previous Chat Of Group'}),
            })    

            await self.send({
                "type": "websocket.accept",
            })

    @sync_to_async
    def getUniqueId(self):
        session=self.scope.get('session')
        mySession = session.get('newGroupData')
        return mySession['uniqueId']

    @database_sync_to_async
    def get_stored_chat(self,group):
        self.historicalChat.clear()
        try:
            messages = ChatMeChatStoringModel.objects.filter(Groups_Name=group)
        except:
            pass

        if messages != None:
            for i in messages:
                self.historicalChat.append({'name':i.Person_Name,'group':i.Groups_Name,'message':i.ChatMe_Message,'msgSequence':i.Message_Sequence})

    @database_sync_to_async
    def get_Total_No_Of_ConnectedandDisconnected_users(self,groupName,active):
        if active == 'Active users':
            self.liveUsersList.clear()
            self.offlineUsersList.clear()

            messages = NewGroupsModel.objects.filter(Groups_Name=groupName,Person_Status="Live")
            for i in messages:
                self.liveUsersList.append(i.Person_Name)
            self.connectedUsers['Yes']= self.liveUsersList
        
            messages1 = NewGroupsModel.objects.filter(Groups_Name=groupName,Person_Status="Offline")
            for i in messages1:
                self.offlineUsersList.append(i.Person_Name)
            self.connectedUsers['No']= self.offlineUsersList

        elif active == 'Offline Users':
            self.offlineUsersList.clear()
            self.liveUsersList.clear()

            messages = NewGroupsModel.objects.filter(Groups_Name=groupName,Person_Status="Offline")
            for i in messages:
                self.offlineUsersList.append(i.Person_Name)
            self.connectedUsers['No']= self.offlineUsersList

            messages1 = NewGroupsModel.objects.filter(Groups_Name=groupName,Person_Status="Live")
            for i in messages1:
                self.liveUsersList.append(i.Person_Name)
            self.connectedUsers['Yes']= self.liveUsersList

    @database_sync_to_async
    def groupAndPersonStatus(self,id,data,status):
        if data == 'PersonStatus':
            messages = NewGroupsModel.objects.filter(Unique_Id=id)
            messages.update(Person_Status=status)

        elif data == 'GroupStatus':
            if self.noOfActiveMembers != 0:
                groupStatusUpdate=NewGroupsModel.objects.filter(Groups_Name=self.groupname)
                groupStatusUpdate.update(Group_Status='Active')
            else:
                groupStatusUpdate=NewGroupsModel.objects.filter(Groups_Name=self.groupname)
                groupStatusUpdate.update(Group_Status='Stoped')

    @database_sync_to_async
    def send_databases_data(self,data):
        if data == 'user-varifying':
            messages = NewGroupsModel.objects.filter(Groups_Name=self.groupname).first()
            return messages.Groups_Name
        
        elif data == 'name-varifying':
            foundPerson=''
            messages = NewGroupsModel.objects.filter(Groups_Name=self.groupname)
            for i in messages:
                if self.user == i.Person_Name:
                    foundPerson = i.Person_Name
                    break
                else:
                    foundPerson = "none"
            return foundPerson 

        elif data == 'activeandtotal-members-store':
            activeMembers = NewGroupsModel.objects.filter(Groups_Name=self.groupname)
            activeMembers.update(No_Of_Active_Members=self.noOfActiveMembers)
            
            totalMembers = NewGroupsModel.objects.filter(Groups_Name=self.groupname)
            totalMembers.update(Total_No_Of_Person=str(totalMembers.count()))



    

        sendPermission={'HostPermission':'none','Login Status':'none',}
        messages = NewGroupsModel.objects.filter(Unique_Id=id)
        
        if messages != '':
            for i in messages:
                sendPermission["HostPermission"]=i.Host_Permissions
                sendPermission["LoginStatus"]=i.Login_Status
        
        return sendPermission
      
    @database_sync_to_async
    def chatMe_ChatStore(self,id,group,person,chat,sequence):
        lastSequence=0

        try:
            messages = ChatMeChatStoringModel.objects.filter(Groups_Name=group).last()
        except:
            pass

        if messages != None:
            lastSequence=messages.Message_Sequence
            lastSequence=int(lastSequence)+1
            saveChat = ChatMeChatStoringModel(Unique_Id=id,Groups_Name=group,Person_Name=person,ChatMe_Message=chat,Message_Sequence=lastSequence)
            saveChat.save()
        else:
            lastSequence=int(lastSequence)+1
            saveChat = ChatMeChatStoringModel(Unique_Id=id,Groups_Name=group,Person_Name=person,ChatMe_Message=chat,Message_Sequence=lastSequence)
            saveChat.save()


    async def websocket_receive(self,e):

        self.username = json.loads(e['text'])['usename']
        self.password = json.loads(e['text'])['code']

       
        if self.username != '' and self.password != '':

            groupVarifying = await self.send_databases_data("user-varifying")
            nameVarifying = await self.send_databases_data("name-varifying")

            if self.password == groupVarifying and self.username == nameVarifying:

                id=await self.getUniqueId()
                await self.chatMe_ChatStore(id,self.password,self.username,json.loads(e['text'])['msg'],0)
   
                await self.channel_layer.group_send(self.groupname,{
                    'type':'chatme.message',
                    'message': e['text'],
                })
                

    async def chatme_message(self,e):
        await self.send({
            "type": "websocket.send",
            "text": e['message'],
        })

    async def connecteduser_message(self,e):
        await self.send({
            "type": "websocket.send",
            "text": e['message'],
        })

    async def historical_storedchat(self,e):
        await self.send({
            "type": "websocket.send",
            "text": e['message'],
        })


    async def websocket_disconnect(self,e):

        groupVarifying = await self.send_databases_data("user-varifying")
        nameVarifying = await self.send_databases_data("name-varifying")

        if self.groupname == groupVarifying and self.user == nameVarifying:

            self.noOfActiveMembers=len(self.liveUsersList)
            await self.send_databases_data("activeandtotal-members-store")

            uniqueId = await self.getUniqueId()
            await self.groupAndPersonStatus(uniqueId,'PersonStatus','Offline')
            await self.groupAndPersonStatus(uniqueId,'GroupStatus','status')
            await self.get_Total_No_Of_ConnectedandDisconnected_users(self.groupname,"Offline Users")

            
            await self.channel_layer.group_send(self.groupname,{
                'type':'connecteduser.message',
                'message': json.dumps(self.connectedUsers),
            })


            if self.noOfActiveMembers == 0:
                self.liveUsersList.clear()
                self.offlineUsersList.clear()

            raise StopConsumer()




    
        
        

    
    