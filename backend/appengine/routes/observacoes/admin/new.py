# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import date
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from observacoe_app.commands import SalvarObsComUsuario

from tekton import router
from gaecookie.decorator import no_csrf
from observacoe_app import facade
from routes.observacoes import admin
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
@login_not_required
def index():
    return TemplateResponse({'save_path': router.to_path(save)},'observacoes/admin/form.html')

@no_csrf
@login_not_required
def save(_handler, _logged_user, observacoe_id= None, **observacoe_properties):
    cmd_save_obs = facade.save_observacoe_cmd(**observacoe_properties)
    cmd_user = SalvarObsComUsuario(_logged_user, **observacoe_properties)
    try:
        cmd_user()
    except CommandExecutionException:
        context = {'save_path': router.to_path(save),
                   'errors': cmd_user.errors,
                   'observacoe': observacoe_properties}

        return TemplateResponse(context, 'observacoes/admin/form.html')
    _handler.redirect(router.to_path(admin))

