# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime
from google.appengine.ext import ndb
from gaegraph.model import Node, Arc
from gaeforms.ndb import property
from slugify import slugify


class Observacoe(Node):
    nome = ndb.StringProperty(required=True)
    setor = ndb.StringProperty(required=True)
    linha = ndb.IntegerProperty(required=True)
    data = ndb.DateProperty(required=True)
    comportamento = ndb.StringProperty(required=True, indexed=False)
    busca= ndb.ComputedProperty(lambda self: slugify(self.comportamento))


class ArcoObs(Arc):
    destination = ndb.KeyProperty(Observacoe, required=True)