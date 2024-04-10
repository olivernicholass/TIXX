from django.core.management.base import BaseCommand
from tixx.models import Ticket 
import sys

class Command(BaseCommand):
    help = 'Import tickets into the database'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='Event ID')
        parser.add_argument('arena_id', type=str, help='Arena ID')


    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        arena_id = kwargs['arena_id']
        
        data = []
        for s in range(1, 5):
            
            if s == 1 or s == 3:
                for j in range(1, 11):
                    letter = chr(j + ord('A') - 1)
                    for i in range(1, 51): 
                        data.append({
                            'eventId': event_id,
                            'seatNum': f'S{s}{letter}{i}',
                            'arenaId': arena_id,  
                            'ticketQR': 'x', 
                            'ticketPrice': 100,
                            'ticketType': 'normal', 
                            'zone': s, 
                            'available': True,
                        })
            
            if s == 2 or s == 4:
                for j in range(1, 21):
                    letter = chr(j + ord('A') - 1)
                    for i in range(1, 11):
                        data.append({
                            'eventId': event_id,
                            'seatNum': f'S{s}{letter}{i}',
                            'arenaId': arena_id, 
                            'ticketQR': 'x', 
                            'ticketPrice': 100, 
                            'ticketType': 'normal',
                            'zone': s, 
                            'available': True,
                        })
            
       
        for item in data:
            ticket = Ticket.objects.create(
                eventId_id=item['eventId'],
                seatNum=item['seatNum'],
                arenaId_id=item['arenaId'],
                ticketQR=item['ticketQR'],
                ticketPrice=item['ticketPrice'],
                ticketType=item['ticketType'],
                zone=item['zone'],
                available=item['available']
            )
            ticket.save()