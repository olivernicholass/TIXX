from django.core.management.base import BaseCommand
from tixx.models import Ticket  # Import your Ticket model

class Command(BaseCommand):
    help = 'Import tickets into the database'

    def handle(self, *args, **kwargs):

        data = []
        for i in range(1, 51):  # Assuming you want to create 50 tickets
            data.append({
                'eventId': 1,  # Assuming eventId corresponds to the Event ID
                'seatNum': f'S1B{i}',  # Generate seat numbers dynamically
                'arenaId': 'AB123',  # Assuming arenaId corresponds to the Arena ID
                'ticketQR': 'x',  # Generate QR codes dynamically
                'ticketPrice': 100,  # Generate ticket prices dynamically
                'ticketType': 'normal',  # Assuming all tickets are Regular type
                'zone': 1,  # Distribute zones from 1 to 8 cyclically
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
