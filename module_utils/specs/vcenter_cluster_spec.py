
from pyVmomi import vim


class VcClusterSpec():
    def get_cluster_spec(self, config):
        spec = vim.cluster.ConfigSpec()

        if config is None:
            return spec

        spec.dasConfig = self._das_config(config.get("dasConfig", None))
        spec.drsConfig = self._drs_config(config.get("drsConfig", None))

        return spec

    def _das_config(self, config):
        das_config = vim.cluster.DasConfigInfo()

        if config is None:
            return das_config

        if "defaultVmSettings" in config:
            das_vm_settings = vim.cluster.DasVmSettings()
            for k, v in config["defaultVmSettings"].items():
                das_vm_settings.__setattr__(k, v)
            das_config.__setattr__("defaultVmSettings", das_vm_settings)
            del config["defaultVmSettings"]

        for k, v in config.items():
            das_config.__setattr__(k, v)

        return das_config

    def _drs_config(self, config):
        drs_config = vim.cluster.DrsConfigInfo()

        if config is None:
            return drs_config

        default_vm_bheavior = {
            "manual": vim.cluster.DrsConfigInfo.DrsBehavior.manual,
            "fullyAutomated": vim.cluster.DrsConfigInfo.DrsBehavior.fullyAutomated,
            "partiallyAutomated": vim.cluster.DrsConfigInfo.DrsBehavior.manual.partiallyAutomated
        }

        for k, v in config.items():
            v = default_vm_bheavior[v] if k == "defaultVmBehavior" else v
            drs_config.__setattr__(k, v)

        return drs_config

    def _dpm_config(self, config):
        dpm_config = vim.cluster.DpmConfigInfo()

        if config is None:
            return dpm_config

        default_dpm_behavior = {
            "automated": vim.cluster.DpmConfigInfo.DpmBehavior.automated,
            "manual": vim.cluster.DpmConfigInfo.DpmBehavior.manual
        }

        for k, v in config.items():
            v = default_dpm_behavior[v] if k == "defaultDpmBehavior" else v
            dpm_config.__setattr__(k, v)
