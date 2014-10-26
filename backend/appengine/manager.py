# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import importlib
import sys
import os
import shutil

if 'GAE_SDK' in os.environ:
    SDK_PATH = os.environ['GAE_SDK']

    sys.path.insert(0, SDK_PATH)

    import dev_appserver

    dev_appserver.fix_sys_path()
else:
    print "GAE_SDK environment variable must be on path and point to App Engine's SDK folder"

PROJECT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))
APPS_DIR = os.path.join(PROJECT_DIR, 'apps')
sys.path.insert(1, APPS_DIR)
APPENGINE_DIR = os.path.join(PROJECT_DIR, 'appengine')
WEB_DIR = os.path.join(APPENGINE_DIR, 'routes')
TEMPLATES_DIR = os.path.join(APPENGINE_DIR, 'templates')
# Templates

MODEL_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class %(model)s(Node):
%(properties)s

'''

COMMANDS_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from %(app_path)s.%(app)s_model import %(model)s



class %(model)sSaveForm(ModelForm):
    """
    Form used to save and update %(model)s
    """
    _model_class = %(model)s
    _include = [%(form_properties)s]


class %(model)sForm(ModelForm):
    """
    Form used to expose %(model)s's properties for list or json
    """
    _model_class = %(model)s




class Save%(model)sCommand(SaveCommand):
    _model_form_class = %(model)sSaveForm


class Update%(model)sCommand(UpdateNode):
    _model_form_class = %(model)sSaveForm


class List%(model)sCommand(ModelSearchCommand):
    def __init__(self):
        super(List%(model)sCommand, self).__init__(%(model)s.query_by_creation())

'''

FACADE_TEMPLATE = r'''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from %(app_path)s.%(app)s_commands import List%(model)sCommand, Save%(model)sCommand, Update%(model)sCommand, %(model)sForm


def save_%(model_underscore)s_cmd(**%(model_underscore)s_properties):
    """
    Command to save %(model)s entity
    :param %(model_underscore)s_properties: a dict of properties to save on model
    :return: a Command that save %(model)s, validating and localizing properties received as strings
    """
    return Save%(model)sCommand(**%(model_underscore)s_properties)


def update_%(model_underscore)s_cmd(%(model_underscore)s_id, **%(model_underscore)s_properties):
    """
    Command to update %(model)s entity with id equals '%(model_underscore)s_id'
    :param %(model_underscore)s_properties: a dict of properties to update model
    :return: a Command that update %(model)s, validating and localizing properties received as strings
    """
    return Update%(model)sCommand(%(model_underscore)s_id, **%(model_underscore)s_properties)


def list_%(model_underscore)ss_cmd():
    """
    Command to list %(model)s entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return List%(model)sCommand()


def %(model_underscore)s_form(**kwargs):
    """
    Function to get %(model)s's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return %(model)sForm(**kwargs)


def get_%(model_underscore)s_cmd(%(model_underscore)s_id):
    """
    Find %(model_underscore)s by her id
    :param %(model_underscore)s_id: the %(model_underscore)s id
    :return: Command
    """
    return NodeSearch(%(model_underscore)s_id)



def delete_%(model_underscore)s_cmd(%(model_underscore)s_id):
    """
    Construct a command to delete a %(model)s
    :param %(model_underscore)s_id: %(model_underscore)s's id
    :return: Command
    """
    return DeleteNode(%(model_underscore)s_id)

'''
HOME_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import %(app)s_facade
from routes.%(web_name)s import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = %(app)s_facade.list_%(model_underscore)ss_cmd()
    %(model_underscore)ss = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    %(model_underscore)s_form = %(app)s_facade.%(model_underscore)s_form()

    def localize_%(model_underscore)s(%(model_underscore)s):
        %(model_underscore)s_dct = %(model_underscore)s_form.fill_with_model(%(model_underscore)s)
        %(model_underscore)s_dct['edit_path'] = router.to_path(edit_path, %(model_underscore)s_dct['id'])
        %(model_underscore)s_dct['delete_path'] = router.to_path(delete_path, %(model_underscore)s_dct['id'])
        return %(model_underscore)s_dct

    localized_%(model_underscore)ss = [localize_%(model_underscore)s(%(model_underscore)s) for %(model_underscore)s in %(model_underscore)ss]
    context = {'%(model_underscore)ss': localized_%(model_underscore)ss,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, '%(app)ss/%(app)s_home.html')


def delete(%(model_underscore)s_id):
    %(app)s_facade.delete_%(model_underscore)s_cmd(%(model_underscore)s_id)()
    return RedirectResponse(router.to_path(index))

'''

NEW_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import %(app)s_facade
from routes import %(web_name)s
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, '%(web_name)s/%(app)s_form.html')


def save(**%(model_underscore)s_properties):
    cmd = %(app)s_facade.save_%(model_underscore)s_cmd(**%(model_underscore)s_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   '%(model_underscore)s': %(model_underscore)s_properties}

        return TemplateResponse(context, '%(web_name)s/%(app)s_form.html')
    return RedirectResponse(router.to_path(%(web_name)s))

'''

EDIT_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from %(app_name)s import %(app)s_facade
from routes import %(web_name)s
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(%(model_underscore)s_id):
    %(model_underscore)s = %(app)s_facade.get_%(model_underscore)s_cmd(%(model_underscore)s_id)()
    %(model_underscore)s_form = %(app)s_facade.%(model_underscore)s_form()
    context = {'save_path': router.to_path(save, %(model_underscore)s_id), '%(model_underscore)s': %(model_underscore)s_form.fill_with_model(%(model_underscore)s)}
    return TemplateResponse(context, '%(web_name)s/%(app)s_form.html')


def save(%(model_underscore)s_id, **%(model_underscore)s_properties):
    cmd = %(app)s_facade.update_%(model_underscore)s_cmd(%(model_underscore)s_id, **%(model_underscore)s_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, '%(model_underscore)s': %(model_underscore)s_properties}

        return TemplateResponse(context, '%(web_name)s/%(app)s_form.html')
    return RedirectResponse(router.to_path(%(web_name)s))

'''

REST_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from %(app_name)s import %(app)s_facade


def index():
    cmd = %(app)s_facade.list_%(model_underscore)ss_cmd()
    %(model_underscore)s_list = cmd()
    %(model_underscore)s_form=%(app)s_facade.%(model_underscore)s_form()
    %(model_underscore)s_dcts = [%(model_underscore)s_form.fill_with_model(m) for m in %(model_underscore)s_list]
    return JsonResponse(%(model_underscore)s_dcts)


def new(_resp, **%(model_underscore)s_properties):
    cmd = %(app)s_facade.save_%(model_underscore)s_cmd(**%(model_underscore)s_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, %(model_underscore)s_id, **%(model_underscore)s_properties):
    cmd = %(app)s_facade.update_%(model_underscore)s_cmd(%(model_underscore)s_id, **%(model_underscore)s_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(%(model_underscore)s_id):
    %(app)s_facade.delete_%(model_underscore)s_cmd(%(model_underscore)s_id)()


def _save_or_update_json_response(cmd, _resp):
    try:
        %(model_underscore)s = cmd()
    except CommandExecutionException:
        _resp.status_code = 400
        return JsonResponse({'errors': cmd.errors})
    %(model_underscore)s_form=%(app)s_facade.%(model_underscore)s_form()
    return JsonResponse(%(model_underscore)s_form.fill_with_model(%(model_underscore)s))

'''

HOME_HTML_TEMPLATE = '''{%% extends '%(web_name)s/%(app)s_base.html' %%}
{%% block body %%}
    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <h1>{%% trans %%}This is a generic home for %(app_name)s {%% endtrans %%}  </h1>
                <a href="{{ new_path }}" class="btn btn-success">{%% trans %%}Create New %(model)s{%% endtrans %%}</a>
                <hr/>
                <h2>{%% trans %%}List of %(model)ss{%% endtrans %%}</h2>
                <table class="table table-striped table-hover">
                    <thead>
                    <tr>
                        <th/>
                        <th>{%% trans %%}Id{%% endtrans %%}</th>
                        <th>{%% trans %%}Creation{%% endtrans %%}</th>
%(headers)s
                    </tr>
                    </thead>
                    <tbody>
                    {%% for %(model_underscore)s in %(model_underscore)ss %%}
                        <tr>
                            <td><a href="{{ %(model_underscore)s.edit_path }}" class="btn btn-success btn-sm"><i
                                    class="glyphicon glyphicon-pencil"></i></a></td>
                            <td>{{ %(model_underscore)s.id }}</td>
                            <td>{{ %(model_underscore)s.creation }}</td>
%(columns)s
                            <td>
                                <form action="{{ %(model_underscore)s.delete_path }}" method="post" onsubmit="return confirm('{{_('Are you sure to delete? Press cancel to avoid deletion.')}}');">
                                    {{ csrf_input() }}
                                    <button class="btn btn-danger btn-sm"><i
                                            class="glyphicon glyphicon-trash"></i></button>
                                </form>
                            </td>
                        </tr>
                    {%% endfor %%}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
{%% endblock %%}'''

FORM_HTML_TEMPLATE = '''{%% extends '%(web_name)s/%(app)s_base.html' %%}
{%% block body %%}
    {%% set %(model_underscore)s=%(model_underscore)s or None %%}
    {%% set errors=errors or None %%}
    <div class="container">
        <div class="row">
            <div class="col-md-6 col-md-offset-3">
                <br/>

                <div class="well">
                    <h1 class="text-center">{%% trans %%}%(model)s Form{%% endtrans %%}</h1>

                    <form action="{{ save_path }}" method="post" role="form">
                        {{ csrf_input() }}
%(inputs)s
                        <button type="submit" class="btn btn-success">{%% trans %%}Save{%% endtrans %%}</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

{%% endblock %%}'''


def _create_dir_if_not_existing(package_path):
    if not os.path.exists(package_path):
        os.mkdir(package_path)


def _create_file_if_not_existing(file_path, content=''):
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as f:
            f.write(content.encode('utf8'))


def _create_package(package_path):
    _create_dir_if_not_existing(package_path)
    _create_file_if_not_existing(os.path.join(package_path, '__init__.py'))


def _create_app(name, app_path, model, *properties):
    properties = '\n'.join(parse_propety(p) for p in properties)
    properties = properties or '    pass'
    _create_package(app_path)
    _create_file_if_not_existing(os.path.join(app_path, '%s_model.py' % name),
                                 MODEL_TEMPLATE % {'model': model, 'properties': properties})


def parse_propety(p):
    name, type_alias = p.split(':')
    types = {'string': 'ndb.StringProperty(required=True)',
             'date': 'ndb.DateProperty(required=True)',
             'datetime': 'ndb.DateTimeProperty(required=True)',
             'int': 'ndb.IntegerProperty(required=True)',
             'float': 'ndb.FloatProperty(required=True)',
             'decimal': 'property.SimpleDecimal(required=True)',
             'currency': 'property.SimpleCurrency(required=True)',
             'bool': 'ndb.BooleanProperty(required=True)'}
    return '    %s = %s' % (name, types[type_alias])


def init_app(name, model, *properties):
    _title('Creating app package')
    app_path = os.path.join(APPS_DIR, name + '_app')
    _create_app(name, app_path, model, *properties)


PROPERTY = '%(model)s.%(property)s'


def _build_properties(model, properties):
    return ', \n                '.join([PROPERTY % {'model': model, 'property': p} for p in properties])


def _model_properties(app, model):
    app_path = app + '_app'
    model_module = importlib.import_module(app_path + '.%s_model' % app)
    model_class = getattr(model_module, model)
    properties = set(model_class._properties.keys())
    properties = properties.difference(set(['class']))
    return properties


def commands_code_for(app, model):
    app_path = app + '_app'
    properties = _model_properties(app, model)
    full_properties = _build_properties(model, properties)
    form_properties = properties.difference(set(['creation']))
    form_properties = _build_properties(model, form_properties)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'full_properties': full_properties,
           'form_properties': form_properties}
    return COMMANDS_TEMPLATE % dct


def _title(param):
    n = 15
    print ('- ' * n) + param + (' -' * n)


def init_commands(app, model):
    print APPS_DIR
    app_path = os.path.join(APPS_DIR, app + '_app')
    commands_script = os.path.join(app_path, '%s_commands.py' % app)
    content = commands_code_for(app, model)
    _create_file_if_not_existing(commands_script, content)
    return content


def _to_app_name(app):
    return app + '_app'


def _to_undescore_case(model):
    model_underscore = model[0].lower() + model[1:]
    return ''.join(('_' + letter.lower() if letter.isupper() else letter) for letter in model_underscore)


def facade_code_for(app, model):
    app_path = _to_app_name(app)
    model_underscore = _to_undescore_case(model)

    dct = {'app': app, 'app_path': app_path, 'model': model, 'model_underscore': model_underscore}
    return FACADE_TEMPLATE % dct


def _to_app_path(app):
    return os.path.join(APPS_DIR, app + '_app')


def init_facade(app, model):
    app_path = _to_app_path(app)
    facade_script = os.path.join(app_path, '%s_facade.py' % app)
    content = facade_code_for(app, model)
    _create_file_if_not_existing(facade_script, content)
    return content


def _to_web_name(app):
    return app + 's'


def _to_web_path(app):
    return os.path.join(WEB_DIR, _to_web_name(app))


def _to_template_path(app):
    return os.path.join(TEMPLATES_DIR, _to_web_name(app))


def init_web(app):
    web_path = _to_web_path(app)
    _create_package(web_path)


def init_web_admin(app):
    web_path = _to_web_path(app)
    _create_package(web_path)


def code_for_home_script(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    return HOME_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_undescore_case(model),
                                   'web_name': web_name,
                                   'app': app}


def init_home_script(app, model):
    app_web_path = _to_web_path(app)
    home_script = os.path.join(app_web_path, 'home.py')
    content = code_for_home_script(app, model)
    _create_file_if_not_existing(home_script, content)
    return content


def code_for_form_script(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    return NEW_SCRIPT_TEMPLATE % {'app_name': app_name,
                                  'model_underscore': _to_undescore_case(model),
                                  'web_name': web_name,
                                  'app': app}


def code_for_edit_script(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    return EDIT_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_undescore_case(model),
                                   'web_name': web_name,
                                   'app': app}


def init_new_script(app, model):
    app_web_path = _to_web_path(app)
    form_script = os.path.join(app_web_path, 'new.py')
    content = code_for_form_script(app, model)
    _create_file_if_not_existing(form_script, content)
    return content


def init_edit_script(app, model):
    app_web_path = _to_web_path(app)
    form_script = os.path.join(app_web_path, 'edit.py')
    content = code_for_edit_script(app, model)
    _create_file_if_not_existing(form_script, content)
    return content


def code_for_rest_script(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    return REST_SCRIPT_TEMPLATE % {'app_name': app_name,
                                   'model_underscore': _to_undescore_case(model),
                                   'web_name': web_name,
                                   'app': app}


def init_rest_script(app, model):
    app_web_path = _to_web_path(app)
    rest_script = os.path.join(app_web_path, 'rest.py')
    content = code_for_rest_script(app, model)
    _create_file_if_not_existing(rest_script, content)
    return content


APP_BASE_HTML_TEMPLATE = '''{%% extends 'base/base.html' %%}
{%% block tabs %%}
    {{ select_tab('%(app_name_upper)s') }}
{%% endblock %%}'''


def init_html_templates(app):
    template_path = _to_template_path(app)
    content = APP_BASE_HTML_TEMPLATE % {'app_name_upper': _to_web_name(app).upper()}
    _create_dir_if_not_existing(template_path)
    base_dir = os.path.join(template_path, '%s_base.html' % app)
    _create_file_if_not_existing(base_dir, content)


def _to_label(label):
    names = label.split('_')
    upper_names = [n[0].upper() + n[1:] for n in names]
    return ' '.join(upper_names)


def _to_html_table_header(properties):
    template = ' ' * 24 + '<th>{%% trans %%}%s{%% endtrans %%}</th>'
    properties = [_to_label(p) for p in properties]
    rendered = [template % p for p in properties]
    return '\n'.join(rendered)


def _to_html_table_columns(model_undescore, properties):
    template = ' ' * 28 + '<td>{{ %(model_underscore)s.%(property)s }}</td>'

    rendered = [template % {'model_underscore': model_undescore, 'property': p} for p in properties]
    return '\n'.join(rendered)


def _to_html_form_inputs(model_undescore, properties):
    template = "{{ form_input(_('%(label)s'),'%(property)s',%(model_underscore)s.%(property)s,errors.%(property)s) }}"
    template = ' ' * 24 + template

    rendered = [template % {'model_underscore': model_undescore, 'property': p, 'label': _to_label(p)} for p in
                properties]
    return '\n'.join(rendered)


def code_for_home_html(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    properties = _model_properties(app, model)
    properties = properties.difference(set(['creation']))
    model_undescore = _to_undescore_case(model)
    return HOME_HTML_TEMPLATE % {'app_name': app_name,
                                 'model_underscore': model_undescore,
                                 'model': model,
                                 'web_name': web_name,
                                 'headers': _to_html_table_header(properties),
                                 'columns': _to_html_table_columns(model_undescore, properties),
                                 'app': app}


def code_for_form_html(app, model):
    web_name = _to_web_name(app)
    app_name = _to_app_name(app)
    properties = _model_properties(app, model)
    properties = properties.difference(set(['creation']))
    model_undescore = _to_undescore_case(model)
    return FORM_HTML_TEMPLATE % {'app_name': app_name,
                                 'model_underscore': model_undescore,
                                 'model': model,
                                 'web_name': web_name,
                                 'inputs': _to_html_form_inputs(model_undescore, properties),
                                 'app': app}


def init_home_html(app, model):
    app_template_path = _to_template_path(app)
    home_script = os.path.join(app_template_path, '%s_home.html' % app)
    content = code_for_home_html(app, model)
    _create_file_if_not_existing(home_script, content)
    return content


def init_form_html(app, model):
    app_template_path = _to_template_path(app)
    form_script = os.path.join(app_template_path, '%s_form.html' % app)
    content = code_for_form_html(app, model)
    _create_file_if_not_existing(form_script, content)
    return content


def scaffold(app, model, *properties):
    init_app(app, model, *properties)
    _title('commands.py')
    print init_commands(app, model)
    _title('facade.py')
    print init_facade(app, model)

    _title('creating routes folder')
    init_web(app)
    _title('routes home.py')
    print init_home_script(app, model)

    _title('routes.new.py')
    print init_new_script(app, model)
    _title('routes.edit.py')
    print init_edit_script(app, model)
    _title('routes rest.py')
    print init_rest_script(app, model)
    _title('creating template folder ans base.html')
    init_html_templates(app)
    _title('templates/home.html')
    print init_home_html(app, model)

    _title('templates/form.html')
    print init_form_html(app, model)


def delete_app(app):
    flag = raw_input('Are you sure you want delete app %s (yes or no)? ' % app)
    if flag.lower() == 'yes':
        app_dir = os.path.join(APPS_DIR, app + '_app')
        shutil.rmtree(app_dir)

        template_dir = os.path.join(TEMPLATES_DIR, app + 's')
        shutil.rmtree(template_dir)
        web_dir = os.path.join(WEB_DIR, app + 's')
        shutil.rmtree(web_dir)


FUNC_DICT = {'model': init_app, 'app': scaffold, 'delete': delete_app}
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'Commands available:'
        print '\n    '.join([''] + FUNC_DICT.keys())
        print 'both model or app must be folowed by <app> <model>'
    elif len(sys.argv) >= 3:
        fcn = FUNC_DICT.get(sys.argv[1])
        if fcn:
            fcn(*sys.argv[2:])
        else:
            print 'Invalid command: %s' % sys.argv[1]
    else:
        print 'Must use command %s followed by params: <app>  <model>' % sys.argv[1]



