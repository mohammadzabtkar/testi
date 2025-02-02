import asyncio

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from task.models import Task
from courier.models import Courier

from django.db.models.signals import post_save
from django.dispatch import receiver
from task.models import Task

def assign_courier_to_task(task_id, courier_id):
    """ اختصاص یک Courier به یک Task و ارسال آپدیت به WebSocket """
    task = Task.objects.get(id=task_id)
    courier = Courier.objects.get(id=courier_id)

    task.courier = courier
    task.save()

    # ارسال پیام به WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "task_updates",
        {
            "type": "send_task_update",
            "data": {
                "task_id": task.id,
                "courier_id": courier.id,
                "message": f"Task {task.id} assigned to Courier {courier.id}"
            }
        }
    )




@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:  # فقط وقتی تسک ایجاد می‌شود
        # فرض می‌کنیم که می‌خواهی کویری به تسک اختصاص بدهی
        assign_courier_to_task(instance.id, instance.courier.id)

@receiver(post_save, sender=Task)
def notify_change(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    asyncio.run(channel_layer.group_send(
        "your_group_name",
        {"type": "your_event_name", "message": "پیک تغییر کرد"}
    ))



def update_task_in_admin(task_id, courier_id):
    # مثلاً اساین کردن courier به task در ادمین پنل
    task = Task.objects.get(id=task_id)
    task.courier = courier_id
    task.save()

    # ارسال پیام به WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'task_task_room',  # نام گروه WebSocket
        {
            'type': 'send_task_update',  # نام تابع در consumer
            'message': f'Task {task_id} updated with courier {courier_id}'
        }
    )
