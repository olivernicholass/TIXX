from tixx.models import Ticket
from tixx.models import Event
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='Event ID')


    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        max_tickets = 2500
        try:
            event = Event.objects.get(pk=event_id)
            tickets = Ticket.objects.filter(eventId=event_id)
            print(f"TICKETS FOR EVENTID: {event_id}")
            
            tcount = 0
            available = 0
            taken = 0
            for ticket in tickets:
                print(f"Ticket ID: {ticket.ticketId}, Seat: {ticket.seatNum}", end=' ')
                tcount += 1
                if ticket.available:
                    available += 1
                else:
                    taken += 1
                
                
            print()
            ccount = 0
            rcount = 0
            scount = 0
            print(f"section 1 seats: ")
            print()
            for ticket in tickets:
                
                if ccount % 25 == 0:
                    print()   
                    rcount += 1
                if rcount % 26 == 0:
                    rcount = 1
                    scount += 1
                    print()
                    print()
                    print(f"section {scount+1} seats: ")
                if(ticket.available):
                    print(f"A", end=' ')
                else:
                    print(f"X", end=' ')
                ccount += 1
                
                    
            print()
            print(f"TOTAL TICKETS: {tcount}")
            print(f"TOTAL AVAILABLE: {available}")
            print(f"TOTAL TAKEN: {taken}")


        except Event.DoesNotExist:
            print("Event does not exist")
        except Exception as e:
            print(f"An error occurred: {e}")