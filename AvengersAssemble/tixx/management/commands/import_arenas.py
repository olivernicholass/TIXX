from django.core.management.base import BaseCommand
from tixx.models import Arena

class Command(BaseCommand):
    help = 'Import arenas into the database'

    def handle(self, *args, **kwargs):
        arenas = [
            ["AB123","19800","Scotiabank Arena"],
            ["AC123","80000","Santiago Bernabéu"],
            ["MSGNY","120789","Madison Square Garden (New York, NY)"],
            ["TAPL","19060","Staples Center (Los Angeles, CA)"],
            ["STAPL","19060","Staples Center (Los Angeles, CA)"],
            ["UCNIL","20917","United Center (Chicago, IL)"],
            ["TDGBM","19580","TD Garden (Boston, MA)"],
            ["RKLY","19000","Barclays Center (Brooklyn, NY)"],
            ["AACDT","19200","American Airlines Center (Dallas, TX)"],
            ["COADC","20356","Capital One Arena (Washington, D.C.)"],
            ["AMWYC","20000","Amway Center (Orlando, FL)"],
            ["ORAC","19596","Oracle Arena (Oakland, CA)"],
            ["FSRFM","17341","Fiserv Forum (Milwaukee, WI)"]
        ]

        for arenaDATA in arenas:
            arena = Arena(
                arenaId=arenaDATA[0],
                arenaCapacity=int(arenaDATA[1]),
                arenaName=arenaDATA[2]
            )
            arena.save()

        self.stdout.write(self.style.SUCCESS('Arenas imported successfully'))