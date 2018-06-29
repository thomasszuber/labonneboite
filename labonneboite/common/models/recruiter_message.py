import datetime, enum

from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.types import Enum
from sqlalchemy.orm.exc import NoResultFound
from labonneboite.common import mapping as mapping_util
from labonneboite.common.models import Office
from labonneboite.common.database import Base
from labonneboite.common.models.base import CRUDMixin
from labonneboite.web.contact_form import forms

class NoOfficeFoundException(Exception):
    pass


class RecruiterMessageCommon(object):
    # Identification part
    id = Column(Integer, primary_key=True)
    siret = Column(Text, nullable=True)
    requested_by_first_name = Column(mysql.TINYTEXT, nullable=True)
    requested_by_last_name = Column(mysql.TINYTEXT, nullable=True)
    requested_by_email = Column(mysql.TINYTEXT, nullable=True)
    requested_by_phone = Column(mysql.TINYTEXT, nullable=True)

    # Timestamps
    date_created = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    date_updated = Column(DateTime, nullable=True)

    @classmethod
    def create_from_form(cls, form):
        instance = cls()
        instance.siret = form.siret.data
        instance.siret = form.siret.data
        instance.requested_by_first_name = form.first_name.data
        instance.requested_by_last_name = form.last_name.data
        instance.requested_by_email = form.email.data
        instance.requested_by_phone = form.phone.data
        instance.fill_values(form)
        return instance.save()

    def fill_values(self, form):
        raise NotImplementedError


class OtherRecruiterMessage(RecruiterMessageCommon, CRUDMixin, Base):
    __tablename__ = 'other_recruiter_message'
    name = 'other'

    comment = Column(Text, nullable=True)

    def fill_values(self, form):
        self.comment = form.comment.data


class RemoveRecruiterMessage(RecruiterMessageCommon, CRUDMixin, Base):
    __tablename__ = 'remove_recruiter_message'
    name = 'remove'

    remove_lba = Column(Boolean, default=True)
    remove_lbb = Column(Boolean, default=True)

    def fill_values(self, form):
        self.remove_lbb = 1 if form.remove_lbb.data else 0
        self.remove_lba = 1 if form.remove_lba.data else 0


class UpdateCoordinatesRecruiterMessage(RecruiterMessageCommon, CRUDMixin, Base):
    __tablename__ = 'update_coordinates_recruiter_message'
    name = 'update_coordinates'

    new_website = Column(mysql.TINYTEXT, nullable=True)
    new_email = Column(mysql.TINYTEXT, nullable=True)
    new_phone = Column(mysql.TINYTEXT, nullable=True)
    contact_mode = Column(mysql.TINYTEXT, nullable=True)
    new_email_alternance = Column(mysql.TINYTEXT, nullable=True)
    new_phone_alternance = Column(mysql.TINYTEXT, nullable=True)
    social_network = Column(mysql.TINYTEXT, nullable=True)

    @classmethod
    def fill_values(self, form):
        self.new_website = form.new_website.data
        self.new_email = form.new_email.data
        self.new_phone = form.new_phone.data
        self.contact_mode = form.new_contact_mode.data
        self.new_email_alternance = form.new_email_alternance.data
        self.new_phone_alternance = form.new_phone_alternance.data
        self.social_network = form.social_network.data


class UpdateJobsRecruiterMessage(RecruiterMessageCommon, CRUDMixin, Base):
    __tablename__ = 'update_jobs_recruiter_message'
    name = 'update_jobs'

    romes_to_add = Column(mysql.TINYTEXT, nullable=True)
    romes_to_remove = Column(mysql.TINYTEXT, nullable=True)
    romes_alternance_to_add = Column(mysql.TINYTEXT, nullable=True)
    romes_alternance_to_remove = Column(mysql.TINYTEXT, nullable=True)

    @classmethod
    def fill_values(self, form):
        try:
            office = Office.query.filter(Office.siret == form.siret.data).first()
        except NoResultFound:
            raise NoOfficeFoundException('No office found with siret : {}'.format(form.data.siret))

        office_romes = set([item.code for item in mapping_util.romes_for_naf(office.naf)])

        _, lbb_romes, lba_romes, hide_romes = forms.compute_romes()
        lbb_romes = set(lbb_romes)
        lba_romes = set(lba_romes)
        hide_romes = set(hide_romes)


        # Remove checkboxes and romes not open to applications
        romes_to_remove = hide_romes.union(office_romes) - lbb_romes

        # Remove checkboxes and romes not open to alternance
        romes_alternance_to_remove = hide_romes.union(office_romes) - lba_romes

        self.romes_to_add = ','.join(lbb_romes - office_romes)
        self.romes_to_remove = ','.join(romes_to_remove)
        self.romes_alternance_to_add = ','.join(lba_romes - office_romes)
        self.romes_alternance_to_remove = ','.join(romes_alternance_to_remove)
