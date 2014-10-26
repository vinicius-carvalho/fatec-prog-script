# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from observacoe_app.commands import SalvarObservacoecomusuario
from tekton import router
from gaecookie.decorator import no_csrf
from observacoe_app import facade
from routes.observacoes import admin


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)},'observacoes/admin/form.html')


def save(_handler, _logged_user, **observacoe_properties):
    cmd = facade.save_observacoe_cmd(**observacoe_properties)
    cmd_user = facade.salvaobsusuario(_logged_user, **observacoe_properties)
    try:
        cmd_user()

    except CommandExecutionException:
        context = {'errors': cmd_user.errors,
                   'observacoe': cmd_user.form

                   }

        return TemplateResponse(context, 'observacoes/admin/form.html')
    _handler.redirect(router.to_path(admin))

