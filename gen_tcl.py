# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
#  Description:
# -------------------------------------------------------------------------------------
#  Author: Nik Henri
# -------------------------------------------------------------------------------------
import os


# -------------------------------------------------------------------------------------
class GenTCL:

    def __init__(self, full_reg_dict):
        self.full_reg_dict = full_reg_dict

    # -------------------------------------------------------------------------------------
    def generate(self, open_generate_file=False):
        for module in self.full_reg_dict.keys():
        # for decoder in self.register_dict['decoder'].keys():
            str = self.generate_tcl_file(self.full_reg_dict[module])
            with open(f'{module}.tcl', 'w') as configfile:
                configfile.write(str)

        if open_generate_file:
            os.startfile(f'{module}.tcl')

    # -------------------------------------------------------------------------------------
    def generate_tcl_file(self, register_dict):
        str = (
        "#================================================================================\n"
        "# UVM test search\n"
        "# @Description: Change modelsim GUI to add menu and button\n"
        "# @Argument:\n"
        "#\n"
        "# @Author: Nik Henri\n"
        "#================================================================================\n")
        return str
