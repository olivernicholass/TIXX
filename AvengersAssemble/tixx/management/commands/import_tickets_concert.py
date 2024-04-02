from django.core.management.base import BaseCommand
from tixx.models import Ticket  # Import your Ticket model
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
            for j in range(1, 26):
                letter = chr(j + ord('A') - 1)
                for i in range(1, 26):  # Assuming you want to create 50 tickets
                    data.append({
                        'eventId': event_id,  # Assuming eventId corresponds to the Event ID
                        'seatNum': f'S{s}{letter}{i}',  # Generate seat numbers dynamically
                        'arenaId': arena_id,  # Assuming arenaId corresponds to the Arena ID
                        'ticketQR': 'x',  # Generate QR codes dynamically
                        'ticketPrice': 100,  # Generate ticket prices dynamically
                        'ticketType': 'normal',  # Assuming all tickets are Regular type
                        'zone': s,  # Distribute zones from 1 to 8 cyclically
                        'available': True,
                    })
            
        # Create Ticket instances from the generated data
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
