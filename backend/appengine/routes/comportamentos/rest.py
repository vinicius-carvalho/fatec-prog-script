# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from comportamento_app import facade


def index():
    cmd = facade.list_comportamentos_cmd()
    comportamento_list = cmd()
    short_form=facade.comportamento_short_form()
    comportamento_short = [short_form.fill_with_model(m) for m in comportamento_list]
    return JsonResponse(comportamento_short)


def save(**comportamento_properties):
    cmd = facade.save_comportamento_cmd(**comportamento_properties)
    return _save_or_update_json_response(cmd)


def update(comportamento_id, **comportamento_properties):
    cmd = facade.update_comportamento_cmd(comportamento_id, **comportamento_properties)
    return _save_or_update_json_response(cmd)


def delete(comportamento_id):
    facade.delete_comportamento_cmd(comportamento_id)()


def _save_or_update_json_response(cmd):
    try:
        comportamento = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})
    short_form=facade.comportamento_short_form()
    return JsonResponse(short_form.fill_with_model(comportamento))

