from django.core.management.base import BaseCommand
from tixx.models import Review

class Command(BaseCommand):
    help = 'Import reviews into the database'

    def handle(self, *args, **kwargs):
        reviews = [
            ["1","Drake was amazing!!!","Drake's concert? Amazing vibes, seriously. The energy was insane, had everyone hyped up. His music hits you deep, you feel it. Can't even describe it, just incredible. Definitely a night to remember, no doubt about it.","2024-03-19","1","5"],
            ["2","Oracle Center Concert :))","Drake show, omg, sooo lit! Crowd go wild all night! His songs, like, amazing, you know? Old, new, all good vibes. I dance non-stop. Drake, he the best, for real! Can't wait for next time, gonna be epic, like, for sure!","2024-03-29","1","5"],
            ["3","Life changing concert...","Drake's concert was electrifying! The energy pulsated through the crowd as he delivered hit after hit with unmatched charisma. From 'Hotline Bling' to 'God's Plan,' the atmosphere was electric, leaving fans in awe of his talent. It was a night of unforgettable music and memories, solidifying Drake's status as a legendary performer.","2024-03-28","1","5"],
            ["4","Disappointing Experience","Attended Drake's concert last night and left feeling disappointed. The sound quality was poor, and Drake seemed disinterested. The venue was overcrowded, making it difficult to enjoy the performance. Overall, it was a lackluster experience.","2024-02-13","1","1"],
            ["5","decent performance, tech issues","Drake put on a solid performance at his recent concert. The setlist was decent, and the crowd was engaged. However, there were some technical issues with the sound system, and the venue was too small for the number of attendees. With some improvements, it could have been a great night.","2024-01-16","1","3"],
            ["6","mixed feelings....","Mixed feelings about Drake's concert. While his performance was entertaining and the atmosphere was lively, there were some aspects that fell short. The venue was too crowded, and it was hard to see the stage from certain angles. Overall, it was an average experience.","2024-02-16","1","2.5"],
            ["7","THE GOAT DID HIS THANG","THIS GUYS DOES NOT MISS, PHENOMENAL PERFORMANCE FROM THE GOAT","2024-03-18","1","5"],
            ["8","the best","So good😭😭😭😭 bro pcd be hitting sooooo hard. Going to drakes concert will be my personality until his next tour fr.","2024-01-01","1","5"],
            ["9","decent concert","It was alright","2024-02-15","1","3"],
            ["10","Amazing concert!","The Foofighters brought down the house with a high-octane performance at Oracle Center. Frontman Dave Grohl's charisma ignited the crowd as hits like ""Everlong"" and ""The Pretender"" filled the air. With boundless energy and musical precision, the band proved why they're rock legends.","2024-03-04","3","5"],
            ["11","Slightly disappointed with our experience..","The Foofighters' performance at Oracle Center showcased their enduring talent but lacked the spark of previous shows. While hits like ""Everlong"" still resonated, the energy felt somewhat subdued. Frontman Dave Grohl's charm was present, but the overall experience fell short of expectations.","2024-03-04","3","3"],
            ["18","Great concert!","This was my first concert ever, I will definitely be seeing drake again 😊😊","2024-03-13","1","3"],
            ["19","unreal experience...","This concert was like no other and I am so glad I bought tickets for it. Drake played my favorite tracks and I will be seeing him again for sure.","2024-03-18","1","5"],
            ["25","fdsa","fdsa","2024-03-19","1","0"],
            ["26","dsa","dsa","2024-03-20","1","0"],
            ["27","loved the concert :))","A mesmerizing experience! Drake's energy lit up the arena, delivering hit after hit with flawless execution and electrifying stage presence","2024-03-04","1","4"],
            ["28","great experience!","Sensational showmanship! Drake commanded the stage with unmatched charisma, treating fans to an exhilarating night of non-stop hits and high-energy vibes.","2024-03-19","1","5"],
            ["32","i love frank ocean!!🌊🌊","frank ocean is my favorite artist of all time and I finally got to see him in concert. This was definitely the best night of my life and I am going to remember it forever. This was also my first time in los angeles and it was great.","2024-03-21","7","5"],
            ["33","frank ocean is the best!!!","Frank Ocean's music is a transcendental journey, blending soulful vocals with introspective lyrics. His album ""Blonde"" is a masterpiece, weaving themes of love, loss, and self-discovery into a sonic tapestry that resonates deeply with listeners. Ocean's artistry is unparalleled, evoking raw emotion with every note.","2024-03-18","7","5"],
            ["34","I LOVE WHITE FERRARI 😊😊","White Ferrari"" by Frank Ocean holds a special place in my heart. Its ethereal melodies and soul-stirring lyrics resonate with me on a profound level. Each listen feels like a journey through my own emotions, making it an unforgettable masterpiece in my eyes.","2024-02-22","7","5"]
        ]

        for review in reviews:
            review_obj = Review(
                reviewId=review[0],
                reviewTitle=review[1],
                reviewText=review[2],
                reviewDate=review[3],
                reviewFigure_id=review[4],
                reviewRating=review[5]
            )
            review_obj.save()

        self.stdout.write(self.style.SUCCESS('Reviews imported successfully'))
