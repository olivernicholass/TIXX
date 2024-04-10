from django.core.management.base import BaseCommand
from tixx.models import Ticket, Event

class Command(BaseCommand):
    help = 'Delete tickets from the database for a specific event and arena'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='Event ID')

    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']

        # Query for tickets with the specified event_id and arena_id
        event_to_delete = Event.objects.filter(eventId=event_id)
        tickets_to_delete = Ticket.objects.filter(eventId=event_id)

        # Delete the tickets
        deleted_count, _ = tickets_to_delete.delete()
        deleted_event = event_to_delete.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted event ID {event_id} with its {deleted_count} tickets"
        ))