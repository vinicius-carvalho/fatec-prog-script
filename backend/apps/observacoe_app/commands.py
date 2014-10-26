# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, SingleOriginSearch, CreateArc, DeleteArcs
from observacoe_app.model import Observacoe, ArcoObs


class ObservacoePublicForm(ModelForm):
    """
    Form used to show properties on app's home
    """
    _model_class = Observacoe
    _include = [Observacoe.setor, 
                Observacoe.linha, 
                Observacoe.data, 
                Observacoe.comportamento,
                Observacoe.nome]


class ObservacoeForm(ModelForm):
    """
    Form used to save and update operations on app's admin page
    """
    _model_class = Observacoe
    _include = [Observacoe.setor, 
                Observacoe.linha, 
                Observacoe.data, 
                Observacoe.comportamento,
                Observacoe.nome]


class ObservacoeDetailForm(ModelForm):
    """
    Form used to show entity details on app's admin page
    """
    _model_class = Observacoe
    _include = [Observacoe.nome, 
                Observacoe.creation, 
                Observacoe.comportamento,
                Observacoe.setor, 
                Observacoe.data, 
                Observacoe.linha]


class ObservacoeShortForm(ModelForm):
    """
    Form used to show entity short version on app's admin page, mainly for tables
    """
    _model_class = Observacoe
    _include = [Observacoe.nome, 
                Observacoe.creation, 
                Observacoe.comportamento,
                Observacoe.setor, 
                Observacoe.data, 
                Observacoe.linha]


class SaveObservacoeCommand(SaveCommand):
    _model_form_class = ObservacoeForm


class UpdateObservacoeCommand(UpdateNode):
    _model_form_class = ObservacoeForm


class ListObservacoeCommand(ModelSearchCommand):
    def __init__(self):
        super(ListObservacoeCommand, self).__init__(Observacoe.query_by_creation())

class GetDonoObs(SingleOriginSearch):
    def __init__(self, obs):
        super(GetDonoObs, self).__init__(ArcoObs, obs)


class SalvarObsComUsuario(CreateArc):
    def __init__(self, _logged_user, **observacoe_properties):
        salvar = SaveObservacoeCommand(**observacoe_properties)
        super(SalvarObsComUsuario, self).__init__(ArcoObs, _logged_user, salvar)


class DeletarArco(DeleteArcs):
    def __init__(self, observacoe):
        super(DeletarArco, self).__init__(ArcoObs, destination=observacoe)