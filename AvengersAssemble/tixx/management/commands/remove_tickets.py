from django.core.management.base import BaseCommand
from tixx.models import Ticket

class Command(BaseCommand):
    help = 'Delete tickets from the database for a specific event and arena'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='Event ID')
        parser.add_argument('arena_id', type=str, help='Arena ID')

    def handle(self, *args, **kwargs):
        event_id = kwargs['event_id']
        arena_id = kwargs['arena_id']

        # Query for tickets with the specified event_id and arena_id
        tickets_to_delete = Ticket.objects.filter(eventId=event_id, arenaId=arena_id)

        # Delete the tickets
        deleted_count, _ = tickets_to_delete.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully deleted {deleted_count} tickets for Event ID {event_id} and Arena ID {arena_id}"
        ))