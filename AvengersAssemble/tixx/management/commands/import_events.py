from django.core.management.base import BaseCommand
from tixx.models import Event, Arena, Figure

class Command(BaseCommand):
    help = 'Import events into the database'

    def handle(self, *args, **kwargs):
        events = [
            ["Foo Fighters","2024-03-29","1","Vancouver","Foo Fighters Concert","Active","Rock","event_images/foofighters_tJc5pIT.webp","AB123","3","20:00:00"],
            ["Lil Tecca","2024-03-17","2","Vancouver","Lil Tecca Concert","Active","Hip-Hop","event_images/liltecca_hsfyluS.jpg","AB123",None,"12:00:00"],
            ["Real Madrid vs. FC Barcelona","2024-03-17","3","Madrid, Spain","Football Game","Active","Soccer","event_images/barca_DvPFJOo.jpg","AC123",None,"12:00:00"],
            ["Drake Concert","2024-05-30","4","Vancouver","Drake Concert","Active","Hip-Hop","event_images/drake-concert.jpg","AB123","1","19:00:00"],
            ["Drake Concert","2024-04-05","5","Los Angeles, CA","Drake Concert","Active","Hip-Hop","","STAPL","1","19:30:00"],
            ["Drake Concert","2024-03-29","6","(Boston, MA)","Drake Concert","Active","Hip-Hop","","TDGBM","1","18:00:00"],
            ["Drake Concert","2024-03-20","7","(Oakland, CA)","Drake Concert","Active","Hip-Hop","","ORAC","1","12:00:00"],
            ["Frank Ocean Concert","2024-04-17","8","Chicago, IL","Frank Ocean Concert","Active","Pop","","UCNIL","7","19:00:00"],
            ["Frank Ocean Concert","2024-04-25","9","New York, NY","Frank Ocean Concert","Active","Pop","","MSGNY","7","17:00:00"],
            ["Frank Ocean Concert","2024-05-16","10","Los Angeles, CA","Frank Ocean Concert","Active","Pop","","STAPL","7","20:00:00"],
            ["Justin Bieber Concert","2024-05-16","11","Boston, MA","Justin Bieber Concert","Active","Pop","","TDGBM","9","18:00:00"],
            ["Kanye West Concert","2024-06-19","12","Los Angeles, CA","Ye Concert","Active","Hip-Hop","","STAPL","2","12:00:00"]
        ]

        for eventDATA in events:
            arenaID = eventDATA[8] if eventDATA[8] else None
            figureID = eventDATA[9] if eventDATA[9] else None

            event = Event(
                eventName=eventDATA[0],
                eventDate=eventDATA[1],
                eventId=eventDATA[2],
                eventLocation=eventDATA[3],
                eventDescription=eventDATA[4],
                eventStatus=eventDATA[5],
                eventGenre=eventDATA[6],
                eventImage=eventDATA[7],
                arenaId=Arena.objects.get(arenaId=arenaID) if arenaID else None,
                figureId=Figure.objects.get(id=figureID) if figureID else None,
                eventTime=eventDATA[10]
            )
            event.save()

        self.stdout.write(self.style.SUCCESS('Events imported successfully'))
