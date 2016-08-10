# -*- coding: utf-8 -*-
import re
from string import ascii_uppercase
from datetime import date
from unidecode import unidecode

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator


# Main models and catalogs
class AcademicDegree(models.Model):

    class Meta:
        verbose_name = u'Grado académico'
        verbose_name_plural = u'Grados académicos'

    name_male = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=u'Grado académico masculino'
    )
    name_female = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=u'Grado académico femenino'
    )

    def __unicode__(self):
        return self.name_male + " / " + self.name_female

    def save(self):
        return_value = super(AcademicDegree, self).save()
        people = Person.objects.filter(academic_degree=self)
        for person in people:
            person.search_field = unidecode(person.__unicode__().lower())
            person.save()

        return return_value


class CourtesyTitle(models.Model):

    class Meta:
        verbose_name = u'Tratamiento de cortesía'
        verbose_name_plural = u'Tratamientos de cortesía'

    title_male = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=u'Título masculino'
    )

    title_female = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=u'Título femenino'
    )

    def __unicode__(self):
        return self.title_male + " / " + self.title_female

    def save(self):
        return_value = super(CourtesyTitle, self).save()
        people = Person.objects.filter(courtesy_title=self)

        for person in people:
            person.search_field = unidecode(person.__unicode__().lower())
            person.save()

        return return_value


class AddressAbstract(models.Model):
    street = models.CharField(
        max_length=255,
        verbose_name='Calle',
        blank=True,
        null=True
    )
    external_number = models.CharField(
        max_length=255,
        verbose_name=u'Número exterior',
        blank=True,
        null=True
    )
    internal_number = models.CharField(
        max_length=255,
        verbose_name=u'Número interior',
        blank=True,
        null=True
    )
    suburb = models.CharField(
        max_length=255,
        verbose_name='Colonia',
        blank=True,
        null=True
    )
    locality = models.CharField(
        max_length=255,
        verbose_name=u'Delegación/Municipio',
        blank=True,
        null=True
    )
    city = models.CharField(
        max_length=255,
        verbose_name=u'Ciudad',
        blank=True,
        null=True
    )
    reference = models.CharField(
        max_length=255,
        verbose_name='Referencia',
        blank=True,
        null=True
    )
    state = models.CharField(
        max_length=255,
        verbose_name='Estado',
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=255,
        verbose_name=u'País',
        blank=True,
        null=True
    )
    zip_code = models.CharField(
        max_length=255,
        verbose_name='Código postal',
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Address(AddressAbstract):

    def __unicode__(self):
        string = (self.street) + " " + (self.external_number) + " " + \
            (self.internal_number) + " " + (self.suburb) + " " + \
            (self.locality) + " " + (self.reference) + " " + \
            (self.city) + " " + (self.state) + " " + (self.country) + \
            " cp: " + (self.zip_code)
        return re.sub(' +', ' ', string)


class OfficialAddress(AddressAbstract):
    rfc = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                r'^([A-Z|a-z|&amp;]{3})(([0-9]{2})([0][13456789]|[1][012])([0][1-9]|[12][\d]|[3][0])|([0-9]{2})([0][13578]|[1][02])([0][1-9]|[12][\d]|[3][01])|([02468][048]|[13579][26])([0][2])([0][1-9]|[12][\d])|([1-9]{2})([0][2])([0][1-9]|[12][0-8]))(\w{2}[A|a|0-9]{1})$|^([A-Z|a-z]{4})(([0-9]{2})([0][13456789]|[1][012])([0][1-9]|[12][\d]|[3][0])|([0-9]{2})([0][13578]|[1][02])([0][1-9]|[12][\d]|[3][01])|([02468][048]|[13579][26])([0][2])([0][1-9]|[12][\d])|([1-9]{2})([0][2])([0][1-9]|[12][0-8]))((\w{2})([A|a|0-9]{1})){0,3}$',
                u'El RFC debe ser en mayúsculas, sin espacios ni guiones, por ejemplo: VECJ880326P76. Este campo valida contra la información del SAT verifique por favor si lo tecleó correctamente'
            )
        ],
        verbose_name='RFC'
    )
    name = models.CharField(
        max_length=255,
        verbose_name=u'Razón Social',
        blank=True,
        null=True
    )
    email = models.EmailField(
        max_length=255,
        unique=False,
        verbose_name='Correo electrónico',
        null=True,
        blank=True
    )

    def __unicode__(self):
        string = (self.name) + " " + (self.rfc) + " " + \
            (self.street) + " " + (self.external_number) + " " + \
            (self.internal_number) + " " + (self.suburb) + " " + \
            (self.locality) + " " + (self.reference) + " " + \
            (self.city) + " " + (self.state) + " " + (self.country) + \
            " cp: " + (self.zip_code)
        return re.sub(' +', ' ', string)


class Person(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Nombre'
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name='Apellido'
    )
    courtesy_title = models.ForeignKey(
        CourtesyTitle,
        verbose_name='Título de cortesía',
        null=True,
        blank=True
    )
    telephone = models.CharField(
        max_length=255,
        verbose_name='Teléfono',
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=255,
        unique=False,
        verbose_name='Correo electrónico',
        null=True,
        blank=True
    )
    birthdate = models.DateField(
        verbose_name='Fecha de nacimiento',
        null=True,
        blank=True
    )
    #Sex definition
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'Masculino'),
        (FEMALE, 'Femenino'),
    )
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        default=MALE,
        verbose_name=u'Sexo'
    )
    academic_degree = models.ForeignKey(
        AcademicDegree,
        verbose_name=u'Grado académico',
        null=True,
        blank=True
    )
    company = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=u'Empresa'
    )
    position = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=u'Puesto'
    )
    status = models.BooleanField(
        default=True,
        verbose_name='Activo',
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    search_field = models.CharField(
        max_length=800,
        blank=True,
        null=True
    )

    def __unicode__(self):
        name = ""
        if self.courtesy_title:
            if self.sex == self.MALE:
                name += self.courtesy_title.title_male + " "
            else:
                name += self.courtesy_title.title_female + " "
        if self.academic_degree:
            if self.sex == self.MALE:
                name += self.academic_degree.name_male + " "
            else:
                name += self.academic_degree.name_female + " "
        return (
            name + self.name + " " + self.last_name
        )

    def save(self):
        # Post save action
        return_value = super(Person, self).save()

        try:
            friend = Friend.objects.get(person=self.pk)
        except Friend.DoesNotExist:
            friend = None
        if friend:
            friend.name = self.name + " " + self.last_name
            friend.save()

        return return_value


class Institution(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=u'Razón social'
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=u'Correo electrónico',
        blank=True,
        null=True
    )
    telephone = models.CharField(
        max_length=255,
        verbose_name=u'Teléfono',
        blank=True,
        null=True
    )
    web_page = models.CharField(
        max_length=500,
        verbose_name=u'Página web',
        blank=True,
        null=True
    )
    status = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    search_field = models.CharField(
        max_length=800,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.name

    def save(self):
        return_value = super(Institution, self).save()
        # post save actopm
        self.search_field = unidecode(self.__unicode__()).lower()
        try:
            friend = Friend.objects.get(institution=self.pk)
        except Friend.DoesNotExist:
            friend = None
        if friend:
            friend.name = self.name
            friend.save()
        return return_value


class Friend(models.Model):
    person = models.OneToOneField(
        Person,
        primary_key=False,
        null=True,
        blank=True
    )
    institution = models.OneToOneField(
        Institution,
        primary_key=False,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255
    )
    official_address = models.ForeignKey(
        OfficialAddress,
        verbose_name=u'Dirección fiscal',
        null=True,
        blank=True
    )
    delivery_address = models.ForeignKey(
        Address,
        verbose_name=u'Dirección para entregas',
        null=True,
        blank=True
    )
    #The unique code for this friend
    code = models.CharField(
        max_length=255
    )
    notes = models.TextField(
        verbose_name='Notas',
        null=True,
        blank=True
    )
    promoter = models.ForeignKey(
        'self',
        verbose_name='Promotor',
        null=True,
        blank=True,
        related_name='promoted'
    )
    temp_key = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.person:
            return self.person.__unicode__()
        else:
            return self.institution.name

    def save(self):
        if not self.code:
            code = u''
            if self.person:
                code += unidecode(self.person.name[0])
                code += unidecode(self.person.last_name[0])
            else:
                code += unidecode(self.institution.name[0])
                code += unidecode(self.institution.name[1])
            for letter in ascii_uppercase:
                if not self._meta.model.objects.filter(code=code + letter):
                    code += letter
                    break
            self.code = code

        if self.person:
            self.name = self.person.name + " " + self.person.last_name
        else:
            self.name = self.institution.name

        return super(Friend, self).save()

    def first_contribution(self):
        return self.contribution_set.filter(
            status__success=True,
        ).earliest('created')


class Contact(models.Model):

    class Meta:
        verbose_name = u'Contacto'
        verbose_name_plural = u'Contactos'

    name = models.CharField(
        max_length=255,
        verbose_name=u'Nombre'
    )

    position = models.CharField(
        max_length=255,
        verbose_name=u'Puesto',
        blank=True,
        null=True
    )

    company = models.CharField(
        max_length=255,
        verbose_name=u'Empresa',
        blank=True,
        null=True
    )

    friend = models.ForeignKey(
        Friend,
        verbose_name=u'Amigo',
        related_name='contacts'
    )

    send_correspondence = models.BooleanField(
        default=False,
        verbose_name=u'Enviar correspondencia'
    )

    def __unicode__(self):
        return self.name + " " + self.position + " " + self.company


class ContactMethod(models.Model):

    class Meta:
        verbose_name = u'Método de contacto'
        verbose_name = u'Métodos de contacto'

    contact_method = models.CharField(
        max_length=255,
        verbose_name=u'Método de contacto'
    )
    contact_information = models.CharField(
        max_length=255,
        verbose_name='Contacto'
    )
    contact = models.ForeignKey(
        Contact,
        blank=False,
        null=False,
        verbose_name='Contacto',
        related_name='contact_methods'
    )
