"""
Model classes for AppDynamics REST API
"""

from . import JsonObject, JsonList
from appd.time import from_ts

class HourlyLicenseUsage(JsonObject):

    FIELDS = {
        'id': '',
        'account_id': 'accountId',
        'max_units_used': 'maxUnitsUsed',
        'min_units_used': 'minUnitsUsed',
        'avg_units_used': 'avgUnitsUsed',
        'total_units_used': 'totalUnitsUsed',
        'sample_count': 'sampleCount',
        'avg_units_allowed': 'avgUnitsAllowed',
        'avg_units_provisioned': 'avgUnitsProvisioned',
        'license_module': 'agentType',
        'created_on_ms': 'createdOn',
    }

    def __init__(self, id=0, account_id=0, max_units_used=0, min_units_used=0, avg_units_used=0, total_units_used=0,
                 sample_count=0, avg_units_allowed=0, avg_units_provisioned=None, license_module=None,
                 created_on_ms=0):
        (self.id, self.account_id, self.max_units_used, self.min_units_used, self.avg_units_used, self.total_units_used,
         self.sample_count, self.avg_units_allowed, self.avg_units_provisioned, self.license_module,
         self.created_on_ms) = (id, account_id, max_units_used, min_units_used, avg_units_used, total_units_used,
                                sample_count, avg_units_allowed, avg_units_provisioned, license_module,
                                created_on_ms)

    @property
    def created_on(self):
        """
        :rtype: datetime.datetime
        """
        return from_ts(self.created_on_ms)


class HourlyLicenseUsageList(JsonList):

    def __init__(self, initial_list=None):
        super(HourlyLicenseUsageList, self).__init__(HourlyLicenseUsage, initial_list)

    def __getitem__(self, i):
        """
        :rtype: HourlyLicenseUsage
        """
        return self.data[i]

    def by_account_id(self, account_id):
        """
        :rtype: HourlyLicenseUsageList
        """
        return HourlyLicenseUsageList([x for x in self.data if x.account_id == account_id])

    def by_license_module(self, license_module):
        """
        :rtype: HourlyLicenseUsageList
        """
        return HourlyLicenseUsageList([x for x in self.data if x.license_module == license_module])


class HourlyLicenseUsages(JsonObject):

    FIELDS = {}

    def __init__(self):
        self.usages = HourlyLicenseUsageList()

    @classmethod
    def from_json(cls, json_dict):
        obj = super(HourlyLicenseUsages, cls).from_json(json_dict)
        obj.usages = HourlyLicenseUsageList.from_json(json_dict['usages'])
        return obj

