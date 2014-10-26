# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_required
from tekton import router
from gaecookie.decorator import no_csrf
from comportamento_app import facade
from routes.comportamentos import admin


@login_required
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'comportamentos/admin/form.html')


@login_required
def save(_handler, comportamento_id=None, **comportamento_properties):
    cmd = facade.save_comportamento_cmd(**comportamento_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'comportamento': cmd.form}

        return TemplateResponse(context, 'comportamentos/admin/form.html')
    _handler.redirect(router.to_path(admin))

