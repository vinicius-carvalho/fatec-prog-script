# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Comportamento(Node):
    titulo = ndb.StringProperty(required=True)
    grau = ndb.StringProperty(required=True)
    numero = ndb.IntegerProperty(required=True)

