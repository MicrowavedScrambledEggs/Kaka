from api.connectors import *
from seafood.models import *
from api.imports import *
import time
import datetime
from django.utils.timezone import get_current_timezone, make_aware


class Import(ImportOp):
    ds = None
    @staticmethod
    def ImportOp(line, succ):
        if line['Deleted Flag'] == 'N':
            term, created = Staff.objects.get_or_create(name=line['Name'], initials=line['Initials'])
            term.datasource = Import.ds
            term.lastupdatedby = line['Updated By']
            SaveKVs(term, line)
            term.save()

    @staticmethod
    def CleanOp():
        Staff.objects.filter(datasource=Import.ds).delete()


def load():
    conn = ExcelConnector('data/seafood/tablet/staff.xlsx')
    im = GenericImport(conn)
    im.load_op = Import.ImportOp
    im.clean_op = Import.CleanOp()
    im.Load()


def init():
    onto = Ontology.objects.get(name="Staff")
    dt = datetime.datetime.now()
    ds_tree, created = DataSource.objects.get_or_create(
        name='Seafood Import Staff Init',
        ontology=onto,
        supplier="Seafood",
    )

    st = Study.objects.get_or_create(
        name='Seafood',
	datasource=ds_tree,
    )

    Import.study = st
    Import.ds = ds_tree


def run():
    init()
    load()


