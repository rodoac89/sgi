import os
import json
from channels.generic.websocket import WebsocketConsumer
from .utils import decryptAES, getCurrentTimestamp
from asgiref.sync import async_to_sync
from apps.activity.models import Session, Workstation


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        enc = self.scope["url_route"]["kwargs"]["enc"] # obtener workstation encriptada desde url
        workstation = decryptAES(enc, os.getenv("WS_SECRET"))
        print("Intento de conexión desde la estación de trabajo " + workstation)
        if (workstation == "iamadmin"): # Conexión desde dashboard
            self.room_group_name = "labs"
            self.workstation = None
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)            
            self.accept() 
        else:
            if Workstation.objects.filter(name=workstation).exists():
                self.workstation = workstation   
                self.room_group_name = "labs"   
                async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
                self.accept()
            else:
                print(f"Conexión denegada para estación de trabajo {workstation} inexistente.")
                self.close()

            

    def disconnect(self, _):
        if self.room_group_name is not None and self.workstation is not None:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "workstation.disconnect",
                    "workstation": self.workstation
                },
            )
            async_to_sync(self.channel_layer.group_discard)("labs", self.channel_name)


    def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "alive":
            session = Session.objects.filter(workstation__name=self.workstation).order_by("start").last()
            if session is None:
                return
            if session.end is None:
                session.alive = getCurrentTimestamp()
                session.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "workstation.alive",
                    "workstation": self.workstation
                },
            )
        if data["type"] == "end":
            session = Session.objects.filter(workstation__name=self.workstation).order_by("start").last()
            session.end = getCurrentTimestamp()
            session.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "workstation.end",
                    "workstation": self.workstation
                },
            )

    def workstation_alive(self, event):
        self.send(text_data=json.dumps({
            "workstation": event["workstation"],
            "type": "alive"
        }))

    def workstation_end(self, event):
        self.send(text_data=json.dumps({
            "workstation": event["workstation"],
            "type": "end"
        }))

    def workstation_disconnect(self, event):
        self.send(text_data=json.dumps({
            "workstation": event["workstation"],
            "type": "disconnect"
        }))