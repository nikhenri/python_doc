# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
def get_register_dict(reg_dict):
    ip_dict = {}
    if reg_dict['decoder'] is None:
        return {}
    validate(reg_dict)
    for module in reg_dict['decoder'].keys():
        ip_dict[module] = get_module_info(reg_dict, module)

    return ip_dict


# -------------------------------------------------------------------------------------
# Quick check to see if the required field are there
# @TODO check field overlap
# @TODO check reg and field name unique
# @TODO cehck that field are in decroissant
def validate(reg_dict):
    module_keys = ['register', 'addr']
    register_keys = ['name', 'type', 'desc', 'field']
    field_keys = ['name', 'rst', 'desc']

    for module_key, module_obj in reg_dict['decoder'].items():
        if set(module_obj.keys()) != set(module_keys):  # check field in register
            raise Exception(f"For {module_key} error in field: expect {module_keys}, got {list(module_obj.keys())}")
        for addr_key, addr_obj in module_obj['register'].items():  # check if register addr
            if set(addr_obj.keys()) != set(register_keys):
                raise Exception(f"For '{module_key}' register addr '0x{addr_key:X}' error in field: expect {register_keys}, got {list(addr_obj.keys())}")
            for field_key, field_obj in addr_obj['field'].items():
                if '-' in str(field_key):
                    (high, low) = field_key.split("-")
                else:
                    (high, low) = (field_key, -1)

                if int(high) <= int(low):
                    raise Exception(f"For '{module_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: Range is negatif or null")
                if set(field_obj.keys()) != set(field_keys):
                    raise Exception(f"For '{module_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: expect {field_keys}, got {list(field_obj.keys())}")

# -------------------------------------------------------------------------------------
def get_module_info(reg_dict, decoder_name):
    module_dict = {'addr': reg_dict['decoder'][decoder_name]['addr'], 'register': {}}
    for register in (map(lambda x: x['name'], reg_dict['decoder'][decoder_name]['register'].values())):
        module_dict['register'][register] = get_module_register_info(reg_dict, decoder_name, register)
    return module_dict


# -------------------------------------------------------------------------------------
def get_module_register_info(reg_dict, decoder_name, register_name):
    addr = [addr for addr, reg in reg_dict['decoder'][decoder_name]['register'].items() if reg['name'] == register_name][0]
    register_dict = {'addr': addr, 'type': reg_dict['decoder'][decoder_name]['register'][addr]['type'], 'desc': reg_dict['decoder'][decoder_name]['register'][addr]['desc'], 'field': {}}

    for field_info in reg_dict['decoder'][decoder_name]['register'][addr]['field'].values():
        register_dict['field'][field_info['name']] = get_module_register_field_info(reg_dict, decoder_name, register_name, field_info['name'])

    return register_dict


# -------------------------------------------------------------------------------------
def get_module_register_field_info(reg_dict, decoder_name, register_name, field_name):
    addr = [addr for addr, reg in reg_dict['decoder'][decoder_name]['register'].items() if reg['name'] == register_name][0]
    field_range = [field_range for field_range, field_info in reg_dict['decoder'][decoder_name]['register'][addr]['field'].items() if field_info['name'] == field_name][0]
    if "-" in str(field_range):
        (field_high, field_low) = map(lambda x: int(x), field_range.split("-"))
    else:
        field_high = field_low = int(field_range)
    return {'high': field_high,
            'low': field_low,
            'length': field_high-field_low+1,
            'type': reg_dict['decoder'][decoder_name]['register'][addr]['type'],
            'reset': reg_dict['decoder'][decoder_name]['register'][addr]['field'][field_range]['rst'],
            'desc': reg_dict['decoder'][decoder_name]['register'][addr]['field'][field_range]['desc']}
