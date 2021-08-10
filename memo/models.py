from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from supermemo2 import SMTwo

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
    quality = models.IntegerField(
        choices=QualityChoices.choices,
    )

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
        return f'Review of {self.item}: {self.next_review_date}'

@receiver(post_save, sender=TaskToMemorize)
def create_review(sender, instance, created, *args, **kwargs):
    """Post save signals which create a first view for users"""
    review = SMTwo.first_review(2)
    if created:
        Review.objects.create(
            item=instance,
            next_review_date=review.review_date)

