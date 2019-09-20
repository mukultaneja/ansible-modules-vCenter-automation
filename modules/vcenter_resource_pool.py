
import os
import yaml
from pyVmomi import vim
from ansible.module_utils.vc import VcAnsibleModule
from ansible.module_utils.specs.vcenter_resource_pool_spec import VcResourcePoolSpec


VC_RESOURCE_POOL_STATES = ['present', 'absent']


def vc_resource_pool_argument_spec():
    return dict(
        cluster_name=dict(type='str', required=False),
        resource_pool_name=dict(type='str', required=True),
        resource_pool_spec=dict(type='str', required=False, default=None),
        state=dict(choices=VC_RESOURCE_POOL_STATES, required=True)
    )


class VcResourcePool(VcAnsibleModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def manage_states(self):
        state = self.params.get('state')
        if state == "present":
            return self._create()

        if state == "absent":
            return self._delete()

    def _get_cluster(self, cluster_name):
        content = self.si.content
        clusters = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.ClusterComputeResource], recursive=True).view
        cluster = list(filter(lambda c: c.name == cluster_name, clusters))
        cluster = cluster[0] if len(cluster) > 0 else None

        if cluster is None:
            raise ValueError("No cluster {0} found".format(cluster_name))

        return cluster

    def _get_resource_pool(self, resource_pool_name):
        content = self.si.content
        resource_pools = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.ResourcePool], recursive=True).view
        resource_pool = list(filter(lambda r: r.name == resource_pool_name, resource_pools))
        resource_pool = resource_pool[0] if len(resource_pool) > 0 else None

        if resource_pool is None:
            raise ValueError("No Resource Pool {0} found".format(resource_pool_name))

        return resource_pool

    def _prepare_resource_pool_spec(self, resource_pool_spec):
        spec = VcResourcePoolSpec()
        s = self._read_spec(resource_pool_spec)

        return spec.get_resource_pool_spec(s)

    def _read_spec(self, spec):
        return yaml.load(open(os.path.abspath(spec)))

    def _create(self):
        response = dict()
        response['changed'] = False
        cluster_name = self.params.get("cluster_name")
        resource_pool_name = self.params.get("resource_pool_name")
        resource_pool_spec = self.params.get("resource_pool_spec")
        cluster = self._get_cluster(cluster_name)
        spec = self._prepare_resource_pool_spec(resource_pool_spec)

        try:
            cluster.resourcePool.CreateResourcePool(name=resource_pool_name, spec=spec)
        except vim.fault.DuplicateName:
            response['msg'] = 'ResourcePool {0} is already present'.format(resource_pool_name)
        else:
            response['msg'] = "ResourcePool {0} has been created".format(resource_pool_name)
            response['changed'] = True

        return response

    def _delete(self):
        response = dict()
        response['changed'] = False
        resource_pool_name = self.params.get("resource_pool_name")
        resource_pool = self._get_resource_pool(resource_pool_name)

        try:
            task = resource_pool.Destroy_Task()
            self.wait_for_task(task)
        except Exception as error:
            response['msg'] = error
        else:
            response['msg'] = 'Resource Pool {0} has been deleted'.format(resource_pool_name)
            response['changed'] = True

        return response


def main():
    argument_spec = vc_resource_pool_argument_spec()
    response = dict(msg=dict(type='str'))
    module = VcResourcePool(argument_spec=argument_spec, supports_check_mode=True)

    try:
        response = module.manage_states()

    except Exception as error:
        response['msg'] = error
        module.fail_json(**response)

    module.exit_json(**response)


if __name__ == '__main__':
    main()
