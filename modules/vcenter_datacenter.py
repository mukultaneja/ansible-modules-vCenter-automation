
from pyVmomi import vim
from ansible.module_utils.vc import VcAnsibleModule

VC_DATACENTER_STATES = ['present', 'absent', 'update']


def vc_datacenter_argument_spec():
    return dict(
        dc_name=dict(type='str', required=True),
        state=dict(choices=VC_DATACENTER_STATES, required=False)
    )


class VcDatacenter(VcAnsibleModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def manage_states(self):
        state = self.params.get('state')
        if state == "present":
            return self.create()

        if state == "absent":
            return self.delete()

    def create(self):
        content = self.si.content
        root = content.rootFolder
        response = dict()
        response['changed'] = False
        dc_name = self.params.get("dc_name")

        try:
            root.CreateDatacenter(dc_name)
        except vim.fault.DuplicateName:
            response['msg'] = 'Datacenter {0} is already present'.format(dc_name)
        except Exception as error:
            response['msg'] = error
        else:
            response['msg'] = 'Datacenter {0} has been created'.format(dc_name)
            response['changed'] = True

        return response

    def delete(self):
        content = self.si.content
        root = content.rootFolder
        response = dict()
        response['changed'] = False
        dc_name = self.params.get("dc_name")

        try:
            for dc in root.childEntity:
                if dc.name == dc_name:
                    dc.Destroy()
        except Exception as error:
            response['msg'] = error
        else:
            response['msg'] = 'Datacenter {0} has been removed'.format(dc_name)
            response['changed'] = True

        return response


def main():
    argument_spec = vc_datacenter_argument_spec()
    response = dict(msg=dict(type='str'))
    module = VcDatacenter(argument_spec=argument_spec, supports_check_mode=True)

    try:
        response = module.manage_states()

    except Exception as error:
        response['msg'] = error.__str__()
        module.fail_json(**response)

    module.exit_json(**response)


if __name__ == '__main__':
    main()
