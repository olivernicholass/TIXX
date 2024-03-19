#inserts ticket records into Ticket model.

from .models import Ticket  # Import your Ticket model

def insert_tickets():
    for i in range(1, 51):  # Assuming you want to insert 50 tickets
        ticket = Ticket.objects.create(
            ticketId=i,
            eventId=1,
            seatNum=i,
            ticketQR="",
            ticketPrice="50",
            zone=5,
            available=True
            )
        ticket.save()

if __name__ == "__main__":
    insert_tickets()