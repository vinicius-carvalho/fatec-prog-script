# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
import obs_app.model

@no_csrf
def index():
    query= obs_app.model.Obs.query()
    contexto={'historico': query.fetch()}
    return TemplateResponse(contexto)





