#/usr/bin/env python

import os
import sys
from pprint import pprint
from bluecat_am import config
from bluecat_am import api

'''Higher Level Utility BAM API Functions'''

def bam_error(err_str):
    print('BAM error:', err_str)
    sys.exit()

#
# takes a mx_host and and optional priority
# and returns a list of mx_host, priority
#

def mx_parse(value):
    sep = ':'
    if sep in value:
        return value.split(sep)
    else:
        return (value, '10')

# Takes a property list as a dictionary e.g.
# {'ttl': '86400', 'absoluteName': 'fwsm-tabu.bkup.utoronto.ca', 'addresses': '128.100.96.158', 'reverseRecord': 'true'}
# and returns it as a string equivalent:
#   ttl=86400|absoluteName=fwsm-tabu.bkup.utoronto.ca|addresses=128.100.96.158|reverseRecord=true|

def dict2props(d):
    props = []
    for k,v in d.items():
        props.append('='.join([k,v]))
    return '|'.join(props) + '|'


# Takes a property list as a string e.g.
#   ttl=86400|absoluteName=fwsm-tabu.bkup.utoronto.ca|addresses=128.100.96.158|reverseRecord=true|
# and returns it as a dictionary equivalent:
#   {'ttl': '86400', 'absoluteName': 'fwsm-tabu.bkup.utoronto.ca', 'addresses': '128.100.96.158', 'reverseRecord': 'true'}

def props2dict(str):
    dd = {}
    ll = str.split('|')
    for i in ll[0:-1]:
        kv = i.split('=')
        dd[kv[0]] = kv[1]
    return dd


'''
    text: "Session Token-> BAMAuthToken: 7NfY4MTU1NDM5MDU1MzkzMzppc2VhLWFwaQ== <- for User : test-api"
    json: Session Token-> BAMAuthToken: 7NfY4MTU1NDM5MDU1MzkzMzppc2VhLWFwaQ== <- for User : test-api
'''

def bam_init():
    fn = 'bam_init'
#   config.ConfigName = 'Production'

    config.BaseURL = os.getenv('BAM_API_URL')
    if config.BaseURL is None:
        bam_error('The BAM_API_URL shell variable must be set')
    env_name = os.getenv('BAM_USER')
    env_pw = os.getenv('BAM_PW')
    if env_name is None or env_pw is None:
        bam_error('The BAM_USER and BAM_PW shell variables must be set')

    Creds = {'username': env_name, 'password': env_pw}
    session_token = api.login(Creds)

    config.AuthHeader = {
      'Authorization': 'BAMAuthToken: ' + session_token,
      'Content-Type': 'application/json'
    }

    if config.Debug:
        print('{} Authorization Header: {}'.format(fn,config.AuthHeader))

    config_ent = api.get_entity_by_name(config.RootId, config.ConfigName, 'Configuration')
    if config.Debug:
        print('{} Config Entity:'.format(fn))
        pprint(config_ent, indent=4)
    config.ConfigId = config_ent['id']
    if config.ConfigId > 0:
        view_ent = api.get_entity_by_name(config.ConfigId, config.ViewName, 'View')
        if config.Debug:
            print('{} View Entity:'.format(fn))
            pprint(view_ent, indent=4)
        config.ViewId = view_ent['id']
    else:
        bam_error('Error: The parent (Configuration) Id must be set before setting the View Id')

    if config.Debug:
        val = api.get_system_info()
        vals = val.split('|')
        for val in vals:
            print(val)
        print()


def bam_logout():
    URL = config.BaseURL + 'logout'
    req = requests.get(URL, headers=config.AuthHeader)
    sys.exit()


# Deletes all data and RRs in the Zone tree including other Zones

def delete_zone(fqdn):
    zone_id = get_zone_id(fqdn)
    if zone_id:
        val = api.delete(zone_id)
        return val

#
# Get the information of an Entity (Id and parentId) given a FQDN or a CIDR block
# Quick and dirty technique, based only on the fqdn
#

def get_info_by_name(fqdn):
    fn = 'get_info_by_name'
    obj_id = config.ViewId
    names = fqdn.split('.')
    lg = len(names)
    for name in names[::-1]:
        ent = api.get_entity_by_name(obj_id, name, 'Entity')
        if config.Debug:
            print('{} name: {} entity:'.format(fn, name))
            pprint(ent, indent=4)
        pid = obj_id
        obj_id = ent['id']
    ent['pid'] = pid
    if ent['type'] == 'Zone':
        pid = ent['id']
        name = ''
    else:
        pid = ent['pid']
        name = fqdn.split('.')[0]
    for obj_type in config.RRObjectTypes:
        if config.Debug:
            print('{} RR type: {}'.format(fn, obj_type))
        ents = api.get_entities(pid, obj_type, 0, 50)
        if config.Debug:
            if type(ents) is str:
                print('{} Type: {} Ent: {}'.format(fn, obj_type, ents))
            else:
                for e in ents:
                    if e['name'] == name:
                        print('{} Type: {} Ent:'.format(fn, obj_type))
                        pprint(e, indent=4)
    if config.Debug:
        print()
    return ent


def view_info_by_name(fqdn, *argv):
    fn = 'view_info_by_name'
    is_Zone = False
    ll = len(argv)
    if config.Debug: 
        print('{} fqdn: {}'.format(fn, fqdn))
        for arg in argv:
            print('arg: {}'.format(arg))
    if ll > 0:
        rr_type = argv[0]
        obj_rr_type = config.RRTypeMap[rr_type]['obj_type']
        if ll > 1:
            obj_rr_key = config.RRTypeMap[rr_type]['prop_key']
            value = argv[1]
    else:
        obj_rr_type = 'Entity'

    obj_id = config.ViewId
    names = fqdn.split('.')
    for name in names[::-1]:
        ent = api.get_entity_by_name(obj_id, name, 'Entity')
        if config.Debug:
            print('{} name: {} entity:'.format(fn, name))
            pprint(ent, indent=4)
        pid = obj_id
        obj_id = ent['id']
    ent['pid'] = pid
    if ent['type'] == 'Zone':
        is_Zone = True
        pid = ent['id']
        name = ''
    else:
        name = names[0]
    if config.Debug:
        print()
    if ll == 0:
        ids = []
        for obj_type in config.RRObjectTypes:
            ents = api.get_entities(pid, obj_type, 0, 50)
            for e in ents:
                if e['name'] == name:
                    ids.append(e['id'])
        bind_print(ids)
        if is_Zone:
            rrs = {}
            for obj_type in config.RRObjectTypes:
                ents = api.get_entities(pid, obj_type, 0, 50)
                if len(ents):
                    for e in ents:
                        name = e['name']
                        if len(name):
                            if name in rrs:
                                lst = rrs[name]
                                lst.append(e)
                                rrs[name] = lst
                            else:
                                rrs[name] = [e]

            ids = []
            for fqdn in sorted(rrs):
                for e in rrs[fqdn]:
                    ids.append(e['id'])
            bind_print(ids)

    elif ll > 0:
        ents = api.get_entities(pid, obj_rr_type, 0, 50)
        ids = []
        for e in ents:
            if e['name'] == name:
                if ll == 1:
                    ids.append(e['id'])
                else:
                    d = props2dict(e['properties'])
                    if value in d[obj_rr_key]:
                        ids.append(e['id'])
    return ent

'''

 Find a RR based on more or less specificity by matching:
 a. fqdn
 b. fqdn + RRtype
 c. fqdn + RRtype + value

 Return an list of matching entities. If there are no matches, return an empty lists


'''


def find_rr(fqdn, *argv):
    """Given a fqdn and an RR type and optionally a value
        return a list of entity IDs which match the given input
    """
    fn = 'find_rr'
    rr_type = None
    value = None
    obj_rr_key = None

    obj_types = config.RRObjectTypes

    if config.Debug:
        print('{}: fqdn: {} argv: {}'.format(fn, fqdn, argv))

    arglen = len(argv)
    if arglen > 0:
        rr_type = argv[0]
        obj_types = [config.RRTypeMap[rr_type]['obj_type']]
        if arglen > 1:
            value = argv[1]
            obj_rr_key = config.RRTypeMap[rr_type]['prop_key']

    if fqdn[-1] == '.':
        trailing_dot = True
        fqdn = fqdn[:-1]
    else:
        trailing_dot = False

    if config.Debug:
        print('{}: rr_type, value, obj_rr_key'.format(fn))
        print('     {} {} {}'.format(rr_type, value, obj_rr_key))
    names = fqdn.split('.')
    tld = names.pop()
    if tld not in config.LegalTLDs:
        print('Top level domain name must be one of: {}'.format(config.LegalTLDs))
    ent = api.get_entity_by_name(config.ViewId, tld, 'Entity')
    par_id = ent['id']

    for name in names[::-1]:
        ent = api.get_entity_by_name(par_id, name, 'Entity')
        ent['pid'] = par_id
        par_id = ent['id']
    obj_id = ent['id']
    par_id = ent['pid']
    rr_ents = []
    if ent['type'] == 'Zone':
        par_id = obj_id
        name = ''
        for obj_type in obj_types:
            if config.Debug:
                print('{}: RR type: {}'.format(fn, obj_type))
            ents = api.get_entities(par_id, obj_type, 0, 100)
            if len(ents):
                if trailing_dot:
                        rr_ents += ents
                else:
                    for ent in ents:
                        if ent['name'] == name:
                            rr_ents.append(ent)
    else:
        for obj_type in obj_types:
            ents = api.get_entities_by_name(par_id, name, obj_type, 0, 10)
            if len(ents):
                rr_ents += ents

    if arglen == 2 and rr_type != 'CNAME':
        found = False
        if rr_type == 'A' or rr_type == 'TXT' or rr_type == 'MX':
            for ent in rr_ents:
                d = props2dict(ent['properties'])
                values = d[obj_rr_key]
                if rr_type == 'A':
                    current_ips = values.split(',')
                    if value in current_ips:
                        found = True
                        rr_ents = [ent]
                        break
                elif rr_type == 'MX':
                    (mx_host, priority) = mx_parse(value)
                    if d['priority'] == priority and mx_host == values:
                        found = True
                        rr_ents = [ent]
                        break
                elif value == values:
                    found = True
                    rr_ents = [ent]
                    break
        if not found:
            rr_ents = []

    ids = []
    for rr_ent in rr_ents:
        if rr_ent['name'] == '':
            ids.append(rr_ent['id'])
    for rr_ent in rr_ents:
        if rr_ent['name'] != '':
            ids.append(rr_ent['id'])
    if config.Debug:
        print()
    return ids

def view_rr(fqdn, *argv):
    ids = find_rr(fqdn, *argv)
    if is_zone(fqdn):
        obj = get_soa_info(fqdn)
        print(obj)
    bind_print(ids)

#
# Print out a list of BAM RR Entity IDs in Bind format
#

def bind_print(ent_ids):
    if len(ent_ids) == 0:
        print('No RRs to display')
        return
    str_lens = []
    for ent_id in ent_ids:
        ent = api.get_entity_by_id(ent_id)
        d = props2dict(ent['properties'])
        fqdn = d['absoluteName']
        str_lens.append(len(fqdn))
    maxlen = max(str_lens)
    fmt_str = '{:<' + str(maxlen+4) + '} IN {:>5} {:<6} {}'
    mx_str = fmt_str + ' {}'
    for ent_id in ent_ids:
        ent = api.get_entity_by_id(ent_id)
        d = props2dict(ent['properties'])
        fqdn = d['absoluteName']
        if 'ttl' in d.keys():
            ttl = d['ttl']
        else:
            ttl = d['ttl'] = '86400'
            ent['properties'] = dict2props(d)
            api.update(ent)
        if ttl == '86400':
            ttl = '     '
        rr_type = config.BAM2Bind[ent['type']]
        value = d[config.RRTypeMap[rr_type]['prop_key']]
        if rr_type == 'A':
            values = value.split(',')
            for val in values:
                print(fmt_str.format(fqdn, ttl, rr_type, val))
        elif rr_type == 'TXT':
            print(fmt_str.format(fqdn, ttl, rr_type, value))
        elif rr_type == 'MX':
            pri = d['priority']
            print(mx_str.format(fqdn, ttl, rr_type, pri, value))
        else:
            print(fmt_str.format(fqdn, ttl, rr_type, value))

#
# A similar function but checking both the rr_type and value
# returns 0 if object can not be found
#

def object_find(fqdn, rr_type, value):
    fn = object_find
    id = 0
    if rr_type == 'MX':
        (value, priority) = mx_parse(value)

    obj_type = config.RRTypeMap[rr_type]['obj_type']
    prop_key = config.RRTypeMap[rr_type]['prop_key']

    names = fqdn.split('.')
    tld = names.pop()
    tld_ent = api.get_entity_by_name(config.ViewId, tld, 'Zone')
    pid = tld_ent['id']
    pname = tld
    while (len(names)):
        name = names.pop()
        ent = api.get_entity_by_name(pid, name, 'Entity')
        obj_id = ent['id']
        obj_ent = api.get_entity_by_id(obj_id)
        if config.Debug:
            print('{} name: {} id: {} ent:'.format(fn,name,obj_id))
            pprint(ent, indent=4)
        if len(names) == 0 and obj_id:
            obj_type = obj_ent['type']
            if obj_type == 'Zone':
                pid = obj_id
            else:
                ents = api.get_entities(pid, obj_type, 0, 100)
                if len(ents):
                    for ent in ents:
                        if 'properties' in ent and ent['properties'] is not None:
                            d = props2dict(ent['properties'])
                            if d['absoluteName'] == fqdn:
                                if 'addresses' in d:
                                    obj_id = ent['id']
                                elif value == d[prop_key]:
                                    obj_id = ent['id']
        pname = name
        pid = obj_id
    return obj_id


def get_id_by_name(fqdn):
    ent = get_info_by_name(fqdn)
    return ent['id']


# not used
def get_pid_by_id(id):
    ent = api.get_parent(id)
    return ent['id']


def get_info_by_id(id):
    ent = api.get_entity_by_id(id)
    pid = api.get_parent(ent['id'])
    ent['pid'] = pid
    return ent


#
# return the parent ID of an Object based on its name
#


def get_pid_by_name(fqdn):
    info = get_info_by_name(fqdn)
    return info['pid']

#
# gets an entity based on fqdn
#

def get_host_info(vid, fqdn):
    names = fqdn.split('.')
    lg = len(names)
    igd = vid
    for name in names[::-1]:
        ent = api.get_entity_by_name(id, name, 'Entity')
        if ent['type'] == 'Zone':
            id = ent['id']
            print(names[:l])
            lg -= 1
        else:
            break
    name = '.'.join(names[:l])
    ent = api.get_entity_by_name(id, name, 'GenericRecord')
    return ent


    
#
# retrieves the Id of a Zone or Subzone
#

def get_zone_id(fqdn):
    info = get_info_by_name(fqdn)
    if info['type'] == 'Zone':
        return info['id']
    else:
        print(fqdn, 'is not a zone')

#
# gets SOA record for a give zone
#

def get_soa_info(fqdn):
    zid = get_zone_id(fqdn)
    pid = get_pid_by_id(zid)
    ent = api.get_entity_by_name(pid, fqdn, 'StartOfAuthority')
    return ent

#
# is_zone takes a name/fqdn as input and returns: False
# if it is not a zone, otherwise the object_Id of the zone
#

def is_zone(fqdn):
    ent = get_info_by_name(fqdn)
    if ent['type'] == 'Zone':
        return ent['id']
    else:
        return False

#
# Add a zone using the generic add_generic call rather than
# the specific add_zone() one
#
    
def add_zone_generic(fqdn):
    dot = '.'
    n = fqdn.split(dot)
    nm = n[0]
    subzone = dot.join(n[1:])
    par_id = get_id_by_name(subzone)
    props = 'deployable=true|'
    props += 'absoluteName=' + fqdn + '|'
    ent = {
        'name': nm,
        'type': 'Zone',
        'properties': props
    }
    val = add_entity(par_id, ent)
    return val

def is_external_host(fqdn):
    if fqdn in get_external_hosts():
        return True
    else:
        return False


def is_host_record(fqdn):
    fn = 'is_host_record'
    ent = get_info_by_name(fqdn)
    if config.Debug:
        print('{} ent: {}'.format(fn))
        pprint(ent, indent=4)
    if ent['id'] > 0 and ent['type'] == 'HostRecord':
        return True
    else:
        return False


def add_PTR_rr(fqdn, ipaddr, ttl=86400):
    macaddr = ''
    hostinfo = ''
    action = 'MAKE_STATIC'
    props = 'ptrs=' + str(config.ViewId) + ',' + fqdn
    val = assign_IP4_Address(config.ConfigId, ipaddr, macaddr, hostinfo, action, props)
    return val

def get_external_hosts():
    exhosts = []
    ents = api.get_entities(config.ViewId, 'ExternalHostRecord', 0, 250)
    for ent in ents:
        exhosts.append(ent['name'])
    return exhosts

def add_external_host(exhost):
    exhosts = get_external_hosts()
    if exhost not in exhosts:
        val = api.add_ExternalHost_Record(config.ViewId, exhost, 'comments=Ext. Host|')
        print(val)

#
# delete a given generic RR
#

def delete_rr(fqdn, rr_type, *argv):
    fn = 'delete_rr'
    if argv:
        value = argv[0]
    else:
        value = '*'
    if config.Debug:
        print('{} Input data: {} {} {}'.format(fn,fqdn, rr_type, value))

# there can only be one CNAME record for a FQDN so the value does not matter
    if rr_type == 'CNAME':
        obj_id = find_rr(fqdn, rr_type)
    else:
        obj_id = find_rr(fqdn, rr_type, value)
    if config.Debug:
        print('{} obj_id: {}'.format(fn, obj_id))
    if obj_id:
        print('This RR exists and will be deleted')
        if rr_type == 'A':
            obj_prop_key = config.RRTypeMap[rr_type]['prop_key']
            ent = api.get_entity_by_id(obj_id[0])
            d = props2dict(ent['properties'])
            ip_list = d[obj_prop_key].split(',')
            ip_list.remove(value)
            if ip_list:
                d[obj_prop_key] = ','.join(ip_list)
                ent['properties'] = dict2props(d)
                if config.Debug:
                    print('before:')
                    bind_print(obj_id)
                api.update(ent)
                if config.Debug:
                    print('after:')
                    bind_print(obj_id)
            else:
                api.delete(obj_id[0])
        else:
            api.delete(obj_id[0])
    else:
        print('No RR exists matching {} {} {}'.format(fqdn,rr_type,value))


#
# fqdn is at the zone level or is a new RR below a zone
# new code using find_rr
#

def add_rr(fqdn, rr_type, value, ttl):
    fn = 'add_rr'
    if config.Debug:
        print('{} Input data: {} {} {} {}'.format(fn, fqdn, rr_type, value, ttl))
    obj_prop_key = config.RRTypeMap[rr_type]['prop_key']
    obj_id = find_rr(fqdn, rr_type, value)
    if obj_id:
        print('This {} Record already exists'.format(rr_type))
        bind_print(obj_id)
        return obj_id
    elif rr_type == 'A':
        obj_id = find_rr(fqdn, rr_type)
        if obj_id:
            ent = api.get_entity_by_id(obj_id[0])
            d = props2dict(ent['properties'])
            ip_list = d[obj_prop_key]
            ip_list += ',' + value
            d[obj_prop_key] = ip_list
            d['ttl'] = ttl
            ent['properties'] = dict2props(d)
            api.update(ent)
            print('Added Host Record:')
            bind_print(obj_id)
        else:
            # adding to the top level of the zone requires a leading dot
            if is_zone(fqdn):
                fqdn = '.' + fqdn
            obj_id = api.add_host_record(fqdn, value, ttl)
    elif rr_type == 'TXT':
        if is_zone(fqdn):
            fqdn = '.' + fqdn
        obj_id = api.add_TXT_Record(fqdn, value, ttl)
    elif rr_type == 'CNAME':
        if is_zone(fqdn):
            print('Cannot add a CNAME record at the top of a Zone')
            return obj_id
        else:
            obj_id = api.add_Alias_Record(fqdn, value, ttl)
    elif rr_type == 'MX':
        (mx_host, priority) = mx_parse(value)
        if is_zone(fqdn):
            fqdn = '.' + fqdn
        obj_id = api.add_MX_Record(fqdn, priority, mx_host, ttl)
    if type(obj_id) is not int:
        print('Cannot add: {} of type {} Error: {}'.format(fqdn, rr_type, obj_id))
    else:
        print('added new {} record:'.format(rr_type))
        bind_print([obj_id])
    return obj_id

#
# update a given RR to the state of the values given
# Using find_rr
#

def update_rr(fqdn, rr_type, value, ttl):
    fn = 'update_rr'
    id_list = find_rr(fqdn, rr_type)
    if not id_list:
        print('Can not find a RR to update with name {} with type {}'.format(fqdn, rr_type))
        return
# There should only be one RR found with the fqdb and type given and value
# If there are more than one, update the first one only
    obj_id = id_list[0]
    ent = api.get_entity_by_id(obj_id)
    if config.Debug:
        print('{} fqdn {} rr_type {} value {}'.format(fn, fqdn, rr_type, value))
        print('{} ent bef:'.formt(fn))
        pprint(ent, indent=4)
    prop_key = config.RRTypeMap[rr_type]['prop_key']
    d = props2dict(ent['properties'])
    d['ttl'] = ttl
    if rr_type ==  'MX':
        (pri, mx) = value.split(',')
        d[prop_key] = mx
        d['priority'] = pri
        ent['properties'] = dict2props(d)
    elif rr_type == 'A':
        org_value = value
        ip_list = value.split(',')
        ip_tup = tuple(ip_list)
        for ip in ip_tup:
            ip_test_ent = api.get_ipranged_by_ip(ip)
            if type(ip_test_ent) is str or ip_test_ent['id'] == 0:
                print('IP address: {} is not in a defined network'.format(ip))
                ip_list.remove(ip)
        if ip_list:
            d[prop_key] = ','.join(ip_list)
            ent['properties'] = dict2props(d)
        else:
            print('None of the IP addresses in {} could be updated'.format(org_value))
            return
    elif rr_type == 'TXT' or rr_type == 'CNAME':
        d[prop_key] = value
        ent['properties'] = dict2props(d)
    if config.Debug:
        print('{} ent aft:'.format(fn))
        pprint(ent, indent=4)
    api.update(ent)
    print('Updated RR as follows:')
    bind_print([obj_id])
