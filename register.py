# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------


class Register:

    # -------------------------------------------------------------------------------------
    def __init__(self, reg_dict):
        self.reg_dict = reg_dict
        self.validate()

    # -------------------------------------------------------------------------------------
    # Quick check to see if the required field are there
    def validate(self):
        IP_KEYS = ['docParser', 'register']
        REGISTER_KEYS = ['name', 'type', 'desc', 'field']
        FIELD_KEYS = ['name', 'rst', 'desc']

        for ip_key, ip_obj in self.reg_dict.items():
            if set(ip_obj.keys()) != set(IP_KEYS):  # check field in register
                raise Exception(f"For {ip_key} error in field: expect {IP_KEYS}, got {list(ip_obj.keys())}")
            for addr_key, addr_obj in ip_obj['register'].items():  # check if register addr
                if set(addr_obj.keys()) != set(REGISTER_KEYS):
                    raise Exception(f"For '{ip_key}' register addr '0x{addr_key:X}' error in field: expect {REGISTER_KEYS}, got {list(addr_obj.keys())}")
                for field_key, field_obj in addr_obj['field'].items():
                    if '-' in str(field_key):
                        (high, low) = field_key.split("-")
                    else:
                        (high, low) = (field_key, -1)
                    if int(high) >= 32:
                        raise Exception(f"For '{ip_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: Can't be higher then 32bits (31)")
                    if int(high) <= int(low):
                        raise Exception(f"For '{ip_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: Range is negatif or null")
                    if set(field_obj.keys()) != set(FIELD_KEYS):
                        raise Exception(f"For '{ip_key}' register addr '0x{addr_key:X}' field '{field_key}' error in field: expect {FIELD_KEYS}, got {list(field_obj.keys())}")

    # -------------------------------------------------------------------------------------
    def get_ip_list(self):
        return self.reg_dict.keys()

    # -------------------------------------------------------------------------------------
    def get_ip_addr_list(self, register_name):
        return self.reg_dict[register_name]['register'].keys()

    # -------------------------------------------------------------------------------------
    def get_register_name(self, register_name, addr):
        return self.reg_dict[register_name]['register'][addr]['name']