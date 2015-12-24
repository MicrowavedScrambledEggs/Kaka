import mongoengine
from django.db import models
from mongcore.models import Feature, ChangeLog, Addition, Deletion, Change
from core.models import Feature as OldFeature
from uuid import uuid4
from mongcore.document_change_listener import *

from django.core.urlresolvers import reverse


class Chromosome(Feature):
    no = mongoengine.StringField(max_length=10)

    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        return self.no


class Genotype(Feature):
    ebrida_id = mongoengine.StringField(max_length=255)
    kea_id = mongoengine.StringField(max_length=255)

    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None,  cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, **kwargs):
        super(Genotype, self).save(
            force_insert, validate, clean, write_concern,
            cascade, cascade_kwargs, _refs, save_condition, **kwargs
        )
        log_addition(self)

    def delete(self, **write_concern):
        log_deletion(self)
        super(Genotype, self).delete(**write_concern)

    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        name = self.name
        if self.kea_id is not None and self.ebrida_id is not None:
            name = name + '/' + self.kea_id + '/' + self.ebrida_id
        name = name + '/' + self.datasource.GetName()
        return name


class Marker(Feature):
    ebrida_id = mongoengine.StringField(max_length=255)
    kea_id = mongoengine.StringField(max_length=255)
    sex = mongoengine.StringField(max_length=5)

    def __unicode__(self):
        return self.GetName()
    
    def GetName(self):
        return self.kea_id + '/' + self.ebrida_id

    def get_absolute_url(self):
        return reverse('marker-detail', kwargs={'pk': self.pk})


class OldMarker(OldFeature):
    ebrida_id = mongoengine.StringField(max_length=255)
    kea_id = mongoengine.StringField(max_length=255)
    sex = mongoengine.StringField(max_length=5)

    def __unicode__(self):
        return self.GetName()

    def GetName(self):
        return self.kea_id + '/' + self.ebrida_id

    def get_absolute_url(self):
        return reverse('marker-detail', kwargs={'pk': self.pk})

    class Meta:
        app_label = 'mongenotype'


class Primer(Feature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class PrimerType(Feature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class OldPrimer(OldFeature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name

    class Meta:
        app_label = 'mongenotype'


class OldPrimerType(OldFeature):
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name

    class Meta:
        app_label = 'mongenotype'


class PrimerOb(Feature):
    primer = mongoengine.ReferenceField(Primer)
    primer_type = mongoengine.ReferenceField(PrimerType)
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name


class OldPrimerOb(OldFeature):
    primer = models.ForeignKey(OldPrimer)
    primer_type = models.ForeignKey(OldPrimerType)
    def __unicode__(self):
        return self.name

    def GetName(self):
        return self.name

    class Meta:
        app_label = 'mongenotype'

#primerob
#    genotype | primertype
#    genotype | markerob
#    genotype | primer
#    genotype | primertail


# Create your models here.
