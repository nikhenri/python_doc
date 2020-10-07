# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
def get_register_dict(reg_dict):
    ip_dict = {}
    for module in reg_dict.keys():
        validate(reg_dict[module])

    for module in reg_dict.keys():
        if reg_dict[module]['decoder'] is not None:
            ip_dict[module] = {'decoder': {}}
            for decoder in reg_dict[module]['decoder'].keys():
                ip_dict[module]['decoder'][decoder] = get_decoder_info(reg_dict[module]['decoder'][decoder])

    for module in reg_dict.keys():
        if reg_dict[module]['ip'] is not None:
            ip_dict[module] = {'decoder': {}}
            for ip in reg_dict[module]['ip'].keys():
                ip_dict[module] = get_ip_info(reg_dict, module, ip)
    return ip_dict


# -------------------------------------------------------------------------------------
# Quick check to see if the required field are there
# @TODO check field overlap
# @TODO check reg and field name unique
# @TODO cehck that field are in decroissant
# @TODO check that IP offset > sub ip length
# @TODO check no 0Xa, instead of 0xa
# @TODO check IP exist
def validate(reg_dict):
    if reg_dict['decoder'] is not None:
        decoder_keys = ['register', 'addr']
        register_keys = ['name', 'type', 'desc', 'field']
        field_keys = ['name', 'rst', 'desc']

        for decoder_key, decoder_obj in reg_dict['decoder'].items():
            if set(decoder_obj.keys()) != set(decoder_keys):  # check field in register
                raise Exception(f"For {decoder_key} error in field: expect {decoder_keys}, got {list(decoder_obj.keys())}")
            for addr_key, addr_obj in decoder_obj['register'].items():  # check if register addr
                if set(addr_obj.keys()) != set(register_keys):
                    raise Exception(f"For '{decoder_key}' register addr '0x{addr_key:X}' error in field: expect {register_keys}, got {list(addr_obj.keys())}")
                for field_key, field_obj in addr_obj['field'].items():
                    if '-' in str(field_key):
                        (high, low) = field_key.split("-")
                    else:
                        (high, low) = (field_key, -1)

                    if int(high) <= int(low):
                        raise Exception(f"For '{decoder_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: Range is negatif or null")
                    if set(field_obj.keys()) != set(field_keys):
                        raise Exception(f"For '{decoder_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: expect {field_keys}, got {list(field_obj.keys())}")


# -------------------------------------------------------------------------------------
def get_ip_info(reg_dict, module, ip):
    ip_dict = {module: {'ip': {ip: {'nb': reg_dict[module]['ip'][ip]['nb'], 'addr': reg_dict[module]['ip'][ip]['addr'], 'offset': reg_dict[module]['ip'][ip]['offset']}}, 'decoder': {}}}
    if reg_dict[module]['ip'][ip]['nb'] > 1:
        for i in range(reg_dict[module]['ip'][ip]['nb']):
            for decoder in reg_dict[ip]['decoder'].keys():
                ip_dict[module]['decoder'][f"{ip}[{i}].{decoder}"] = get_decoder_info(reg_dict[ip]['decoder'][decoder])
                ip_dict[module]['decoder'][f"{ip}[{i}].{decoder}"]["addr"] += reg_dict[module]['ip'][ip]['addr'] + reg_dict[module]['ip'][ip]['offset'] * i
                #ip_dict[module]['decoder'][f"{ip}[{i}].{decoder}"][]

    return ip_dict[module]


# -------------------------------------------------------------------------------------
def get_decoder_info(reg_dict):
    decoder_dict = {'addr': reg_dict['addr'], 'register': {}}
    for register in (map(lambda x: x['name'], reg_dict['register'].values())):
        decoder_dict['register'][register] = get_decoder_register_info(reg_dict, register)
    return decoder_dict


# -------------------------------------------------------------------------------------
def get_decoder_register_info(reg_dict, register_name):
    addr = [addr for addr, reg in reg_dict['register'].items() if reg['name'] == register_name][0]
    register_dict = {'addr': addr, 'type': reg_dict['register'][addr]['type'], 'desc': reg_dict['register'][addr]['desc'], 'field': {}}

    for field_info in reg_dict['register'][addr]['field'].values():
        register_dict['field'][field_info['name']] = get_decoder_register_field_info(reg_dict, register_name, field_info['name'])

    return register_dict


# -------------------------------------------------------------------------------------
def get_decoder_register_field_info(reg_dict, register_name, field_name):
    addr = [addr for addr, reg in reg_dict['register'].items() if reg['name'] == register_name][0]
    field_range = [field_range for field_range, field_info in reg_dict['register'][addr]['field'].items() if field_info['name'] == field_name][0]
    if "-" in str(field_range):
        (field_high, field_low) = map(lambda x: int(x), field_range.split("-"))
    else:
        field_high = field_low = int(field_range)
    return {'high': field_high,
            'low': field_low,
            'length': field_high-field_low+1,
            'type': reg_dict['register'][addr]['type'],
            'reset': reg_dict['register'][addr]['field'][field_range]['rst'],
            'desc': reg_dict['register'][addr]['field'][field_range]['desc']}
