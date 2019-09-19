

import os
import sys
import ssl
import time
from pyVmomi import vim
from pyVim import connect
from ansible.module_utils.basic import AnsibleModule

sys.path.append("/Users/mtaneja/Work/Projects/VMware/lcm/vcps/vcps-core/vcps-test-root/packages3.7/")


def vc_argument_spec():
    return dict(
        user=dict(type='str', required=False, default=os.environ.get('env_user')),
        password=dict(type='str', required=False, no_log=True, default=os.environ.get('env_password')),
        host=dict(type='str', required=False, default=os.environ.get('env_host')),
        port=dict(type='int', required=False, default=os.environ.get('env_port')),
    )


class VcAnsibleModule(AnsibleModule):
    def __init__(self, *args, **kwargs):
        argument_spec = vc_argument_spec()
        argument_spec.update(kwargs.get('argument_spec', dict()))
        kwargs['argument_spec'] = argument_spec

        super(VcAnsibleModule, self).__init__(*args, **kwargs)
        self.login()

    def login(self):
        try:
            user = self.params.get('user')
            password = self.params.get('password')
            host = self.params.get('host')
            port = self.params.get("port")
            self.si = connect.SmartConnect(
                host=host, user=user, pwd=password, port=port, sslContext=ssl._create_unverified_context())

        except Exception as error:
            error = 'Login failed for user {0} on host {1}'
            raise Exception(error.format(user, host))

    def wait_for_task(self, task):
        while task.info.state != vim.TaskInfo.State.success:
            time.sleep(60)

        return task.info.state
