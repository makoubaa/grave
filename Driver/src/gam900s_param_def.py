# start of module and package import ------------------------------------------
from collections import OrderedDict	#order of the dicts are needed
from copy import deepcopy 			#prevent references to dictionaries
from . import helper
# end of module and package import --------------------------------------------



# start of variable definition ------------------------------------------------

# start section: Parameterization
# manufacturer data: 
d_manufacturerdata = OrderedDict()
d_manufacturerdata["MANUFACTURER_DAY"] =                {"data":None,   "type":"uint8_t"}
d_manufacturerdata["MANUFACTURER_MONTH"] =              {"data":None,   "type":"uint8_t"}
d_manufacturerdata["MANUFACTURER_YEAR"] =               {"data":None,   "type":"uint8_t"}
d_manufacturerdata["MANUFACTURER_TESTER"] =             {"data":None,   "type":"uint32_t"}
d_manufacturerdata["MANUFACTURER_SERIAL_NUMBER"] =      {"data":None,   "type":"uint32_t"}
d_manufacturerdata["MANUFACTURER_DEVICEREVISION"] =     {"data":None,   "type":"uint32_t"}

# canopen parameter: 
d_canopenparam_cust = OrderedDict()
d_canopenparam_cust["CANOPEN_TERMINATOR_ACTIVE"] =      {"data":None,   "type":"uint8_t"}
d_canopenparam_man = OrderedDict()
d_canopenparam_man["s_CustomerParameter"] = d_canopenparam_cust
d_canopenparam_man["CANOPEN_NODE_ID"] =                 {"data":None,   "type":"uint8_t"} 
d_canopenparam_man["CANOPEN_BAUD_RATE"] =               {"data":None,   "type":"uint8_t"} 
d_canopenparam_man["CANOPEN_RESOLUTION"] =              {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_LED_STATUS"] =              {"data":None,   "type":"uint8_t"} 
d_canopenparam_man["CANOPEN_NMT_AUTO_START"] =          {"data":None,   "type":"uint8_t"} 
d_canopenparam_man["CANOPEN_VENDOR_ID"] =               {"data":None,   "type":"uint32_t"} 
d_canopenparam_man["CANOPEN_TPDO1_EVENT_TIME"] =        {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_TPDO2_EVENT_TIME"] =        {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_TPDO3_EVENT_TIME"] =        {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_TPDO1_COBID"] =             {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_TPDO2_COBID"] =             {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_TPDO3_COBID"] =             {"data":None,   "type":"uint16_t"} 
d_canopenparam_man["CANOPEN_TPDO1_MAPPING"] =           {"data":None,   "type":"uint64_t"} 
d_canopenparam_man["CANOPEN_TPDO2_MAPPING"] =           {"data":None,   "type":"uint64_t"} 
d_canopenparam_man["CANOPEN_TPDO3_MAPPING"] =           {"data":None,   "type":"uint64_t"} 

# filter parameter: 
u_number_filters = 15
d_filterparam = OrderedDict()
for u_filter_number in range(u_number_filters):
    d_filter = OrderedDict()
    d_filter["FILTER" + str(u_filter_number + 1) + "_FREQ_1"] =     {"data":None,   "type":"uint16_t"} 
    d_filter["FILTER" + str(u_filter_number + 1) + "_FREQ_2"] =     {"data":None,   "type":"uint16_t"} 
    d_filter["FILTER" + str(u_filter_number + 1) + "_APASS"] =      {"data":None,   "type":"uint16_t"} 
    d_filter["FILTER" + str(u_filter_number + 1) + "_ASTOP"] =      {"data":None,   "type":"uint16_t"} 
    d_filter["FILTER" + str(u_filter_number + 1) + "_DESIGN"] =     {"data":None,   "type":"uint8_t"} 
    d_filter["FILTER" + str(u_filter_number + 1) + "_TYPE"] =       {"data":None,   "type":"uint8_t"} 
    d_filter["FILTER" + str(u_filter_number + 1) + "_ORDER"] =      {"data":None,   "type":"uint8_t"} 
    d_filterparam["FILTER" + str(u_filter_number + 1)] = d_filter 

# filterband parameter: 
u_number_filterbands = 12
d_filterbandparam = OrderedDict() 
for u_filterband_number in range(u_number_filterbands): 
    d_filterband = OrderedDict() 
    d_filterband["FILTERBAND" + str(u_filterband_number + 1) + "_FILTERS"] =    {"data":None,   "type":"uint32_t"} 
    d_filterband["FILTERBAND" + str(u_filterband_number + 1) + "_RMS"] =        {"data":None,   "type":"uint16_t"} 
    d_filterband["FILTERBAND" + str(u_filterband_number + 1) + "_INPUT"] =      {"data":None,   "type":"uint8_t"} 
    d_filterbandparam["FILTERBAND" + str(u_filterband_number + 1)] = d_filterband 

# second order section banks parameter 
u_number_sosbanks = 4 
u_number_sos_per_bank = 2 
d_sosbankparam = OrderedDict() 
for u_sosbank_number in range(u_number_sosbanks): 
    d_sosbank = OrderedDict() 
    for u_sos_number in range(u_number_sos_per_bank): 
        d_sos = OrderedDict() 
        d_sos["SOS" + str(u_sosbank_number + 1) + "_" + str(u_sos_number + 1) + "_B0"] = {"data":None,  "type":"float64_t"} 
        d_sos["SOS" + str(u_sosbank_number + 1) + "_" + str(u_sos_number + 1) + "_B1"] = {"data":None,  "type":"float64_t"} 
        d_sos["SOS" + str(u_sosbank_number + 1) + "_" + str(u_sos_number + 1) + "_B2"] = {"data":None,  "type":"float64_t"} 
        d_sos["SOS" + str(u_sosbank_number + 1) + "_" + str(u_sos_number + 1) + "_A0"] = {"data":None,  "type":"float64_t"} 
        d_sos["SOS" + str(u_sosbank_number + 1) + "_" + str(u_sos_number + 1) + "_A1"] = {"data":None,  "type":"float64_t"} 
        d_sos["SOS" + str(u_sosbank_number + 1) + "_" + str(u_sos_number + 1) + "_A2"] = {"data":None,  "type":"float64_t"} 
        d_sosbank["SOS" + str(u_sos_number + 1)] = d_sos 
    d_sosbankparam["SOSBANK" + str(u_sosbank_number + 1)] = d_sosbank 

#handler filterbands parameterization: 
#customer parameterization(filter param, filterband param), manufacturer param(sos param) 
d_handlerfilterbandsparam_cust = OrderedDict() 
d_handlerfilterbandsparam_man = OrderedDict() 
d_handlerfilterbandsparam_cust["as_FilterParameter"] = d_filterparam 
d_handlerfilterbandsparam_cust["as_FilterbandParameter"] = d_filterbandparam 
d_handlerfilterbandsparam_man["s_CustomerParameter"] = d_handlerfilterbandsparam_cust 
d_handlerfilterbandsparam_man["as_SosBankParam"] = d_sosbankparam 

# dac parameter: 
u_number_dacs = 2 
d_dacparam_cust = OrderedDict() 
d_dacparam_man = OrderedDict() 
for u_dac_number in range(u_number_dacs): 
    d_dac = OrderedDict() 
    d_dac["DAC" + str(u_dac_number + 1) + "_INPUT_FB"] =    {"data":None,   "type":"uint8_t"} 
    d_dac["DAC" + str(u_dac_number + 1) + "_MIN"] =         {"data":None,   "type":"int16_t"} 
    d_dac["DAC" + str(u_dac_number + 1) + "_MAX"] =         {"data":None,   "type":"int16_t"} 
    d_dacparam_cust["DAC" + str(u_dac_number + 1)] = d_dac 
d_dacparam_cust["DAC_TYPE"] =                               {"data":None,   "type":"uint8_t"} 
d_dacparam_man["s_CustomerParameter"] = d_dacparam_cust 
d_dacparam_man["DAC_AVAILABLE"] =                           {"data":None,   "type":"uint8_t"} 

# relay parameter: 
d_relayparam = OrderedDict() 
u_number_relays = 12 
for u_relay_number in range(u_number_relays): 
    d_relay = OrderedDict() 
    d_relay["RELAY" + str(u_relay_number + 1) + "_ATTACK_MIN"] =        {"data":None,   "type":"int16_t"} 
    d_relay["RELAY" + str(u_relay_number + 1) + "_ATTACK_MAX"] =        {"data":None,   "type":"int16_t"} 
    d_relay["RELAY" + str(u_relay_number + 1) + "_ATTACK_TIME"] =       {"data":None,   "type":"uint16_t"} 
    d_relay["RELAY" + str(u_relay_number + 1) + "_DECAY_MIN"] =         {"data":None,   "type":"int16_t"} 
    d_relay["RELAY" + str(u_relay_number + 1) + "_DECAY_MAX"] =         {"data":None,   "type":"int16_t"} 
    d_relay["RELAY" + str(u_relay_number + 1) + "_DECAY_TIME"] =        {"data":None,   "type":"uint16_t"} 
    d_relay["RELAY" + str(u_relay_number + 1) + "_TARGET"] =            {"data":None,   "type":"uint8_t"} 
    d_relayparam["RELAY" + str(u_relay_number + 1)] = d_relay 
d_relayparam["SAFETY_RELAY_LATCHED"] =                                  {"data":None,   "type":"uint32_t"} 

# sensor parameter: 
d_sensorparam = OrderedDict() 
d_sensorparam["SENSOR_FULL_SCALE_RANGE"] =              {"data":None,   "type":"uint8_t"} 

# plausibility parameter: 
d_plausibilityparam = OrderedDict() 
d_plausibilityparam["PLAUSIBILITY_FREQ_STAGE1"] =       {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_FREQ_STAGE2"] =       {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_FREQ_STAGE3"] =       {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_APASS_MIN"] =         {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_APASS_MAX"] =         {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_APASS_STEPSIZE"] =    {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_ASTOP_MIN"] =         {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_ASTOP_MAX"] =         {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_ASTOP_STEPSIZE"] =    {"data":None,   "type":"uint16_t"} 
d_plausibilityparam["PLAUSIBILITY_ORDER_MAX"] =         {"data":None,   "type":"uint8_t"} 

# test in parameter: 
_u_Ref_TestInMode = 0
d_testinparam = OrderedDict()
d_testinparam["TEST_IN_VARIANT"] =                      {"data":None, 	"type":"uint8_t"}

#customer parameter/package: 
_u_Ref_CustomerCRC = 0; 
d_customerpackage = OrderedDict() 
d_customerparam = OrderedDict() 
d_customerparam["s_MyCANOpenCustomerParameter"] = deepcopy(d_canopenparam_cust) 
d_customerparam["s_MyHandlerFilterbandsCustomerParameter"] = deepcopy(d_handlerfilterbandsparam_cust) 
d_customerparam["s_MyDacCustomerParameter"] = deepcopy(d_dacparam_cust) 
d_customerparam["s_MyRelayParameter"] = deepcopy(d_relayparam) 
d_customerparam["s_MySensorParameter"] = deepcopy(d_sensorparam) 
d_customerparam["s_MyTestInParameter"] = deepcopy(d_testinparam) 
d_customerpackage["s_MyCustomerParameter"] = deepcopy(d_customerparam) 
d_customerpackage["CRC"] = 	{"data":_u_Ref_CustomerCRC, "type":"uint32_t"} 

# manufacturer parameter/package: 
d_manufacturerpackage = OrderedDict() 
d_manufacturerparam = OrderedDict() 
d_manufacturerparam["s_MyCANOpenParameter"] = deepcopy(d_canopenparam_man) 
d_manufacturerparam["s_MyHandlerFilterbandsParameter"] = deepcopy(d_handlerfilterbandsparam_man) 
d_manufacturerparam["s_MyDacParameter"] = deepcopy(d_dacparam_man) 
d_manufacturerparam["s_MyRelayParameter"] = deepcopy(d_relayparam) 
d_manufacturerparam["s_MySensorParameter"] = deepcopy(d_sensorparam) 
d_manufacturerparam["s_MyPlausibilityParameter"] = deepcopy(d_plausibilityparam) 
d_manufacturerparam["s_MyTestInParameter"] = deepcopy(d_testinparam) 
d_manufacturerpackage["s_MyManufacturerData"] = deepcopy(d_manufacturerdata) 
d_manufacturerpackage["s_MyManufacturerParameter"] = deepcopy(d_manufacturerparam) 
d_manufacturerpackage["ADMIN_PASSWORD_MANUFACTURER"] =  {"data":None,   "type":"uint32_t"} 
d_manufacturerpackage["CRC"] =                          {"data":None,   "type":"uint32_t"} 

#delete intermediate structures defined above which are now part of the packages 
del d_canopenparam_man 
del d_canopenparam_cust 
del d_handlerfilterbandsparam_man 
del d_handlerfilterbandsparam_cust 
del d_dacparam_man 
del d_dacparam_cust 
del d_relayparam 
del d_sensorparam 
del d_plausibilityparam 
del d_testinparam 
del d_manufacturerdata 
del d_manufacturerparam 
del d_customerparam 

# end section: Parameterization
# end of variable definition -------------------------------------------------- 



# start of function definition ------------------------------------------------ 

def l_GetParameterizationList( s_ParameterizationType ): 
    l_ParameterizationList = [] 
    if s_ParameterizationType == "Manufacturer parameterization": 
        d_manufacturerpackage["CRC"]["data"] = u_GetChecksum( d_manufacturerpackage["s_MyManufacturerParameter"] ) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerData"] ),                                                                                             "s_obj":"Manufacturer Data"     }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyCANOpenParameter"] ),                                                                "s_obj":"CANopen Param"         }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyHandlerFilterbandsParameter"]["s_CustomerParameter"]["as_FilterParameter"] ),        "s_obj":"Filter Param"          }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyHandlerFilterbandsParameter"]["s_CustomerParameter"]["as_FilterbandParameter"] ),    "s_obj":"Filterband Param"      }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyHandlerFilterbandsParameter"]["as_SosBankParam"] ),                                  "s_obj":"SOS Param"             }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyDacParameter"] ),                                                                    "s_obj":"DAC Param"             }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyRelayParameter"] ),                                                                  "s_obj":"Relay Param"           }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MySensorParameter"] ),                                                                 "s_obj":"Misc Param"            }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyPlausibilityParameter"] ),                                                           "s_obj":"Plausibility Param"    }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_manufacturerpackage["s_MyManufacturerParameter"]["s_MyTestInParameter"] ),                                                                 "s_obj":"Misc Param"            }) 
        l_ParameterizationList.append({"l_data":{key:value for key, value in d_manufacturerpackage.items() if key == "CRC"},                                                                                    "s_obj":"Misc Param"            }) 
        l_ParameterizationList.append({"l_data":{key:value for key, value in d_manufacturerpackage.items() if key == "ADMIN_PASSWORD_MANUFACTURER"},                                                            "s_obj":"Misc Param"            }) 
    elif s_ParameterizationType == "Customer parameterization": 
        d_customerpackage["CRC"]["data"] = u_GetChecksum( d_customerpackage["s_MyCustomerParameter"] ) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MyCANOpenCustomerParameter"] ),                                        "s_obj":"CANopen Param"     }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MyHandlerFilterbandsCustomerParameter"]["as_FilterParameter"] ),       "s_obj":"Filter Param"      }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MyHandlerFilterbandsCustomerParameter"]["as_FilterbandParameter"] ),   "s_obj":"Filterband Param"  }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MyDacCustomerParameter"] ),                                            "s_obj":"DAC Param"         }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MyRelayParameter"] ),                                                  "s_obj":"Relay Param"       }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MySensorParameter"] ),                                                 "s_obj":"Misc Param"        }) 
        l_ParameterizationList.append({"l_data":d_DeepflattenDict( d_customerpackage["s_MyCustomerParameter"]["s_MyTestInParameter"] ),                                                 "s_obj":"Misc Param"        }) 
        l_ParameterizationList.append({"l_data":{key:value for key, value in d_customerpackage.items() if key == "CRC"},                                                                "s_obj":"Misc Param"        }) 
    else: 
        print("Parameterization type not supported") 
        return 

    return l_ParameterizationList 


def u_GetChecksum( input_value ): 
    if type(input_value) == OrderedDict: 
        d_struct = input_value                                                  #input value is dict > use dict 
    elif type(input_value) == str: 
        if input_value == "Manufacturer parameterization":                      #input value is string > lookup dict 
            d_struct = d_manufacturerparam 
        elif input_value == "Customer parameterization": 
            d_struct = d_customerparam 
        else: 
            print("Invalid string for checksum calculation")                    #dict identifier not found > return 
            return 
    else: 
        print("Invalid input value for checksum calculation")                   #dict identifier not found > return 
        return 

    l_MemoryImage = l_BuildMemoryImageFromStruct( d_struct ) 
    u_Checksum = u_GetChecksumFromMemoryImage( l_MemoryImage ) 
    return u_Checksum 


def l_BuildMemoryImageFromStruct( d_struct ): 
    if "u_IterationDepth" not in l_BuildMemoryImageFromStruct.__dict__: 
        l_BuildMemoryImageFromStruct.u_IterationDepth = 0                       #define function attribute upon first call 
    if l_BuildMemoryImageFromStruct.u_IterationDepth == 0: 
        l_BuildMemoryImageFromStruct.l_MemoryImage = []                         #define or reset attributes upon non iterative call 
        l_BuildMemoryImageFromStruct.u_ByteCount = 0 

    u_Padding = 0x00 
    l_BuildMemoryImageFromStruct.u_IterationDepth += 1 

    #Structure pre padding (open structure) 
    #http://www.catb.org/esr/structure-packing/ 
    #http://www.keil.com/support/man/docs/armcc/armcc_chr1360774870320.htm 
    u_LargestMember = u_GetLargestMember( d_struct ) 
    u_Residual = l_BuildMemoryImageFromStruct.u_ByteCount % u_LargestMember 
    if u_Residual != 0: 
        u_PaddingNumber = u_LargestMember - u_Residual 
        l_BuildMemoryImageFromStruct.l_MemoryImage.extend( [u_Padding] * u_PaddingNumber ) 
        l_BuildMemoryImageFromStruct.u_ByteCount += u_PaddingNumber 

    for key, value in d_struct.items(): 
        if "type" in value:                                                     #atomic parameter found > append data to memory 
                u_DataSize = helper.u_get_size_from_type ( value["type"] ) 
                u_Residual = l_BuildMemoryImageFromStruct.u_ByteCount % u_DataSize 
                if u_Residual != 0:     #Field padding 
                    u_PaddingNumber = u_DataSize - u_Residual 
                    l_BuildMemoryImageFromStruct.l_MemoryImage.extend( [u_Padding] * u_PaddingNumber ) 
                    l_BuildMemoryImageFromStruct.u_ByteCount += u_PaddingNumber 
                l_DataList = helper.l_data_to_list ( value["data"], value["type"] ) 
                l_BuildMemoryImageFromStruct.l_MemoryImage.extend( l_DataList ) 
                l_BuildMemoryImageFromStruct.u_ByteCount += u_DataSize 
        else: 
            l_BuildMemoryImageFromStruct( value )                               #dict struct found > iterate 

    #Structure post padding (close structure) 
    u_Residual = l_BuildMemoryImageFromStruct.u_ByteCount % u_LargestMember 
    if u_Residual != 0: 
        u_PaddingNumber = u_LargestMember - u_Residual 
        l_BuildMemoryImageFromStruct.l_MemoryImage.extend( [u_Padding] * u_PaddingNumber ) 
        l_BuildMemoryImageFromStruct.u_ByteCount += u_PaddingNumber 

    l_BuildMemoryImageFromStruct.u_IterationDepth -= 1 
    return l_BuildMemoryImageFromStruct.l_MemoryImage 


def u_GetLargestMember( d_struct ): 
    u_LargestMember = 0 
    u_ItemSize = 0

    for key, value in d_struct.items(): 
        if "type" in value: 
            u_ItemSize = helper.u_get_size_from_type( value["type"] )           #atomic parameter found > get size 
        else: 
            u_ItemSize = u_GetLargestMember( value )                            #dict struct found > iterate 

        if type(u_ItemSize) == type(None) or type(u_LargestMember) == type(None): 
            print(key, value) 
        elif u_ItemSize > u_LargestMember: 
            u_LargestMember = u_ItemSize 

    return u_LargestMember 


#https://www.st.com/content/ccc/resource/technical/document/application_note/39/89/da/89/9e/d7/49/b1/DM00068118.pdf/files/DM00068118.pdf/jcr:content/translations/en.DM00068118.pdf 
def u_GetChecksumFromMemoryImage( l_MemoryImage ): 
    u_BytesPerBlock = 4       #CRC over 4byte blocks 
    u_BitsPerBlock = 32       #CRC over 32bit blocks 
    u_BitsPerByte = 8 
    u_MemoryLength = len( l_MemoryImage ) 
    u_Crc32MSB = 0x80000000 
    u_32BitMask = 0xFFFFFFFF 
    u_CrcPoly = 0x04C11DB7 
    u_Crc32 = 0xFFFFFFFF 

    if (u_MemoryLength % u_BytesPerBlock) != 0: 
        print ("Error: Invald image length") 
        return

    for u_BlockCount in range(u_MemoryLength // u_BytesPerBlock): 
        u_BlockStream = 0 
        for u_ByteCount in range(u_BytesPerBlock): 
            u_BlockStream += (l_MemoryImage[(u_BlockCount * u_BytesPerBlock) + u_ByteCount]) << (u_ByteCount * u_BitsPerByte) 
        u_Crc32 = u_Crc32 ^ u_BlockStream; 
        for u_BitCount in range(u_BitsPerBlock): 
            if (u_Crc32 & u_Crc32MSB) != 0: 
                u_Crc32 = ((u_Crc32 << 1) & u_32BitMask) ^ u_CrcPoly 
            else: 
                u_Crc32 = (u_Crc32 << 1) & u_32BitMask 

    return u_Crc32 


def v_PrintMemDump( l_MemoryImage, u_StartAddress ): 
    u_Address = u_StartAddress 
    u_BytesPerLine = 16 
    u_BlockCount = 0 
    u_AddressOffset = 0 

    u_MemorySize = len(l_MemoryImage) 
    fp = open("memdump.txt", "w") 

    while (u_AddressOffset + u_BytesPerLine) < u_MemorySize: 
        s_LineString = "0x{:08X}  {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}".format(u_Address, l_MemoryImage[u_AddressOffset], l_MemoryImage[u_AddressOffset+1], l_MemoryImage[u_AddressOffset+2], l_MemoryImage[u_AddressOffset+3], 
                                                                                                    l_MemoryImage[u_AddressOffset+4], l_MemoryImage[u_AddressOffset+5], l_MemoryImage[u_AddressOffset+6], l_MemoryImage[u_AddressOffset+7]) 
        s_LineString += " - {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}".format(l_MemoryImage[u_AddressOffset+8], l_MemoryImage[u_AddressOffset+9], l_MemoryImage[u_AddressOffset+10], l_MemoryImage[u_AddressOffset+11], 
                                                                                            l_MemoryImage[u_AddressOffset+12], l_MemoryImage[u_AddressOffset+13], l_MemoryImage[u_AddressOffset+14], l_MemoryImage[u_AddressOffset+15]) 
        s_LineString += "\n" 
        fp.write( s_LineString ) 
        u_BlockCount += 1 
        u_AddressOffset = u_BlockCount * u_BytesPerLine 
        u_Address = u_StartAddress + u_AddressOffset 
    fp.close() 


def l_DeepflattenList( l_List ): 
    l_ReturnList = [] 

    for item in l_List: 
        if type(item) == list: 
            l_ReturnList.extend( l_DeepflattenList(item) ) 
        else: 
            l_ReturnList.append( item ) 

    return l_ReturnList 


def d_DeepflattenDict( l_dict ): 
    d_return_dict = OrderedDict() 

    if (type(l_dict) != OrderedDict): 
        print("Invalid dict type") 
        return 

    for key, value in l_dict.items(): 
        if "data" in value: 
            d_return_dict[key] = value                                          #atomic parameter found > add to dict 
        else: 
            d_flattened_dict = d_DeepflattenDict(value)                         #dict found > add flattened dict 
            for key_flattened, value_flattened in d_flattened_dict.items(): 
                d_return_dict[key_flattened] = value_flattened 

    return d_return_dict 
# end of function definition -------------------------------------------------- 



# start of script execution --------------------------------------------------- 
# end of script execution ----------------------------------------------------- 
