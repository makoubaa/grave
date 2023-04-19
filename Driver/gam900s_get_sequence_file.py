# start of module and package import ------------------------------------------
from os.path import exists
from src import gam900s_driver
# end of module and package import --------------------------------------------


# start of variable definition -------------------------------------------------
# end of variable definition --------------------------------------------------

# start of function definition ------------------------------------------------
# end of function definition --------------------------------------------------

# start of script execution ---------------------------------------------------
print("---------- GAM900S sequence file generator ----------")
my_gam900s = gam900s_driver.GAM900S(s_log_level = "info")

s_manufacturer_param_filename = input("Input full manufacturer parameter filename: ")
if exists(s_manufacturer_param_filename):
    my_gam900s.seq_file_mode = True
    my_gam900s.connect(s_manufacturer_eds_path="gam900s_v2_00_manufacturer_v1_00.eds")
    my_gam900s.b_load_default_manufacturer_parameters(s_manufacturer_param_filename)
    my_gam900s.write_manufacturer_parameter_sequence()
else:
    print("Manufacturer parameter file does not exist > abort seq file generation")

# end of script execution -----------------------------------------------------
