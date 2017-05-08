"""Model module."""
from __future__ import unicode_literals

from .utils import tostr

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save

from address.models import AddressField, Country

from datetime import date


class Account(models.Model):
    """Account model."""

    user = models.OneToOneField(User, primary_key=True)
    avatar = models.ForeignKey('Media', related_name='+', null=True)
    address = AddressField(null=True, blank=True, related_name='+')
    languages = models.ManyToManyField(
        Country, blank=True, default=[], related_name='+'
    )


class Media(models.Model):
    """Media model."""

    file = models.FileField()
    url = models.CharField(max_length=255)


class VotedElement(models.Model):
    """Voted element model."""

    @property
    def score(self):
        """Score."""
        return sum(v.value for v in self.votes.all()) / self.votes.count()

    @property
    def type(self):
        """Get type name."""
        return self.__class__.__name__


class ContactElement(VotedElement):
    """Contact element model."""

    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=255, blank=True)
    public = models.BooleanField(default=True, blank=True)
    medias = models.ManyToManyField(
        Media, default=[], blank=True, related_name='+'
    )
    contacts = models.ManyToManyField(
        Account, related_name='debates', blank=True
    )


class Debate(ContactElement):
    """Debate model."""


class Organization(ContactElement):
    """Organization model."""

    address = AddressField(blank=True)
    lon = models.FloatField(blank=True)
    lat = models.FloatField(blank=True)

    @property
    def sorteddebates(self):
        """Get sorted debates by voting score."""
        return sorted(
            list(self.debates.filter(scheduling=None)), key='score',
            reversed=True
        )


class Scheduling(VotedElement):
    """Scheduling model."""

    date = models.DateField(blank=True)
    mduration = models.IntegerField(default=60, blank=True)
    organization = models.ForeignKey(
        Organization, blank=True, related_name='schedulings'
    )
    debate = models.OneToOneField(Debate, blank=True)


class Vote(models.Model):
    """Vote model."""

    account = models.ForeignKey(Account, blank=True, related_name='votes')
    votedelement = models.ForeignKey(
        VotedElement, blank=True, related_name='votes'
    )
    value = models.IntegerField()

    class Meta:
        """Vote meta class."""

        unique_together = ('account', 'votedelement')


class Category(models.Model):
    """Category model."""

    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)
    debates = models.ManyToManyField(Debate, blank=True, default=[])
    organizations = models.ManyToManyField(
        Organization, blank=True, default=[]
    )


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
    debates = models.IntegerField(default=0)
    organizations = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Representation."""
        return tostr(
            self, 'date', 'account', 'debates', 'organizations', 'votes'
        )


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
@receiver(post_save, sender=Debate)
@receiver(post_save, sender=Vote)
@receiver(post_save, sender=Organization)
def updatenewitems(sender, instance, created, **kwargs):
    """Save duration in stats."""
    if created:
        params = {
            '{0}s'.format(type(instance).__name__.lower()): 1
        }
        getorcreatestat(**params)
