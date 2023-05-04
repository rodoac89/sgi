import json
from channels.generic.websocket import WebsocketConsumer
from .utils import decryptAES, validateWorkstationByRegex
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        enc = self.scope["url_route"]["kwargs"]["enc"]
        dec = decryptAES(enc, "gUkXp2s5v8y/B?E(G+KbPeShVmYq3t6w")
        if (dec == "iamadmin"):
            self.room_group_name = "labs"
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)            
            self.accept()
        elif (validateWorkstationByRegex(dec)):
            self.room_group_name = "labs"    
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
            self.accept()
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "workstation.handshake",
                "workstation": dec,
                "channel": self.channel_name
            },
        )
        else:            
            self.close()
        

    def disconnect(self, _):
        async_to_sync(self.channel_layer.group_discard)("labs", self.channel_name)

    def receive(self, text_data):
        pass

    def workstation_handshake(self, event):
        self.send(text_data=json.dumps({
            "workstation": event["workstation"],
            "channel": event["channel"]
        }))