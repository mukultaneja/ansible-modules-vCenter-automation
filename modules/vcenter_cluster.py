
import os
import yaml
from pyVmomi import vim
from ansible.module_utils.vc import VcAnsibleModule
from ansible.module_utils.specs.vcenter_cluster_spec import VcClusterSpec


VC_CLUSTER_STATES = ['present', 'absent', 'update']


def vc_cluster_argument_spec():
    return dict(
        dc_name=dict(type='str', required=False),
        cluster_name=dict(type='str', required=True),
        cluster_spec=dict(type='str', required=False, default=None),
        state=dict(choices=VC_CLUSTER_STATES, required=False)
    )


class VcCluster(VcAnsibleModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def manage_states(self):
        state = self.params.get('state')
        if state == "present":
            return self._create()

        if state == "update":
            return self._update()

        if state == "absent":
            return self._delete()

    def _get_datacenter(self, dc_name):
        content = self.si.content
        root = content.rootFolder
        dc = list(filter(lambda d: d.name == dc_name, root.childEntity))
        dc = dc[0] if len(dc) > 0 else None

        if dc is None:
            raise ValueError("No datacenter {0} found".format(dc_name))

        return dc

    def _get_cluster(self, cluster_name):
        content = self.si.content
        clusters = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.ClusterComputeResource], recursive=True).view
        cluster = list(filter(lambda c: c.name == cluster_name, clusters))
        cluster = cluster[0] if len(cluster) > 0 else None

        if cluster is None:
            raise ValueError("No cluster {0} found".format(cluster_name))

        return cluster

    def _prepare_cluster_spec(self, cluster_spec):
        spec = VcClusterSpec()
        s = self._read_spec(cluster_spec)

        return spec.get_cluster_spec(s)

    def _read_spec(self, spec):
        return yaml.load(open(os.path.abspath(spec)))

    def _create(self):
        response = dict()
        response['changed'] = False
        dc_name = self.params.get("dc_name")
        cluster_name = self.params.get("cluster_name")
        cluster_spec = self.params.get("cluster_spec")
        dc = self._get_datacenter(dc_name)
        spec = self._prepare_cluster_spec(cluster_spec)

        try:
            dc.hostFolder.CreateCluster(name=cluster_name, spec=spec)
        except vim.fault.DuplicateName:
            response['msg'] = 'Cluster {0} is already present'.format(cluster_name)
        else:
            response['msg'] = "Cluster {0} has been created".format(cluster_name)
            response['changed'] = True

        return response

    def _update(self):
        response = dict()
        response['changed'] = False
        cluster_name = self.params.get("cluster_name")
        cluster_spec = self.params.get("cluster_spec")
        spec = self._prepare_cluster_spec(cluster_spec)

        try:
            cluster = self._get_cluster(cluster_name)
            task = cluster.ReconfigureCluster_Task(spec=spec, modify=False)
            self.wait_for_task(task)
        except Exception as error:
            response['msg'] = error
        else:
            response['msg'] = "Cluster {0} has been updated".format(cluster_name)
            response['changed'] = True

        return response

    def _delete(self):
        response = dict()
        response['changed'] = False
        cluster_name = self.params.get("cluster_name")

        try:
            cluster = self._get_cluster(cluster_name)
            task = cluster.Destroy_Task()
            self.wait_for_task(task)
        except Exception as error:
            response['msg'] = error
        else:
            response['msg'] = "Cluster {0} has been deleted".format(cluster_name)
            response['changed'] = True

        return response


def main():
    argument_spec = vc_cluster_argument_spec()
    response = dict(msg=dict(type='str'))
    module = VcCluster(argument_spec=argument_spec, supports_check_mode=True)

    try:
        response = module.manage_states()

    except Exception as error:
        response['msg'] = error
        module.fail_json(**response)

    module.exit_json(**response)


if __name__ == '__main__':
    main()
