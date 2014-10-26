# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from comportamento_app import facade
from routes.comportamentos import admin


@login_not_required
@no_csrf
def index():
    cmd = facade.list_comportamentos_cmd()
    comportamentos = cmd()
    public_form = facade.comportamento_public_form()
    comportamento_public_dcts = [public_form.fill_with_model(comportamento) for comportamento in comportamentos]
    context = {'comportamentos': comportamento_public_dcts,'admin_path':router.to_path(admin)}
    return TemplateResponse(context)

