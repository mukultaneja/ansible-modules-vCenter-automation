---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---
<!-- Setting Use Case -->
<div class="environment-settings col-12" id="environment-settings">
<h2>Environment Settings</h2>
<hr />
<ol>
<li>
<h3>Login</h3>
</li>
<pre>
<code>
 - name: vCenterAnsibleAutomation
   hosts: localhost
   environment:
    env_user: vCenter_USER_NAME
    env_password: vCenter_USER_PASSWORD
    env_host: vCenter_URL
    env_port: vCenter_Port

</code>
</pre>
<p>
vCenter Ansible Modules prefer following two ways to set login variables for vCenter instance.
</p>
<ol>
<li>
<b>Environment Variables - </b>
The end user can set login variables in the environment as shown above. Once they are set, modules will use these variables for all the subsequent resource operations automatically.
</li>
<li>
<b>Local Variables - </b>
The end user can set login variables for specific module(s) as local variables. This approach gives more freedom to the end user to execute specific module(s) on specific vCenter instance(s).
</li>
</ol>
<br />
<p>
By default, the priority will be given to <b>Local Variables</b> than <b>Environment Variables.</b>
</p>
<li>
<h3>Response</h3>
<p>vCenter Ansible Modules provide sort of a unanimous response across all operations. The response shall contain atleast following properties,</p>
<ul>
<li>msg - the success/failure string corresponding to the resource</li>
<li>changed - "true" if resource has been modified at the infrastrucutre level else "false"
</li>
</ul>
</li>
</ol>
</div>

<!--                  -->
<!-- vCenter Datacenter Use Case -->
<div class="datacenter col-12" id="datacenter">
<h2>vCenter Datacenter</h2>
<hr />
<ol>
<li>
<h3>vCenter Datacenter States</h3>
<ul>
<li>
<h5>Create vCenter Datacenter</h5>
</li>
<pre>
<code>
 - name: create vCenter datacenter
   vcenter_datacenter:
    dc_name: test_datacenter
    state: present

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>dc_name - (Required) Name of the new vCenter datacenter</li>
<li>state == present (Required) to create datacenter</li>
</ul>
<li>
<h5>Delete vCenter Datacenter</h5>
</li>
<pre>
<code>
 - name: delete vCenter datacenter
   vcenter_datacenter:
    dc_name: test_datacenter
    state: absent

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>dc_name - (Required) Name of the vCenter datacenter</li>
<li>state == absent (Required) to delete datacenter</li>
</ul>
</ul>
</li>
</ol>
</div>

<!--                  -->
<!-- vCenter Cluster Use Case -->
<div class="cluster col-12" id="cluster">
<h2>vCenter Cluster</h2>
<hr />
<ol>
<li>
<h3>vCenter Cluster States</h3>
<ul>
<li>
<h5>Create vCenter Cluster</h5>
</li>
<pre>
<code>
 - name: create vCenter cluster
   vcenter_cluster:
    dc_name: test_datacenter
    cluster_name: test_cluster
    cluster_spec: <!CLUSTER_SPEC_LOCATION!>
    state: present

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>dc_name - (Required) Name of the vCenter datacenter</li>
<li>cluster_name - (Required) Name of the new vCenter cluster</li>
<li>cluster_spec - (Optional) Cluster <a href="#cluster-spec">spec</a> location</li>
<li>state == present (Required) to create cluster</li>
</ul>
<li>
<h5>Update vCenter cluster</h5>
</li>
<pre>
<code>
- name: update cluster
  vcenter_cluster:
    cluster_name: test_cluster
    cluster_spec: <!CLUSTER_SPEC_LOCATION!>
    state: update

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>cluster_name - (Required) Name of the vCenter cluster</li>
<li>cluster_spec - (Optional) Cluster <a href="#cluster-spec">spec</a> location</li>
<li>state == update (Required) to update cluster</li>
</ul>
<li>
<h5>Delete vCenter cluster</h5>
</li>
<pre>
<code>
 - name: delete vCenter cluster
  vcenter_cluster:
   cluster_name: test_cluster
   state: absent

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>cluster_name - (Required) Name of the vCenter cluster</li>
<li>state == absent (Required) to delete cluster</li>
</ul>
<li>
<h5 id="cluster-spec">vCenter Cluster Spec</h5>
</li>
<pre>
<code>
    dasConfig:
        admissionControlEnabled: true
        enabled: true
        failoverLevel: 1
        defaultVmSettings:
            isolationResponse: powerOff
            restartPriority: high
    drsConfig:
        enabled: true
        defaultVmBehavior: fullyAutomated
        vmotionRate: 4
    dpmConfig:
        defaultDpmBehavior: manual
        enabled: true

</code>
</pre>
Reference:-
<a href="https://pubs.vmware.com/vi-sdk/visdk250/ReferenceGuide/vim.cluster.ConfigSpecEx.html" target="_blank">ClusterConfigSpecEx</a>
</ul>
</li>
</ol>
</div>

<!-- vCenter Cluster Use Case -->
<div class="resource-pool col-12" id="resource-pool">
<h2>vCenter Resource Pool</h2>
<hr />
<ol>
<ul>
<li>
<h3>vCenter Resource Pool States</h3>
</li>
<li>
<h5>Create Resource Pool</h5>
</li>
<pre>
<code>
 - name: create resource pool
   vcenter_resource_pool:
    cluster_name: test_cluster
    resource_pool_name: test_resource_pool
    resource_pool_spec: <!RESOURCE_POOL_SPEC_LOCATION!>
    state: present

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>cluster_name - (Required) Name of the vCenter cluster</li>
<li>resource_pool_name - (Required) Name of the new resource pool</li>
<li>resource_pool_spec - (Optional) Resource Pool <a href="#resource-pool-spec">spec</a> location</li>
<li>state == present (Required) to create resource pool</li>
</ul>
<li>
<h5>Delete Resource Pool</h5>
</li>
<pre>
<code>
 - name: delete resource pool
   vcenter_resource_pool:
    resource_pool_name: hello_world_resource_pool
    state: absent

</code>
</pre>
<h5>Argument Reference</h5>
<ul>
<li>user - (Optional) - vCenter user name</li>
<li>password - (Optional) - vCenter password</li>
<li>host - (Optional) - vCenter host name</li>
<li>port - (Optional) - vCenter port number</li>
<li>resource_pool_name - (Required) Name of the resource pool</li>
<li>state == absent (Required) to delete resource pool</li>
</ul>
<li>
<h5 id="resource-pool-spec">Resource Pool Spec</h5>
</li>
<pre>
<code>
    changeVersion: "1"
    cpuAllocation:
      expandableReservation: true
      limit: -1
      reservation: 0
      shares:
        level: normal
    memoryAllocation:
      expandableReservation: true
      limit: -1
      reservation: 0
      shares:
        level: normal

</code>
</pre>
Reference:-
<a href="https://pubs.vmware.com/vi3/sdk/ReferenceGuide/vim.ResourcePool.html" target="_blank">ResourcePool</a>
</ul>
</ol>
</div>