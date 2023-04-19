import time
from os.path import exists
import canopen
from canopen.sdo.constants import *
import struct
from . import gam900s_param_def as gam_defs
from . import helper as hlp


class GAM900S:

    def __init__(self, s_log_level="error"):  # could be changed to singleton pattern since only one physical hil system is present
        """
        Initialiazes the class at instanciation time
        """
        self._log_level = s_log_level
        self._log("\nEntering gam900s instantiation", s_level="info")
        self._canopen_handle = canopen.Network()
        self.canopen_node = None
        self.connected = False
        self._manufacturer_param_dict = gam_defs.d_DeepflattenDict(gam_defs.d_manufacturerpackage)
        self._customer_param_dict = gam_defs.d_DeepflattenDict(gam_defs.d_customerpackage)
        self._b_admin_mode_set = False
        self._b_customer_mode_set = False
        self._default_admin_password = 0xFF00FF00
        self._device_status_save_key = 0x65766173  # "save" / "evas" as pw
        self._device_status_delete_key = 0x216C6564  # "del!" / "!led" as pw
        self._flash_access_time = 2.5
        self._restart_wait_time = 4.0
        self.f_failure_reaction_time_s = 0.05
        self.u_failure_reaction_time_ms = int(self.f_failure_reaction_time_s * 1000)
        self.seq_file_mode = False
        self._log("Leaving gam900s instantiation \n", s_level="info")

    def connect(self, s_interface="ixxat", u_channel=0, u_baudrate=50000, u_node=1, s_req_svn_version=None, s_manufacturer_eds_path="gam900s_v2_00_manufacturer_v1_00.eds"):
        """
        Connects via the can driver to the gam900s dut
        The can interface, channel, baudrate, node can be passed
        The required svn version number can be passed and will be checked if unequals None
        The manufacturer eds file path can be passed (a valid eds file is neccessary, default eds file will be searched in the same folder if nothing is passed)
        """
        b_proceed = True
        self._log("\nEntering gam900s connect", s_level="info")
        if self.connected == True:
            self._log("Error gam900s connect: Already connected > abort connect", s_level="error")
            b_proceed = False
        if b_proceed == True:
            self._log("Connecting to gam900s", s_level="info")
            if self.seq_file_mode == False:
                self._canopen_handle.connect(bustype=s_interface, channel=u_channel, bitrate=u_baudrate)
            self.canopen_node = self._canopen_handle.add_node(u_node, s_manufacturer_eds_path)
        if b_proceed == True and s_req_svn_version != None:
            if self.sdo_read("Error Information", "svn version") != s_req_svn_version:
                self._log("Error gam900s connect: Invalid dut svn version > abort and disconnect", s_level="error")
                self.disconnect()
                b_proceed = False
        if b_proceed == True:
            self.connected = True  # all checks passed > set connected flag
        self._log("Leaving gam900s connect \n", s_level="info")

    def disconnect(self):
        """
        Disconnects the can driver
        """
        self._log("\nEntering gam900s disconnect", s_level="info")
        if self.connected == True:
            self._canopen_handle.disconnect()
            self.connected = False
        else:
            self._log("Gam900s already disconnected", s_level="info")
        self._log("Leaving gam900s disconnect \n", s_level="info")

    def b_load_default_manufacturer_parameters(self, s_default_param_path="GAM900S_V2_Default_Param.csv"):
        """
        Loads the default manufacturer parameters from the csv file
        The default param file path can be passed (a valid param file is neccessary, default param file will be searched in the same folder if nothing is passed)
        """
        b_proceed = True
        self._log("\nEntering gam900s load manufacturer parameters", s_level="info")
        if exists(s_default_param_path) == False:
            self._log("Error gam900s load default manufacturer parameter: Param file does not exist > abort load", s_level="error")
        if b_proceed == True:
            b_proceed = self._b_load_default_parameters(s_parameter_type="manufacturer", s_default_param_path=s_default_param_path)
        self._log("Leaving gam900s load manufacturer parameters \n", s_level="info")
        return b_proceed

    def b_load_default_customer_parameters(self, s_default_param_path="GAM900S_V2_Default_Customer_Param.csv"):
        """
        Loads the default customer parameters from the csv file
        The default param file path can be passed (a valid param file is neccessary, default param file will be searched in the same folder if nothing is passed)
        """
        b_proceed = True
        self._log("\nEntering gam900s load customer parameters", s_level="info")
        if exists(s_default_param_path) == False:
            self._log("Error gam900s load default customer parameter: Param file does not exist > abort load", s_level="error")
        if b_proceed == True:
            b_proceed = self._b_load_default_parameters(s_parameter_type="customer", s_default_param_path=s_default_param_path)
        self._log("Leaving gam900s load customer parameters \n", s_level="info")
        return b_proceed

    def _b_load_default_parameters(self, s_parameter_type, s_default_param_path):
        """
        Loads the default parameters from the csv file
        The default param file path can be passed (a valid param file is neccessary)
        """
        b_proceed = True
        self._log("\nEntering gam900s load default parameters", s_level="info")
        if s_parameter_type == "manufacturer":
            d_param_dict = self._manufacturer_param_dict
        elif s_parameter_type == "customer":
            d_param_dict = self._customer_param_dict
        else:
            self._log("Error gam900s load default parameter: Invalid parameter type " + s_parameter_type + " > abort load", s_level="error")
            b_proceed = False
        if exists(s_default_param_path) == False:
            self._log("Error gam900s load default parameter: Param file does not exist > abort load", s_level="error")
        if b_proceed == True:
            with open(s_default_param_path) as paramfile:
                for s_line in paramfile.readlines():
                    s_line = s_line.strip()
                    if s_line == "":
                        continue  # skip empty lines
                    s_param, s_value = s_line.split(";")
                    if s_param == "PARAM":
                        continue  # skip header
                    elif s_param == "LAYOUT":
                        continue  # skip layout identifier
                    elif "ENABLED" in s_param:
                        if s_value == "True":
                            continue  # skip enable params
                        elif s_value == "False":
                            self._set_default_param_section(s_parameter_type, s_param)  # set default values for not enabled params
                        else:
                            self._log("Error: Invalid enable key " + s_value + "for " + s_param)
                            b_proceed = False
                            break
                    else:
                        d_param_dict[s_param]["data"] = self._map_parameter(s_param, s_value)
        self._log("Leaving gam900s load customer parameters \n", s_level="info")
        return b_proceed

    def set_manufacturer_parameter(self, s_param_name, param_value, b_mapping=True):
        """
        Sets the passed manufacturer parameter
        The mapping can be activated by assigning b_mapping to True
        """
        if s_param_name in self._manufacturer_param_dict.keys():
            if b_mapping == False:
                self._manufacturer_param_dict[s_param_name]["data"] = param_value
            else:
                self._manufacturer_param_dict[s_param_name]["data"] = self._map_parameter(s_param_name, param_value)
        else:
            self._log("Error gam900s set manufacturer parameter: Invalid parameter " + s_param_name, s_level="error")

    def get_local_manufacturer_parameter(self, s_param_name, b_mapping=False):
        """
        Returns the desired manufacturer parameter from the local dict (not from the sensor > if loaded both are equal)
        The mapping is not yet supported
        """
        if s_param_name in self._manufacturer_param_dict.keys():
            if b_mapping == False:
                return self._manufacturer_param_dict[s_param_name]["data"]
            else:
                pass
        else:
            self._log("Error gam900s get manufacturer parameter: Invalid parameter " + s_param_name + "\n", s_level="error")

    def set_customer_parameter(self, s_param_name, param_value, b_mapping=True):
        """
        Sets the passed customer parameter
        The mapping can be activated by assigning b_mapping to True
        """
        if s_param_name in self._customer_param_dict.keys():
            if b_mapping == False:
                self._customer_param_dict[s_param_name]["data"] = param_value
            else:
                self._customer_param_dict[s_param_name]["data"] = self._map_parameter(s_param_name, param_value)
        else:
            self._log("Error gam900s set customer parameter: Invalid parameter " + s_param_name, s_level="error")

    def get_local_customer_parameter(self, s_param_name, b_mapping=False):
        """
        Returns the desired customer parameter from the local dict (not from the sensor > if loaded both are equal)
        The mapping is not yet supported
        """
        if s_param_name in self._customer_param_dict.keys():
            if b_mapping == False:
                return self._customer_param_dict[s_param_name]["data"]
            else:
                pass
        else:
            self._log("Error gam900s get customer parameter: Invalid parameter " + s_param_name + "\n", s_level="error")

    def b_perform_manufacturer_parameterization(self, u_admin_password=None, b_manipulate_crc=False):
        """
        Performs the manufacturer parameterization
        """
        self._log("\nEntering gam900s manufacturer parametrisation", s_level="info")
        b_proceed = True
        if (not self._b_admin_mode_set) or (u_admin_password is not None):
            self._log("Set the device to admin mode", s_level="info")
            if not self.b_set_admin_mode(u_admin_password=u_admin_password):
                self._log("Error gam900s manufacturer parametrisation: set admin mode", s_level="error")
                b_proceed = False
        if b_proceed == True:
            b_proceed = self._b_perform_parameterization(s_parameter_type="manufacturer", b_manipulate_crc=b_manipulate_crc)
        self._log("Reset the device admin mode", s_level="info")
        if not self.b_reset_admin_mode(u_admin_password=u_admin_password):
            self._log("Error gam900s manufacturer parametrization: reset admin mode", s_level="error")
            b_proceed = False
        time.sleep(self._restart_wait_time)
        self._log("Leaving gam900s manufacturer parametrisation \n", s_level="info")
        return b_proceed

    def b_perform_customer_parameterization(self, u_customer_password=None, b_manipulate_crc=False):
        """
        Performs the customer parameterization
        """
        self._log("\nEntering gam900s customer parameterization", s_level="info")
        b_proceed = True
        if (not self._b_customer_mode_set) or (u_customer_password is not None):
            self._log("Set the device to customer mode", s_level="info")
            if not self.b_set_customer_mode(u_customer_password=u_customer_password):
                self._log("Error gam900s customer parameterization: set customer mode", s_level="error")
                b_proceed = False
        if b_proceed == True:
            b_proceed = self._b_perform_parameterization(s_parameter_type="customer", b_manipulate_crc=b_manipulate_crc)
        self._log("Reset the device customer mode", s_level="info")
        if self.b_reset_customer_mode(u_customer_password=u_customer_password) == False:
            self._log("Error gam900s customer parameterization: reset customer mode", s_level="error")
            b_proceed = False
        time.sleep(self._restart_wait_time)
        self._log("Leaving gam900s customer parameterization \n", s_level="info")
        return b_proceed

    def _b_perform_parameterization(self, s_parameter_type, b_manipulate_crc):
        """
        Performs the (manufacturer / customer) parameterization
        """
        b_proceed = True
        self._log("\nEntering gam900s parameterization", s_level="info")
        if not self.seq_file_mode:
            self._log("Set the device to pre operational state", s_level="info")  # set the node to pre operational state
            self.canopen_node.nmt.state = "PRE-OPERATIONAL"
        if s_parameter_type == "manufacturer":
            s_param_list_id = "Manufacturer parameterization"
            s_device_status_id = "manufacturer parameterization"
        elif s_parameter_type == "customer":
            s_param_list_id = "Customer parameterization"
            s_device_status_id = "customer parameterization"
        else:
            self._log("Error gam900s perform parameterization: Invalid parameter type " + s_parameter_type + " > abort parameterization", s_level="error")
            b_proceed = False
        if b_proceed:
            l_param_list = gam_defs.l_GetParameterizationList(s_param_list_id)
            self._log("Write parameters to the device", s_level="info")  # write parameters
            for list_item in l_param_list:
                for key, value in list_item["l_data"].items():
                    s_object_name = list_item["s_obj"]
                    s_param_name = key
                    param_value = value["data"]
                    if (self.seq_file_mode) and (s_object_name == "Manufacturer Data"):  # exclude manufacturer data in seq file mode
                        continue
                    if b_manipulate_crc and (s_param_name == "CRC"):
                        param_value = value["data"] + 1  # manipulate crc by increment
                    if self.b_sdo_write(param_value, s_object_name, s_param_name):
                        self._log("Write ok: " + s_param_name + " (value " + str(param_value) + ")", s_level="info")
                    else:
                        self._log("Error perform parameterization: Failed to write item: " + s_param_name + " > abort parameterization", s_level="error")
                        b_proceed = False
                        break
                if not b_proceed:
                    break
            if (b_proceed == True) and (self.seq_file_mode == False):  # save parameters if nothing went wrong (not in seq file mode)
                self._log("Write parameters success > save parameters", s_level="info")
                if not self.b_sdo_write(self._device_status_save_key, "Device Status", s_device_status_id):
                    self._log("Error gam900s save params > abort parameterization", s_level="error")
                    b_proceed = False
            time.sleep(self._flash_access_time)
        self._log("Leaving gam900s parameterization \n", s_level="info")
        return b_proceed

    def b_perform_acceleration_calibration(self, u_admin_password=None, b_default_calibration=True,
                                           l_channel_a_gain_matrix=None, l_channel_a_offset_vector=None,
                                           l_channel_b_gain_matrix=None, l_channel_b_offset_vector=None):
        """
        Performs the acceleration calibration
        The passed gain matrix and offset vectors are used if b_default_calibration is True
        """
        b_proceed = True
        self._log("\nEntering gam900s acceleration calibration", s_level="info")
        if b_default_calibration:
            l_channel_a_gain_matrix = [[1.0, 0.0, 0.0],
                                       [0.0, -1.0, 0.0],
                                       [0.0, 0.0, 1.0]]
            l_channel_a_offset_vector = [0.0, 0.0, 0.0]
            l_channel_b_gain_matrix = [[0.0, 1.0, 0.0],
                                       [-1.0, 0.0, 0.0],
                                       [0.0, 0.0, -1.0]]
            l_channel_b_offset_vector = [0.0, 0.0, 0.0]
        if not self.b_set_admin_mode(u_admin_password=u_admin_password):  # set admin mode
            self._log("Error gam900s acceleration calibration: set admin mode", s_level="error")
            b_proceed = False
        if b_proceed:
            u_number_axes = 3
            for u_axis in range(u_number_axes):
                for u_cross_axis in range(u_number_axes):
                    if not self.b_sdo_write(l_channel_a_gain_matrix[u_axis][u_cross_axis], "Acceleration Calibration", "channel a gain " + str(u_axis) + str(u_cross_axis)):
                        self._log("Error gam900s acceleration calibration: write channel a gain" + str(u_axis) + str(u_cross_axis), s_level="error")
                        b_proceed = False;
                        break;
                    if not self.b_sdo_write(l_channel_b_gain_matrix[u_axis][u_cross_axis], "Acceleration Calibration", "channel b gain " + str(u_axis) + str(u_cross_axis)):
                        self._log("Error gam900s acceleration calibration: write channel b gain" + str(u_axis) + str(u_cross_axis), s_level="error")
                        b_proceed = False;
                        break;
                if b_proceed == True:
                    if self.b_sdo_write(l_channel_a_offset_vector[u_axis], "Acceleration Calibration", "channel a offset " + str(u_axis)) == False:
                        self._log("Error gam900s acceleration calibration: write channel a offset " + str(u_axis), s_level="error")
                        b_proceed = False
                        break
                    if self.b_sdo_write(l_channel_b_offset_vector[u_axis], "Acceleration Calibration", "channel b offset " + str(u_axis)) == False:
                        self._log("Error gam900s acceleration calibration: write channel a offset " + str(u_axis), s_level="error")
                        b_proceed = False
                        break
                else:
                    break
        if b_proceed and self.b_sdo_write(self._device_status_save_key, "Device Status", "acceleration calibration") == False:
            self._log("Error acceleration calibration: save calibration", s_level="error")
            b_proceed = False
        time.sleep(self._flash_access_time)
        if b_proceed and self.b_reset_admin_mode(u_admin_password=u_admin_password) == False:  # reset admin mode
            self._log("Error acceleration calibration: reset admin mode", s_level="error")
            time.sleep(self._restart_wait_time)
            return False
        time.sleep(self._restart_wait_time)
        self._log("Leaving gam900s acceleration calibration", s_level="info")
        return b_proceed

    def b_perform_temperature_calibration(self, u_admin_password=None, i_temp_set_value=23):
        """
        Performs the temperature calibration
        """
        b_proceed = True
        self._log("\nEntering gam900s temperature calibration", s_level="info")
        if self.b_set_admin_mode(u_admin_password=u_admin_password) == False:  # set admin mode
            self._log("Error temperature calibration: set admin mode", s_level="error")
            b_proceed = False
        if b_proceed and self.b_sdo_write(i_temp_set_value, "Temperature Calibration", "temp set value") == False:
            self._log("Error temperature calibration: set temp value", s_level="error")
            b_proceed = False
        if b_proceed and self.b_sdo_write(self._device_status_save_key, "Device Status", "temperature calibration") == False:
            self._log("Error temperature calibration: save calibration", s_level="error")
            b_proceed = False
        time.sleep(self._flash_access_time)
        if self.b_reset_admin_mode(u_admin_password=u_admin_password) == False:  # reset admin mode
            self._log("Error temperature calibration: reset admin mode \n", s_level="error")
            time.sleep(self._restart_wait_time)
            b_proceed = False
        time.sleep(self._restart_wait_time)
        self._log("Leaving gam900s temperature calibration", s_level="info")
        return b_proceed

    def b_delete_nvm_data(self):
        """
        Deletes the nvm data of the dut (parameterization, calibration, canopen and error data)
        If an type 3 error is active nvm data is not deleted
        """
        b_proceed = True
        self._log("\nEntering gam900s delete nvm data", s_level="info")
        if self.b_set_admin_mode() == False:  # set admin mode
            self._log("Error delete nvm data: set admin mode", s_level="error")
            b_proceed = False
        if b_proceed and self.b_sdo_write(self._device_status_delete_key, "Device Status", "delete nvm data") == False:
            self._log("Error delete nvm data: delete cmd", s_level="error")
            b_proceed = False
        time.sleep(self._flash_access_time)
        if self.b_reset_admin_mode() == False:  # reset admin mode
            self._log("Error delete nvm data: reset admin mode", s_level="error")
            time.sleep(self._restart_wait_time)
            b_proceed = False
        time.sleep(self._restart_wait_time)
        self._log("\Leaving gam900s delete nvm data", s_level="info")
        return b_proceed

    def d_get_device_status(self):
        """
        Returns a dict of the device status
        Device status includes manufacturer and customer parameterization, acceleration and temperature calibration
        """
        b_proceed = True
        self._log("\nEntering gam900s get device status", s_level="info")
        return_dict = dict()
        if not self.b_set_admin_mode():  # set admin mode
            self._log("Error get device status: set admin mode", s_level="info")
            b_proceed = False
        if b_proceed == True:
            device_status_list = ["manufacturer parametrisation", "customer parametrisation", "acceleration calibration", "temperature calibration"]
            for device_status_item in device_status_list:
                read_value = self.sdo_read("Device Status", device_status_item)
                if read_value is not None:
                    return_dict[device_status_item] = hlp.b_data_to_bytes(read_value, "uint32_t").decode('ascii')
                else:
                    self._log("Error get device status: sdo read", s_level="info")
                    return_dict = None
                    b_proceed = False
                    break
        if not self.b_reset_admin_mode():  # reset admin mode
            self._log("Error get device status: reset admin mode", s_level="error")
        self._log("Leaving gam900s get device status \n", s_level="info")
        return return_dict

    def d_get_error_information(self):
        """
        Returns a dict of the error information
        """
        self._log("\nEntering gam900s get error information", s_level="info")
        return_dict = dict()
        device_status_list = ["module id", "event id", "debug value 1", "debug value 2", "microcontroller", "failmode active", "raw x", "raw y", "raw z",
                              "filterband 1", "filterband 2", "filterband 3", "filterband 4", "temperature", "svn version"]
        for device_status_item in device_status_list:
            read_value = self.sdo_read("Error Information", device_status_item)
            if read_value != None:
                return_dict[device_status_item] = read_value
            else:
                self._log("Error get error information: sdo read \n", s_level="info")
                return_dict = None
        self._log("Leaving gam900s get error information \n", s_level="info")
        return return_dict

    def b_set_admin_mode(self, u_admin_password=None):
        """
        Sets the admin mode
        """
        if u_admin_password is None:  # no password passed > use default admin password
            u_my_admin_password = self._default_admin_password
        else:
            u_my_admin_password = u_admin_password
        if not self.connected:
            self._log("Error gam900s set admin mode: device not connected", s_level="error")
            return False
        self.canopen_node.nmt.state = "PRE-OPERATIONAL"  # set the node to pre operational state
        if not self.b_sdo_write(u_my_admin_password, "Admin Mode", "set"):
            self._log("Error gam900s set admin mode: sdo write", s_level="error")
            return_value = False
        else:
            return_value = True
        self._admin_mode_set = return_value
        return return_value

    def b_reset_admin_mode(self, u_admin_password=None):
        """
        Resets the admin mode
        """
        if not u_admin_password:  # no password passed > use default admin password
            u_my_admin_password = self._default_admin_password
        else:
            u_my_admin_password = u_admin_password
        if not self.connected:
            self._log("Error gam900s reset admin mode: device not connected", s_level="error")
            return False
        self.canopen_node.nmt.state = "PRE-OPERATIONAL"  # set the node to pre operational state
        if not self.b_sdo_write(u_my_admin_password, "Admin Mode", "reset"):
            self._log("Error gam900s reset admin mode: sdo write", s_level="error")
            return_value = False
        else:
            return_value = True
        time.sleep(self._restart_wait_time)
        time.sleep(2.0)  # wait for additional 2 seconds
        self._admin_mode_set = False
        return return_value

    def b_set_customer_mode(self, u_customer_password=None):
        """
        Sets the customer mode
        """
        if u_customer_password is None:  # no password passed > use password from manufacturer crc
            u_my_customer_password = gam_defs.u_GetChecksum(gam_defs.d_manufacturerpackage["s_MyManufacturerParameter"])
        else:
            u_my_customer_password = u_customer_password
        if not self.connected:
            self._log("Error gam900s set customer mode: device not connected", s_level="error")
            return False
        self.canopen_node.nmt.state = "PRE-OPERATIONAL"  # set the node to pre operational state
        if not self.b_sdo_write(u_my_customer_password, "Customer Mode", "set"):
            self._log("Error gam900s set customer mode: sdo write", s_level="error")
            return_value = False
        else:
            return_value = True
        self._customer_mode_set = return_value
        return return_value

    def b_reset_customer_mode(self, u_customer_password=None):
        """
        Resets the customer mode
        """
        if u_customer_password == None:  # no password passed > use password from manufacturer crc
            u_my_customer_password = gam_defs.u_GetChecksum(gam_defs.d_manufacturerpackage["s_MyManufacturerParameter"])
        else:
            u_my_customer_password = u_customer_password
        if not self.connected:
            self._log("Error gam900s reset customer mode: device not connected", s_level="error")
            return False
        if not self.b_sdo_write(u_my_customer_password, "Customer Mode", "reset"):
            self._log("Error gam900s reset customer mode: sdo write", s_level="error")
            return_value = False
        else:
            return_value = True
        time.sleep(self._restart_wait_time)
        self._customer_mode_set = False
        return return_value

    def sdo_read(self, s_obj, s_subindex=None):
        """
        Performs and sdo read
        If the read fail None is returned and the exception is logged
        """
        if self.connected:
            try:
                if s_subindex is None:
                    value = (self.canopen_node.sdo[s_obj]).phys  # object does not have a subindex
                else:
                    value = (self.canopen_node.sdo[s_obj][s_subindex]).phys  # object does have a subindex
            except Exception as e:
                if s_subindex is None:
                    self._log("Error sdo read: Exception (" + s_obj + "): " + str(e), s_level="error")  # object does not have a subindex
                else:
                    self._log("Error sdo read: Exception (" + s_obj + ", " + s_subindex + "): " + str(e), s_level="error")  # object does have a subindex
                value = None
        else:
            self._log("Error sdo read: Device not connected", s_level="error")
            value = None
        return value

    def b_sdo_write(self, value, s_obj, s_subindex=None):
        """
        Performs and sdo write
        If the write fail None is returned and the exception is logged
        If admin mode reset is written the error is surpressed (not sdo message is returned)
        """
        b_write_success = False
        if self.connected:
            try:
                if s_subindex is None:
                    (self.canopen_node.sdo[s_obj]).phys = value  # object does not have a subindex
                else:
                    (self.canopen_node.sdo[s_obj][s_subindex]).phys = value  # object does have a subindex
                b_write_success = True
            except Exception as e:
                if ((s_obj == "Admin Mode") or (s_obj == "Customer Mode")) and (s_subindex == "reset"):  # admin and customer mode do not return an sdo message
                    b_write_success = True
                else:
                    if s_subindex is None:
                        self._log("Error sdo write: Exception (" + s_obj + "): " + str(e), s_level="error")  # object does not have a subindex
                    else:
                        self._log("Error sdo write: Exception (" + s_obj + ", " + s_subindex + "): " + str(e), s_level="error")  # object does have a subindex
                    b_write_success = False
        else:
            self._log("Error sdo write: Device not connected", s_level="error")
            b_write_success = False
        return b_write_success

    def b_wait_for_bootup_msg(self, f_timeout=10):
        """
        Waits for a bootup message for a desired time
        If bootup message is receive during the desired time True is returned, else False is returned
        """
        b_bootup_msg_received = False
        if self.connected:
            try:
                self.canopen_node.nmt.wait_for_bootup(f_timeout)
                b_bootup_msg_received = True
            except Exception as e:
                self._log("Error wait for bootup: Exception " + str(e), s_level="error")
                b_bootup_msg_received = False
        else:
            self._log("Error wait for bootup: Device not connected", s_level="error")
            b_bootup_msg_received = False
        return b_bootup_msg_received

    def write_manufacturer_parameter_sequence(self):
        """
        Writes the CAN sequence of the passed manufacturer parameters to a local file
        """
        s_seq_file_name = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + "_seq_file.log"
        with open(s_seq_file_name, "w") as seq_file_pointer:
            def request_response_fake(sdo_request):
                req_seq = struct.unpack_from("BBBBBBBB", sdo_request)  # unpack sdo request(bytes to tuple)
                seq_file_pointer.write("Tx 601 {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}".format(req_seq[0],
                                                                                                               req_seq[1], req_seq[2], req_seq[3], req_seq[4], req_seq[5],
                                                                                                               req_seq[6], req_seq[7]) + "\n")
                if req_seq[0] & 0xE0 == REQUEST_DOWNLOAD:  # check request command and return corresponding response
                    return struct.pack("B", RESPONSE_DOWNLOAD)
                elif req_seq[0] & 0xE0 == REQUEST_SEGMENT_DOWNLOAD:
                    return struct.pack("B", RESPONSE_SEGMENT_DOWNLOAD)
                else:
                    pass  # assert

            self.canopen_node.sdo.request_response = request_response_fake
            self._b_perform_parameterization(s_parameter_type="manufacturer", b_manipulate_crc=False)

    def _map_parameter(self, s_parameter, value):
        """
        Maps the passed manufacturer parameter
        Mapping is performed for: canopen baudrate, sos data, filter parameter, filterband parameter (else strings are converted to integer)
        """
        f_parameter_scaling = 20.0
        if s_parameter == "CANOPEN_BAUD_RATE":
            l_mapping_from_string = ["20000", "50000", "100000", "125000", "250000", "500000", "800000", "1000000"]
            l_mapping_from_int = [20000, 50000, 100000, 125000, 250000, 500000, 800000, 1000000]
            l_mapping_to = [1, 2, 3, 4, 5, 6, 7, 8]
            if type(value) == str and value in l_mapping_from_string:
                return_value = l_mapping_to[l_mapping_from_string.index(value)]
            elif type(value) == int and value in l_mapping_from_int:
                return_value = l_mapping_to[l_mapping_from_int.index(value)]
            else:
                self._log("Error manufacturer param mapping: Invalid canopen baud rate", s_level="error")
                return_value = 0
        elif "SOS" in s_parameter:
            if type(value) == str:
                return_value = float(value)
            elif (type(value) == int) or (type(value) == float):
                return_value = value
            else:
                self._log("Error manufacturer param mapping: Invalid sos data type", s_level="error")
                return_value = 0.0
        elif ("FILTER" in s_parameter) and ("DESIGN" in s_parameter):
            l_mapping_from = ["BUTTER", "CHEBY1", "CHEBY2", "ELLIPTIC", "SOS1", "SOS2", "SOS3", "SOS4"]
            l_mapping_to = [1, 2, 3, 4, 5, 6, 7, 8]
            if value in l_mapping_from:
                return_value = l_mapping_to[l_mapping_from.index(value)]
            else:
                self._log("Invalid filter design")
                return_value = 0
        elif ("FILTER" in s_parameter) and ("TYPE" in s_parameter):
            l_mapping_from = ["LOWPASS", "HIGHPASS", "BANDPASS"]
            l_mapping_to = [1, 2, 3]
            if value in l_mapping_from:
                return_value = l_mapping_to[l_mapping_from.index(value)]
            else:
                self._log("Error manufacturer param mapping: Invalid filter type", s_level="error")
                return_value = 0
        elif ("FREQ" in s_parameter) or ("APASS" in s_parameter) or ("ASTOP" in s_parameter):
            if type(value) == str:
                return_value = int(float(value) * f_parameter_scaling)
            elif (type(value) == int) or (type(value) == float):
                return_value = int(value * f_parameter_scaling)
            else:
                self._log("Error manufacturer param mapping: Invalid filter data type", s_level="error")
        elif ("FILTERBAND" in s_parameter) and ("INPUT" in s_parameter):
            l_mapping_from = ["X", "Y", "Z", "XY", "XZ", "YZ", "XYZ"]
            l_mapping_to = [1, 2, 3, 4, 5, 6, 7]
            if value in l_mapping_from:
                return_value = l_mapping_to[l_mapping_from.index(value)]
            else:
                self._log("Error manufacturer param mapping: Invalid filterband input", s_level="error")
                return_value = 0
        elif ("FILTERBAND" in s_parameter) and ("RMS" in s_parameter):
            if type(value) == str:
                return_value = int(float(value) * f_parameter_scaling)
            elif (type(value) == int) or (type(value) == float):
                return_value = int(value * f_parameter_scaling)
            else:
                self._log("Error manufacturer param mapping: Invalid filterband rms", s_level="error")
        else:  # no special mapping needed
            if type(value) == str:
                if "0x" in value:
                    return_value = int(value, 16)  # convert string to base 16 integer (hex)
                else:
                    return_value = int(value, 10)  # convert string to base 10 integer
            else:
                return_value = value  # return value as it is

        return return_value

    def _set_default_param_section(self, s_parameter_type, s_param_section):  # s_param_section contains enabled string eg: FILTER1_ENABLED
        """
        Sets the default param sections
        """
        if s_parameter_type == "manufacturer":
            d_param_dict = self._manufacturer_param_dict
        elif s_parameter_type == "customer":
            d_param_dict = self._customer_param_dict
        else:
            self._log("Error set default param section: No valid parameter type " + s_parameter_type, s_level="error")
            return
        s_section, unused = s_param_section.split("_")
        if "SOS" in s_section:
            s_param = s_section + "_1_B0"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1")
            s_param = s_section + "_1_B1"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_1_B2"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_1_A0"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1")
            s_param = s_section + "_1_A1"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_1_A2"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_2_B0"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1")
            s_param = s_section + "_2_B1"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_2_B2"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_2_A0"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1")
            s_param = s_section + "_2_A1"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_2_A2"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
        elif "FILTERBAND" in s_section:
            s_param = s_section + "_INPUT"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "X")
            s_param = s_section + "_FILTERS"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_RMS"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
        elif "FILTER" in s_section:
            s_param = s_section + "_DESIGN"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "BUTTER")
            s_param = s_section + "_TYPE"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "LOWPASS")
            s_param = s_section + "_ORDER"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "4")
            s_param = s_section + "_FREQ_1"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "15")
            s_param = s_section + "_FREQ_2"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "25")
            s_param = s_section + "_APASS"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0.5")
            s_param = s_section + "_ASTOP"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "50")
        elif "RELAY" in s_section:
            s_param = s_section + "_ATTACK_MIN"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "-1000")
            s_param = s_section + "_ATTACK_MAX"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1000")
            s_param = s_section + "_ATTACK_TIME"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
            s_param = s_section + "_DECAY_MIN"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "-1000")
            s_param = s_section + "_DECAY_MAX"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1000")
            s_param = s_section + "_DECAY_TIME"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "1000")
            s_param = s_section + "_TARGET"
            d_param_dict[s_param]["data"] = self._map_parameter(s_param, "0")
        else:
            self._log("Error set default param section: No valid param section " + s_param_section, s_level="error")

    def _log(self, s_string, s_level="info"):
        """
        Logs the passed string depending on the desired log level
        Currently only print output is supported 
        """
        if self._log_level == "info":
            if s_level in ["info", "error"]:
                print(s_string)
        elif self._log_level == "error":
            if s_level in ["error"]:
                print(s_string)
        elif self._log_level == "none":
            pass
        else:
            print("Error: Invalid log level")
