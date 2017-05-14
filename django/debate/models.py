"""Model module."""
from __future__ import unicode_literals

from .utils import tostr

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from address.models import AddressField, Country

from time import time

from datetime import date, datetime

from re import compile


class Account(models.Model):
    """Account model."""

    user = models.OneToOneField(User, primary_key=True)
    avatar = models.ForeignKey('Media', related_name='+', null=True)
    address = AddressField(null=True, blank=True, related_name='+')
    languages = models.ManyToManyField(
        Country, blank=True, default=[], related_name='+'
    )


class Tag(models.Model):
    """Tag model."""

    name = models.CharField(max_length=50, primary_key=True)

    RE = compile('#\w+')

    @staticmethod
    def settags(commentedelt, tagsfield):
        """Set tags to commentedelt from input txt."""
        tagsfieldattr = getattr(commentedelt, tagsfield)
        tags = [
            tag[1:] for tag in Tag.RE.findall(tagsfieldattr)
        ]
        commentedelt.tags.set(tags)


class CommentedElement(models.Model):
    """Commented element model."""

    created = models.DateTimeField(blank=True, default=datetime.now)
    modified = models.DateTimeField(blank=True, default=None, null=True)
    tags = models.ManyToManyField(
        Tag, blank=True, default=[], related_name='tagged'
    )

    @property
    def score(self):
        """Score."""
        return sum(v.value for v in self.votes.all()) / self.votes.count()

    @property
    def type(self):
        """Get type name."""
        return type(self).__name__


@receiver(pre_save, sender=CommentedElement)
def update(sender, instance, **kwargs):
    """Update modified."""
    instance.modified = time()


class Comment(CommentedElement):
    """Comment model."""

    author = models.ForeignKey(Account, blank=True, related_name='comments')
    cited = models.ManyToManyField(
        Account, default=[], blank=True, related_name='cited'
    )
    content = models.CharField(max_length=255, db_index=True)
    commentated = models.ForeignKey(
        CommentedElement, related_name='comments', blank=True
    )

    CITED_RE = compile(r'@\w+')

    def setcited(self):
        """Set cited."""
        cited = [cited[1:] for cited in Comment.CITED_RE.findall(self.content)]
        self.cited.set(cited)


@receiver(pre_save, sender=Comment)
def updatecomment(sender, instance, **kwargs):
    """Update modified time if element is updated."""
    Tag.settags(instance, 'content')
    instance.setcited()


class Media(models.Model):
    """Media model."""

    file = models.FileField()
    url = models.CharField(max_length=255)
    source = models.ForeignKey(
        CommentedElement, blank=True, related_name='medias'
    )


class AdministratedElement(CommentedElement):
    """Contact element model."""

    name = models.CharField(max_length=50, blank=True, db_index=True)
    description = models.CharField(max_length=255, blank=True, db_index=True)
    public = models.BooleanField(default=True, blank=True, db_index=True)
    admins = models.ManyToManyField(Account, default=[], blank=True)


@receiver(pre_save, sender=AdministratedElement)
def updateadministratedelt(sender, instance, **kwargs):
    """Update modified time if element is updated."""
    Tag.settags(instance, 'description')


class Topic(AdministratedElement):
    """Topic model."""

    base = models.OneToOneField(
        AdministratedElement,
        parent_link=True, related_name='_topic', blank=True
    )


class Space(AdministratedElement):
    """Space model."""

    address = AddressField(blank=True)
    lon = models.FloatField(blank=True, db_index=True)
    lat = models.FloatField(blank=True, db_index=True)

    base = models.OneToOneField(
        AdministratedElement,
        parent_link=True, related_name='_space', blank=True
    )

    @property
    def sorteddebates(self):
        """Get sorted topics by voting score."""
        return sorted(
            list(self.topics.filter(scheduling=None)), key='score',
            reversed=True
        )


class Scheduling(AdministratedElement):
    """Scheduling model."""

    date = models.DateField(blank=True)
    mduration = models.IntegerField(default=60, blank=True)
    space = models.ForeignKey(
        Space, blank=True, related_name='schedulings'
    )
    topic = models.ForeignKey(Topic, blank=True, related_name='schedulings')
    base = models.OneToOneField(
        AdministratedElement,
        parent_link=True, related_name='_scheduling', blank=True
    )


class Vote(models.Model):
    """Vote model."""

    account = models.ForeignKey(Account, blank=True, related_name='votes')
    voted = models.ForeignKey(
        CommentedElement, blank=True, related_name='votes'
    )
    value = models.IntegerField()

    class Meta:
        """Vote meta class."""

        unique_together = ('account', 'voted')


@python_2_unicode_compatible
class ForbiddenEmail(models.Model):
    """Forbidden email."""

    email = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        """Representation."""
        return tostr(self, 'email')


@python_2_unicode_compatible
class Stat(models.Model):
    """Statistical model."""

    date = models.DateField(default=date.today, primary_key=True)
    accounts = models.IntegerField(default=0)
    topics = models.IntegerField(default=0)
    spaces = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Representation."""
        return tostr(
            self, 'date', 'account', 'topics', 'spaces', 'votes'
        )


class ProjectionEntry(models.Model):
    """Projection Entry."""

    scheduling = models.OneToOneField(Scheduling, blank=True)
    question = models.CharField(max_length=255, db_index=True)
    answers = models.CharField(max_length=255, db_index=True)


def getorcreatestat(**kwargs):
    """Get or create a stat with input field and value."""
    result, created = Stat.objects.get_or_create(
        date=date.today(), defaults=kwargs
    )

    if not created:
        for field in kwargs:
            kwargs[field] = F(field) + kwargs[field]
        Stat.objects.filter(date=result.date).update(**kwargs)

    return result


@receiver(post_save, sender=Account)
@receiver(post_save, sender=Topic)
@receiver(post_save, sender=Vote)
@receiver(post_save, sender=Space)
def updatenewitems(sender, instance, created, **kwargs):
    """Save duration in stats."""
    if created:
        params = {
            '{0}s'.format(type(instance).__name__.lower()): 1
        }
        getorcreatestat(**params)
