# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from observacoe_app import facade
from routes.observacoes import admin


@no_csrf
def index(observacoe_id):
    observacoe = facade.get_observacoe_cmd(observacoe_id)()
    detail_form = facade.observacoe_detail_form()
    context = {'save_path': router.to_path(save, observacoe_id), 'observacoe': detail_form.fill_with_model(observacoe)}
    return TemplateResponse(context, 'observacoes/admin/form.html')


def save(_handler, observacoe_id, **observacoe_properties):
    cmd = facade.update_observacoe_cmd(observacoe_id, **observacoe_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'observacoe': cmd.form}

        return TemplateResponse(context, 'observacoes/admin/form.html')
    _handler.redirect(router.to_path(admin))

