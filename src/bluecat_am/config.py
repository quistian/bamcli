
"""

Global Variables convention:
    * start with UpperCase
    * have no _ character
    * may have mid UpperCase words

"""

Debug = False
Silent = False

Baseurl = ''

ConfigName = 'Test'
ConfigId = 0

ViewName = 'Public'
ViewId = 0

RootId = 0

LegalTLDs = ('ca', 'com', 'edu', 'org')

AuthHeader = {}

ObjectTypes = (
        'Entity',
        'Configuration',
        'View',
        'InternalRootZone',
        'ExternalHostRecord'
        'User',
        'UserGroup'
        'Zone',
        'StartOfAuthority',
        'HostRecord',
        'AliasRecord',
        'MXRecord',
        'TXTRecord',
        'SRVRecord',
        'GenericRecord',
        'HINFORecord',
        'NAPTRRecord',
)

RRObjectTypes = ObjectTypes[6:]

RRTypeMap = {
        'MX': {'obj_type': 'MXRecord', 'prop_key': 'linkedRecordName'},
        'A': {'obj_type': 'HostRecord', 'prop_key': 'addresses'},
        'a': {'obj_type': 'GenericRecord', 'prop_key': 'rdata'},
        'PTR': {'obj_type': 'GenericRecord', 'prop_key': 'rdata'},
        'CNAME': {'obj_type': 'AliasRecord', 'prop_key': 'linkedRecordName'},
        'TXT': {'obj_type': 'TXTRecord', 'prop_key': 'txt'},
}

BAM2Bind = {
        'HostRecord': 'A',
        'MXRecord': 'MX',
        'AliasRecord': 'CNAME',
        'TXTRecord': 'TXT',
}

IPv4Objects = (
        'IP4Block',
        'IP4Network',
        'IP4Adress',
        'IP4DHCPRange',
        'IP4NetworkTemplate',
)

Categories = {
    'all': 'ALL',
    'admin': 'ADMIN',
    'Configuration': 'CONFIGURATION',
    'deploymentOptions': 'DEPLOYMENT_OPTIONS',
    'deploymentRoles': 'DEPLOYMENT_ROLES',
    'deploymentSchedulers': 'DEPLOYMENT_SCHEDULERS',
    'dhcpClassObjects': 'DHCPCLASSES_OBJECTS',
    'dhcpNACPolicies': 'DHCPNACPOLICY_OBJECTS',
    'IP4Objects': 'IP4_OBJECTS',
    'IP6Objects': 'IP6_OBJECTS',
    'MACPoolObjects': 'MACPOOL_OBJECTS',
    'resourceRecords': 'RESOURCE_RECORD',
    'servers': 'SERVERS',
    'tags': 'TAGS',
    'tasks': 'TASKS',
    'TFTPObjects': 'TFTP_OBJECTS',
    'vendorProfiles ': 'VENDOR_PROFILES',
    'viewZones ': 'VIEWS_ZONES',
    'TSIGKeys ': 'TSIG_KEYS',
    'GSS': 'GSS',
    'DHCPZones': 'DHCP_ZONES',
    'ServerGroup': 'SERVERGROUP',
}
