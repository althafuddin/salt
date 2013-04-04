'''
Saltify Module
==============
The Saltify module is designed to install Salt on a remote machine, virtual or
bare metal, using SSH. This module is useful for provisioning machines which
are already installed, but not Salted.

Use of this module requires no configuration in the main cloud configuration
file. However, profiles must still be configured, as described in the saltify
documentation.
'''

# Import python libs
import re
import sys
import time
import yaml
import json
import urllib
import urllib2
import logging
import xml.etree.ElementTree as ET

# Import salt libs
import salt.utils.event
import salt.utils.xmlutil

# Import salt cloud libs
import saltcloud.utils
import saltcloud.config as config

# Get logging started
log = logging.getLogger(__name__)


def __virtual__():
    '''
    Needs no special configuration
    '''
    return 'saltify'


def avail_locations():
    '''
    Because this module is not specific to any cloud providers, there will be
    no locations to list.
    '''
    return {
        'Error': {
            'Not Supported': '--list-locations not supported by Saltify'
        }
    }


def avail_images():
    '''
    Because this module is not specific to any cloud providers, there will be
    no images to list.
    '''
    return {
        'Error': {
            'Not Supported': '--list-images not supported by Saltify'
        }
    }


def avail_sizes():
    '''
    Because this module is not specific to any cloud providers, there will be
    no sizes to list.
    '''
    return {
        'Error': {
            'Not Supported': '--list-sizes not supported by Saltify'
        }
    }


def list_nodes():
    '''
    Because this module is not specific to any cloud providers, there will be
    no nodes to list.
    '''
    return {}


def list_nodes_full():
    '''
    Because this module is not specific to any cloud providers, there will be
    no nodes to list.
    '''
    return {}


def list_nodes_select():
    '''
    Because this module is not specific to any cloud providers, there will be
    no nodes to list.
    '''
    return {}


def create(vm_):
    '''
    Provision a single machine
    '''
    log.info('Provisioning existing machine {0}'.format(vm_['name']))

    if config.get_config_value('deploy', vm_, __opts__) is True:
        deploy_script = script(vm_)
        ssh_username = config.get_config_value('ssh_username', vm_, __opts__)
        deploy_kwargs = {
            'host': vm_['ssh_host'],
            'username': ssh_username,
            'script': deploy_script,
            'name': vm_['name'],
            'deploy_command': '/tmp/deploy.sh',
            'start_action': __opts__['start_action'],
            'sock_dir': __opts__['sock_dir'],
            'conf_file': __opts__['conf_file'],
            'minion_pem': vm_['priv_key'],
            'minion_pub': vm_['pub_key'],
            'keep_tmp': __opts__['keep_tmp'],
            'sudo': config.get_config_value(
                'sudo', vm_, __opts__, default=(ssh_username != 'root')
            ),
            'password': config.get_config_value('password', vm_, __opts__),
            'ssh_keyfile': config.get_config_value(
                'ssh_keyfile', vm_, __opts__
            ),
            'script_args': config.get_config_value(
                'script_args', vm_, __opts__
            ),
            'minion_conf': saltcloud.utils.minion_conf_string(__opts__, vm_)
        }

        deployed = saltcloud.utils.deploy_script(**deploy_kwargs)
        if deployed:
            log.info('Salt installed on {0}'.format(vm_['name']))
        else:
            log.error('Failed to start Salt on host {0}'.format(vm_['name']))

    return {}


def script(vm_):
    '''
    Return the script deployment object
    '''
    minion = saltcloud.utils.minion_conf_string(__opts__, vm_)
    script = saltcloud.utils.os_script(
        config.get_config_value('script', vm_, __opts__),
        vm_, __opts__, minion
    )
    return script


def destroy(name, call=None):
    '''
    Because this module is not specific to any cloud providers, it is not
    possible to destroy a node.
    '''
    return {
        'Error': {
            'Not Supported': '--destroy and --action destroy not supported '
                             'by Saltify'
        }
    }
