# start of module and package import ------------------------------------------
from os.path import exists
from src import gam900s_driver
# end of module and package import --------------------------------------------


# start of variable definition -------------------------------------------------
# end of variable definition --------------------------------------------------



# start of function definition ------------------------------------------------
# end of function definition --------------------------------------------------



# start of script execution ---------------------------------------------------
print("---------- GAM900S parameterization and calibration ----------")
my_gam900s = gam900s_driver.GAM900S(s_log_level = "info")
my_gam900s.connect(s_manufacturer_eds_path="gam900s_v2_00_manufacturer_v1_00.eds")

if input("Delete nvm data (y, n): ").upper() == "Y":
    my_gam900s.b_delete_nvm_data()

if input("Perform manufacturer parameterization (y, n): ").upper() == "Y":
    s_manufacturer_param_filename = input("Input full manufacturer parameter filename: ")
    if exists( s_manufacturer_param_filename ):
        if my_gam900s.b_load_default_manufacturer_parameters(s_default_param_path=s_manufacturer_param_filename) == True:
            if my_gam900s.b_perform_manufacturer_parameterization() == True:
                print("Manufacturer parameterization succeeded")
            else:
                print("Manufacturer parameterization failed")
    else:
        print("Manufacturer parameter file does not exist > abort parameterization")
    
if input("Perform acceleration calibration (y, n): ").upper() == "Y":
    if my_gam900s.b_perform_acceleration_calibration() == True:
        print("Acceleration calibration succeeded")
    else:
        print("Acceleration calibration failed")
    
if input("Perform temperature calibration (y, n): ").upper() == "Y":
    if my_gam900s.b_perform_temperature_calibration() == True:
        print("Temperature calibration succeeded")
    else:
        print("Temperature calibration failed")

my_gam900s.disconnect()

#exit()
# end of script execution -----------------------------------------------------
