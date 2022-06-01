from collections import UserList
from email import message
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import JsonResponse
import string
import random
import json
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

## Pizza's model
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='home/pizza_uploaded_images', default="")

    ## dunder function of pizza's model - It will show items' name in admin panel
    def __str__(self):
        return self.name
    
## random string generator
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    print(''.join(random.choice(chars) for _ in range(size)))
    return ''.join(random.choice(chars) for _ in range(size))

## choices - first element in tuple will be shown to the use on front end
## First element is assigned to model and 2nd element is for human readable form.
CHOICES = (
    ("Order received", "Order received"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Order delivered", "Order delivered")
)

## Order's model
class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, default='')
    amount = models.IntegerField(default=100)
    status = models.CharField(max_length=100, choices = CHOICES, default = "Order Received")
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not len(self.order_id):
            self.order_id = random_string_generator()
        super(Order, self).save(*args, **kwargs)

    ## dunder function of order's model
    def __str__(self):
        return self.order_id

    @staticmethod
    ## This function will give us all the details using order_id
    def give_order_details(order_id):
        instance = Order.objects.filter(order_id = order_id).first()
        data = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status
        
        ## To change the progress bar - 5 choices, each divided into 20%
        progress_percentage = 0
        if instance.status == 'Order received':
            progress_percentage = 20
        if instance.status == 'Baking':
            progress_percentage = 40
        if instance.status == 'Baked':
            progress_percentage = 60
        if instance.status == 'Out for delivery':
            progress_percentage = 80
        if instance.status == 'Order delivered':
            progress_percentage = 100
        data['progress'] = progress_percentage
        
        return data

## Creating signals to call the order_status channel
@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        data = {}
        data['order_id'] = instance.order_id
        data['amount'] = instance.amount
        data['status'] = instance.status
        
        ## To change the progress bar - 5 choices, each divided into 20%
        progress_percentage = 0
        if instance.status == 'Order received':
            progress_percentage = 20
        if instance.status == 'Baking':
            progress_percentage = 40
        if instance.status == 'Baked':
            progress_percentage = 60
        if instance.status == 'Out for delivery':
            progress_percentage = 80
        if instance.status == 'Order delivered':
            progress_percentage = 100
        data['progress'] = progress_percentage

        ## calling signal using async_to_sync which will call the channel 'order_status' in consumers.py
        async_to_sync(channel_layer.group_send) (
            'order_%s' % instance.order_id, {
                'type': 'order_status',
                'value': json.dumps(data)
            }
        )