# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandParallel
from observacoe_app.commands import GetDonoObs
from observacoe_app.model import Observacoe
from slugify import slugify
from tekton import router
from gaecookie.decorator import no_csrf
from observacoe_app import facade
from routes.observacoes.admin import new, edit


def delete(_handler, observacoe_id):
    facade.delete_observacoe_cmd(observacoe_id)()
    facade.DeletarArcocmd(observacoe_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    # cmd = facade.list_observacoes_cmd()
    # observacoes = cmd()
    # get_dono_cmd_lista=[GetDonoObs(o) for o in observacoes]
    # paralelo=CommandParallel(*get_dono_cmd_lista)
    # paralelo()
    #
    # edit_path = router.to_path(edit)
    # delete_path = router.to_path(delete)
    # short_form = facade.observacoe_short_form()
    #
    # def short_observacoe_dict(observacoe):
    #     observacoe_dct = short_form.fill_with_model(observacoe)
    #     observacoe_dct['edit_path'] = router.to_path(edit_path, observacoe_dct['id'])
    #     observacoe_dct['delete_path'] = router.to_path(delete_path, observacoe_dct['id'])
    #     return observacoe_dct
    #
    #
    # short_observacoes = [short_observacoe_dict(observacoe) for observacoe in observacoes]
    # for observacao,dono_comando in zip(short_observacoes,get_dono_cmd_lista):
    #     observacao['dono_flag']=(dono_comando.result ==_logged_user)
    # context = {'observacoes': short_observacoes,
    #            'new_path': router.to_path(new),
    #            'busca_produtos':router.to_path(busca_produtos)
    #            }
    return TemplateResponse()




@no_csrf
def busca_produtos(_logged_user, busca):
    cmd = facade.list_observacoes_cmd()
    observacoes = cmd()
    busca = slugify(busca)
    pesquisa = Observacoe.query(Observacoe.busca >= busca).order(Observacoe.busca)

    get_dono_cmd_lista=[GetDonoObs(o) for o in observacoes]
    paralelo=CommandParallel(*get_dono_cmd_lista)
    paralelo()

    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    short_form = facade.observacoe_short_form()

    def short_observacoe_dict(observacoe):
        observacoe_dct = short_form.fill_with_model(observacoe)
        observacoe_dct['edit_path'] = router.to_path(edit_path, observacoe_dct['id'])
        observacoe_dct['delete_path'] = router.to_path(delete_path, observacoe_dct['id'])
        return observacoe_dct


    short_observacoes = [short_observacoe_dict(observacoe) for observacoe in observacoes]
    for observacao,dono_comando in zip(short_observacoes,get_dono_cmd_lista):
        observacao['dono_flag']=(dono_comando.result ==_logged_user)
    context = {'observacoe': short_observacoes,
               'new_path': router.to_path(new),
               'observacoes': pesquisa.fetch()
               }
    return TemplateResponse(context, router.to_path('observacoes/admin/home.html'))
