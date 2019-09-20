
from pyVmomi import vim


class VcResourcePoolSpec():
    def get_resource_pool_spec(self, config):
        spec = vim.ResourceConfigSpec()

        if config is None:
            return spec

        spec.cpuAllocation = self._resource_allocation(config.get("cpuAllocation"))
        spec.memoryAllocation = self._resource_allocation(config.get("memoryAllocation"))
        spec.changeVersion = config.get("changeVersion")

        return spec

    def _resource_allocation(self, config):
        spec = vim.ResourceAllocationInfo()

        if config is None:
            return spec

        shares_config = {
            "normal": vim.SharesInfo.Level.normal,
            "low": vim.SharesInfo.Level.low,
            "high": vim.SharesInfo.Level.high
        }
        spec.expandableReservation = config.get("expandableReservation", False)
        spec.limit = config.get("limit", -1)
        spec.reservation = config.get("reservation", 0)
        spec.shares = vim.SharesInfo()
        shares = config.get("shares", None)

        if shares:
            level = shares.get("level")
            if level == "custom":
                spec.shares.level = vim.SharesInfo.Level.custom
                spec.shares.shares = shares.get("shares")
            else:
                spec.shares.level = shares_config.get(level)

        return spec
