# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException, CommandParallel
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from observacoe_app.commands import GetDonoObs
from tekton.gae.middleware.json_middleware import JsonResponse, JsonUnsecureResponse
from observacoe_app import facade

def index(_logged_user):
    cmd = facade.list_observacoes_cmd()
    observacoe_list = cmd()
    get_dono_cmd_lista=[GetDonoObs(o) for o in observacoe_list]
    paralelo=CommandParallel(*get_dono_cmd_lista)
    paralelo()

    short_form=facade.observacoe_short_form()
    observacoe_short = [short_form.fill_with_model(m) for m in observacoe_list]
    for observacao,dono_comando in zip(observacoe_short,get_dono_cmd_lista):
        observacao['dono_flag']=(dono_comando.result == _logged_user)
        return JsonResponse(observacoe_short)


def save(_resp, _logged_user,**observacoe_properties):
   cmd = facade.save_observacoe_cmd(**observacoe_properties)
   cmd_user=facade.salvaobsusuario(_logged_user, **observacoe_properties)
   return _save_or_update_json_response(cmd, _resp)


def update(_resp,observacoe_id, **observacoe_properties):
    cmd = facade.update_observacoe_cmd(observacoe_id, **observacoe_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(observacoe_id):
    facade.delete_observacoe_cmd(observacoe_id)()


def _save_or_update_json_response(cmd, _resp):
    try:
        observacoe = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    short_form=facade.observacoe_short_form()
    return JsonResponse(short_form.fill_with_model(observacoe))

