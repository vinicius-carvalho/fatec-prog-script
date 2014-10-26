# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from comportamento_app.model import Comportamento

class ComportamentoPublicForm(ModelForm):
    """
    Form used to show properties on app's home
    """
    _model_class = Comportamento
    _include = [Comportamento.titulo, 
                Comportamento.grau, 
                Comportamento.numero]


class ComportamentoForm(ModelForm):
    """
    Form used to save and update operations on app's admin page
    """
    _model_class = Comportamento
    _include = [Comportamento.titulo, 
                Comportamento.grau, 
                Comportamento.numero]


class ComportamentoDetailForm(ModelForm):
    """
    Form used to show entity details on app's admin page
    """
    _model_class = Comportamento
    _include = [Comportamento.titulo, 
                Comportamento.creation, 
                Comportamento.grau, 
                Comportamento.numero]


class ComportamentoShortForm(ModelForm):
    """
    Form used to show entity short version on app's admin page, mainly for tables
    """
    _model_class = Comportamento
    _include = [Comportamento.titulo, 
                Comportamento.creation, 
                Comportamento.grau, 
                Comportamento.numero]


class SaveComportamentoCommand(SaveCommand):
    _model_form_class = ComportamentoForm


class UpdateComportamentoCommand(UpdateNode):
    _model_form_class = ComportamentoForm


class ListComportamentoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListComportamentoCommand, self).__init__(Comportamento.query_by_creation())

