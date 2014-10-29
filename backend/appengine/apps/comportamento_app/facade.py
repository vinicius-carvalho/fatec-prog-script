# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from comportamento_app.commands import ListComportamentoCommand, SaveComportamentoCommand, UpdateComportamentoCommand, \
    ComportamentoPublicForm, ComportamentoDetailForm, ComportamentoShortForm


def save_comportamento_cmd(**comportamento_properties):
    """
    Command to save Comportamento entity
    :param comportamento_properties: a dict of properties to save on model
    :return: a Command that save Comportamento, validating and localizing properties received as strings
    """
    return SaveComportamentoCommand(**comportamento_properties)


def update_comportamento_cmd(comportamento_id, **comportamento_properties):
    """
    Command to update Comportamento entity with id equals 'comportamento_id'
    :param comportamento_properties: a dict of properties to update model
    :return: a Command that update Comportamento, validating and localizing properties received as strings
    """
    return UpdateComportamentoCommand(comportamento_id, **comportamento_properties)


def list_comportamentos_cmd():
    """
    Command to list Comportamento entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListComportamentoCommand()


def comportamento_detail_form(**kwargs):
    """
    Function to get Comportamento's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return ComportamentoDetailForm(**kwargs)


def comportamento_short_form(**kwargs):
    """
    Function to get Comportamento's short form. just a subset of comportamento's properties
    :param kwargs: form properties
    :return: Form
    """
    return ComportamentoShortForm(**kwargs)

def comportamento_public_form(**kwargs):
    """
    Function to get Comportamento'spublic form. just a subset of comportamento's properties
    :param kwargs: form properties
    :return: Form
    """
    return ComportamentoPublicForm(**kwargs)


def get_comportamento_cmd(comportamento_id):
    """
    Find comportamento by her id
    :param comportamento_id: the comportamento id
    :return: Command
    """
    return NodeSearch(comportamento_id)


def delete_comportamento_cmd(comportamento_id):
    """
    Construct a command to delete a Comportamento
    :param comportamento_id: comportamento's id
    :return: Command
    """
    return DeleteNode(comportamento_id)

