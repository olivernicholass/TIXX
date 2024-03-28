from django.core.management.base import BaseCommand
from tixx.models import Review, ReviewImage

class Command(BaseCommand):
    help = 'Import review images into the database'

    def handle(self, *args, **kwargs):
        review_images = [
            ["2","1","review_images/drakereview.jpg"],
            ["3","2","review_images/reviewdrake.jpg"],
            ["4","3","review_images/drakeimage.jpg"],
            ["5","10","review_images/foofight.jpg"],
            ["6","11","review_images/foo.jpg"],
            ["7","27","review_images/images_1.jpg"],
            ["8","28","review_images/drake-tour-moments.webp"],
            ["12","32","review_images/franko.jpg"],
            ["13","33","review_images/frankkk.jpg"],
            ["14","34","review_images/whiteferrari.jpg"]
        ]

        for imageDATA in review_images:
            reviewID = imageDATA[1]
            try:
                review = Review.objects.get(reviewId=reviewID)
                image = ReviewImage.objects.create(
                    review=review,
                    reviewImage=imageDATA[2]
                )
            except Review.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Review with ID {reviewID} does not exist"))

        self.stdout.write(self.style.SUCCESS('Review images imported successfully'))