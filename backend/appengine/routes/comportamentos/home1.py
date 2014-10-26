# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_required
from tekton import router
from gaecookie.decorator import no_csrf
from comportamento_app import facade
from routes.comportamentos.admin import new, edit

@login_required
def delete(_handler, comportamento_id):
    facade.delete_comportamento_cmd(comportamento_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    cmd = facade.list_comportamentos_cmd()
    comportamentos = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    short_form = facade.comportamento_short_form()

    def short_comportamento_dict(comportamento):
        comportamento_dct = short_form.fill_with_model(comportamento)
        comportamento_dct['edit_path'] = router.to_path(edit_path, comportamento_dct['id'])
        comportamento_dct['delete_path'] = router.to_path(delete_path, comportamento_dct['id'])
        return comportamento_dct

    short_comportamentos = [short_comportamento_dict(comportamento) for comportamento in comportamentos]
    context = {'comportamentos': short_comportamentos,
               'new_path': router.to_path(new)}
    return TemplateResponse(context)

