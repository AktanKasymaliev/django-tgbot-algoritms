from django.db import models
from django.db import models
from django.db.models.signals import post_save

from supermemo2 import SMTwo

class MemoException(Exception):
    pass

class QualityChoices(models.IntegerChoices):
    COMPLETE_BLACKOUT = 0
    INCORR_CORRECT_ONE_REMEMBERED = 1
    INCORR_CORRECT_ONE_SEEMED_EASY = 2
    CORRECT_IT_WAS_DIFFICULT_TO_RECALL = 3
    CORRECT_AFTER_HESITATION = 4
    PERFECT_RESPONSE = 5

class TaskToMemorize(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255, null=True, blank=True)

    def create_new_review(self, quality):
        """Call this when there are some reviews (at least one) reviews"""
        if quality < 0 or quality > 5:
            raise MemoException(
                'Quality should be between 0 and 5 inclusively')
        last_rev = self.reviews.last()
        rev = SMTwo.first_review(quality, last_rev.review_date)
        Review.objects.create(
            item=self,
            quality=quality,
            next_review_date=rev.review_date)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            rev = SMTwo.first_review(3)
            Review.objects.create(
                item=instance,
                next_review_date=rev.review_date)

    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    item = models.ForeignKey(TaskToMemorize,
                             related_name='reviews',
                             on_delete=models.CASCADE)
    quality = models.IntegerField(
        choices=QualityChoices.choices,
        default=QualityChoices.CORRECT_IT_WAS_DIFFICULT_TO_RECALL)

    review_date = models.DateField(auto_now_add=True)
    next_review_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Review of {self.item}: {self.review_date}'

post_save.connect(TaskToMemorize.post_create, sender=TaskToMemorize)