# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb

from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from tekton import router


@no_csrf
def index():
    contexto = {'salvar_path':router.to_path(save)}
    return TemplateResponse(contexto)


class Solicitacao(Node):
    nome= ndb.StringProperty(required=True)
    email= ndb.StringProperty(required=True)
    comp= ndb.StringProperty(required=True)


class SolicitaForm(ModelForm):
    _model_class = Solicitacao
    _include = [Solicitacao.nome,Solicitacao.comp,Solicitacao.email]


def save(_resp,**props):
    solicitacaoForm=SolicitaForm(**props)
    erros=solicitacaoForm.validate()
    if erros:
        contexto = {'salvar_path': router.to_path(save),
                    'erros': erros}
        return TemplateResponse(contexto, 'scomp/home.html')

    #soli= Solicitacao(nome=props['nome'], email=['email'], comp=['comp'])

