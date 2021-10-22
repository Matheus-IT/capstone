from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Queue
import json


class QueueConsumer(AsyncWebsocketConsumer):
	GROUP_NAME = 'awaiting_queue'

	async def handle_add_user_to_channel_group(self, received_group_name):	
		# Accept just users who are trying to connect to the right
		# room name, to avoid cross site forgery
		if received_group_name == self.GROUP_NAME:
			await self.channel_layer.group_add(
				self.GROUP_NAME,
				self.channel_name
			)

			return True
		else:
			return False


	async def connect(self):
		try:
			received_group_name = self.scope['url_route']['kwargs']['group_name']
			user_was_added = await self.handle_add_user_to_channel_group(received_group_name)
			
			if user_was_added:
				print(f'Success! Connected to {self.GROUP_NAME}')
			else:
				print('Fail! User trying to connect to a different room name')
				await self.close()
				return
			
			await self.accept()

			queue = await self.get_queue()
			print(queue)
			await self.send(text_data=json.dumps({
				'queueSize': queue.num_of_people
			}))
		except Exception as e:
			print(e)


	@database_sync_to_async
	def get_queue(self):
		try:
			queue =  Queue.objects.all()[0]
			if queue:
				return queue
		except IndexError:
			return Queue.objects.create(num_of_people=0)
	

	@database_sync_to_async
	def save_queue(self, queueObj):
		return queueObj.save()


	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		print(text_data_json['queue_size'])

		try:
			queue = await self.get_queue()
			old_queue_size = queue.num_of_people
			queue.num_of_people = text_data_json['queue_size']

			if old_queue_size < queue.num_of_people:
				print('Queue has became bigger')
				has_increased = True
			else:
				print('Queue has became smaller')
				has_increased = False
			
			await self.channel_layer.group_send(
				self.GROUP_NAME,
				{
					'type': 'send_queue_info_to_client',
					'has_the_queue_increased': has_increased
				}
			)

			await self.save_queue(queue)
		except Exception as e:
			print(e)


	async def send_queue_info_to_client(self, event):
		await self.send(
			text_data=json.dumps({
				'hasTheQueueIncreased': event['has_the_queue_increased']
			})
		)

	
	async def disconnect(self, close_code):
		pass
