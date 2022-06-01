from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync, sync_to_async

class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' % self.room_name
        print('connect')
        
        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        ## getting the order_id from 'self.room_name' and using the function 'give_order_details' from models.py
        order_fetch = Order.give_order_details(self.room_name)
        
        ## to send the data from server/backend to front end
        self.send(text_data = json.dumps({'payload': order_fetch})) 

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard) (
            self.room_group_name,
            self.channel_name
        )

    ## Receive - to call the order_status channel
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name, {
                'type': 'order_status',
                'payload': text_data
            }
        )
    
    ## order_status channel - When signal is triggered/updated then this channel will get called
    def order_status(self, event):
        print(event)
        order = json.loads(event['value'])
        self.send(text_data = json.dumps({
            'payload': order
        }))