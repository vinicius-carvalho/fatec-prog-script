# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from observacoe_app.commands import ListObservacoeCommand, SaveObservacoeCommand, UpdateObservacoeCommand, \
    ObservacoePublicForm, ObservacoeDetailForm, ObservacoeShortForm, SalvarObsComUsuario, DeletarArco


def save_observacoe_cmd(**observacoe_properties):
    """
    Command to save Observacoe entity
    :param observacoe_properties: a dict of properties to save on model
    :return: a Command that save Observacoe, validating and localizing properties received as strings
    """
    return SaveObservacoeCommand(**observacoe_properties)


def update_observacoe_cmd(observacoe_id, **observacoe_properties):
    """
    Command to update Observacoe entity with id equals 'observacoe_id'
    :param observacoe_properties: a dict of properties to update model
    :return: a Command that update Observacoe, validating and localizing properties received as strings
    """
    return UpdateObservacoeCommand(observacoe_id, **observacoe_properties)


def list_observacoes_cmd():
    """
    Command to list Observacoe entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListObservacoeCommand()


def observacoe_detail_form(**kwargs):
    """
    Function to get Observacoe's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return ObservacoeDetailForm(**kwargs)


def observacoe_short_form(**kwargs):
    """
    Function to get Observacoe's short form. just a subset of observacoe's properties
    :param kwargs: form properties
    :return: Form
    """
    return ObservacoeShortForm(**kwargs)

def observacoe_public_form(**kwargs):
    """
    Function to get Observacoe'spublic form. just a subset of observacoe's properties
    :param kwargs: form properties
    :return: Form
    """
    return ObservacoePublicForm(**kwargs)


def get_observacoe_cmd(observacoe_id):
    """
    Find observacoe by her id
    :param observacoe_id: the observacoe id
    :return: Command
    """
    return NodeSearch(observacoe_id)


def delete_observacoe_cmd(observacoe_id):
    """
    Construct a command to delete a Observacoe
    :param observacoe_id: observacoe's id
    :return: Command
    """
    return DeleteNode(observacoe_id)


def salvaobsusuario(_logged_user, **observacoe_properties):

    return SalvarObsComUsuario(_logged_user, **observacoe_properties)

def DeletarArcocmd(obsevacoe):

    return DeletarArco(obsevacoe)