# start of module and package import ------------------------------------------
import struct
# end of module and package import --------------------------------------------


# start of variable definition ------------------------------------------------
# end of variable definition --------------------------------------------------


# start of private function definition ----------------------------------------
def _b_ui8_to_bytes(u8_number):
    return struct.pack("B", int(round(u8_number)))
def _b_i8_to_bytes(i8_number):
    return struct.pack("b", int(round(i8_number)))
def _b_u16_to_bytes(u16_number):
    return struct.pack("H", int(round(u16_number)))
def _b_i16_to_bytes(i16_number):
    return struct.pack("h", int(round(i16_number)))
def _b_u32_to_bytes(u32_number):
    return struct.pack("L", int(round(u32_number)))
def _b_i32_to_bytes(i32_number):
    return struct.pack("l", int(round(i32_number)))
def _b_u64_to_bytes(u64_number):
    return struct.pack("Q", int(round(u64_number)))
def _b_i64_to_bytes(i64_number):
    return struct.pack("q", int(round(i64_number)))
def _b_f32_to_bytes(f32_number):
    return struct.pack("f", f32_number)
def _b_f64_to_bytes(f64_number):
    return struct.pack("d", f64_number)  
    
def _ui8_bytes_to_uint8(b_bytes):
    return struct.unpack("B", b_bytes)[0]
def _i8_bytes_to_int8(b_bytes):
    return struct.unpack("b", b_bytes)[0]
def _ui16_bytes_to_uint16(b_bytes):
    return struct.unpack("H", b_bytes)[0]
def _i16_bytes_to_int16(b_bytes):
    return struct.unpack("h", b_bytes)[0]
def _ui32_bytes_to_uint32(b_bytes):
    return struct.unpack("L", b_bytes)[0]
def _i32_bytes_to_int32(b_bytes):
    return struct.unpack("l", b_bytes)[0]
def _ui64_bytes_to_uint64(b_bytes):
    return struct.unpack("Q", b_bytes)[0]
def _i64_bytes_to_int64(b_bytes):
    return struct.unpack("q", b_bytes)[0]
def _f32_bytes_to_float32(b_bytes):
    return struct.unpack("f", b_bytes)[0]
def _f64_bytes_to_float64(b_bytes):
    return struct.unpack("d", b_bytes)[0]
# end of private function definition ------------------------------------------


# start of public function definition -----------------------------------------
def hexstring_to_data( s_hexstring, s_data_type, u_offset=0, s_endianness="big" ): 
    assert s_hexstring != None, "Assert in function hexstring_to_data: Passed hexstring shall not be None"
    assert s_data_type != None, "Assert in function hexstring_to_data: Passed type shall not be None"
    assert s_endianness == "little" or s_endianness == "big", "Assert in function hexstring_to_data: Passed endiannes shall not be unequal little or big"        
    u_size_in_bytes = u_get_size_from_type( s_data_type )
    u_number_characters = u_size_in_bytes * 2
    b_bytes = int(s_hexstring[u_offset:(u_offset+u_number_characters)], 16).to_bytes(u_size_in_bytes, byteorder=s_endianness)
    data = bytes_to_data(b_bytes, s_data_type, s_endianness=s_endianness)
    return data    


def s_data_to_hexstring( data, s_data_type, s_endianness="big" ): 
    assert data != None, "Assert in function s_data_to_hexstring: Passed data shall not be None"
    assert s_data_type != None, "Assert in function list_to_data: Passed type shall not be None"
    assert s_endianness == "little" or s_endianness == "big", "Assert in function list_to_data: Passed endiannes shall not be unequal little or big"        
    l_data_list = l_data_to_list( data, s_data_type, s_endianness=s_endianness )
    if l_data_list == None:
        return None
    s_return_string = ""
    for i in l_data_list:
        s_return_string += '{:02X}'.format(i)			#append string in two character hexadecimal number format
    return s_return_string


def list_to_data( l_list, s_data_type, s_endianness="little" ): 
    assert l_list != None, "Assert in function list_to_data: Passed list shall not be None"
    assert s_data_type != None, "Assert in function list_to_data: Passed type shall not be None"
    assert s_endianness == "little" or s_endianness == "big", "Assert in function list_to_data: Passed endiannes shall not be unequal little or big"        
    return bytes_to_data( bytes(l_list), s_data_type, s_endianness=s_endianness )


def l_data_to_list( data, s_data_type, s_endianness="little" ): 
    assert data != None, "Assert in function l_data_to_list: Passed data shall not be None"
    assert s_data_type != None, "Assert in function l_data_to_list: Passed type shall not be None"
    assert s_endianness == "little" or s_endianness == "big", "Assert in function l_data_to_list: Passed endiannes shall not be unequal little or big"        
    return list(b_data_to_bytes( data, s_data_type, s_endianness=s_endianness ))
    
    
def b_data_to_bytes( data, s_data_type, s_endianness="little" ): 
    assert data != None, "Assert in function b_data_to_bytes: Passed data shall not be None"
    assert s_data_type != None, "Assert in function b_data_to_bytes: Passed type shall not be None"
    assert s_endianness == "little" or s_endianness == "big", "Assert in function b_data_to_bytes: Passed endiannes shall not be unequal little or big"    
    if s_data_type == "uint8_t":
        b_bytes = _b_ui8_to_bytes(data)
    elif s_data_type == "int8_t":
        b_bytes = _b_i8_to_bytes(data)
    elif s_data_type == "uint16_t":
        b_bytes = _b_u16_to_bytes(data)
    elif s_data_type == "int16_t":
        b_bytes = _b_i16_to_bytes(data)
    elif s_data_type == "uint32_t":
        b_bytes = _b_u32_to_bytes(data)
    elif s_data_type == "int32_t":        
        b_bytes = _b_i32_to_bytes(data)
    elif s_data_type == "uint64_t":        
        b_bytes = _b_u64_to_bytes(data)
    elif s_data_type == "int64_t":
        b_bytes = _b_i64_to_bytes(data)
    elif s_data_type == "float32_t":
        b_bytes = _b_f32_to_bytes(data)
    elif s_data_type == "float64_t":
        b_bytes = _b_f64_to_bytes(data)
    else:
        print("Invalid data type")
        return None     
    if s_endianness == "big":
        b_bytes = b_bytes[::-1]    #pack returns little endianness > for big endianness bytes must be swapped
    return b_bytes


def bytes_to_data( b_bytes, s_data_type, s_endianness="little" ):
    assert b_bytes != None, "Assert in function bytes_to_data: Passed byte shall not be None"
    assert s_data_type != None, "Assert in function bytes_to_data: Passed type shall not be None"
    assert s_endianness == "little" or s_endianness == "big", "Assert in function bytes_to_data: Passed endiannes shall not be unequal little or big"
    if s_endianness == "big":
        b_bytes = b_bytes[::-1]    #pack expects little endianness > for big endianness bytes must be swapped    
    if s_data_type == "uint8_t":
        data = _ui8_bytes_to_uint8(b_bytes)
    elif s_data_type == "int8_t":
        data = _i8_bytes_to_int8(b_bytes)
    elif s_data_type == "uint16_t":
        data = _ui16_bytes_to_uint16(b_bytes)
    elif s_data_type == "int16_t":
        data = _i16_bytes_to_int16(b_bytes)
    elif s_data_type == "uint32_t":
        data = _ui32_bytes_to_uint32(b_bytes)
    elif s_data_type == "int32_t":        
        data = _i32_bytes_to_int32(b_bytes)
    elif s_data_type == "uint64_t":        
        data = _ui64_bytes_to_uint64(b_bytes)
    elif s_data_type == "int64_t":
        data = _i64_bytes_to_int64(b_bytes)
    elif s_data_type == "float32_t":
        data = _f32_bytes_to_float32(b_bytes)
    elif s_data_type == "float64_t":
        data = _f64_bytes_to_float64(b_bytes)
    else:
        print("Invalid data type")
        return None     
    return data    
    
def u_get_size_from_type (s_type):
    assert s_type != None, "Assert in function u_get_size_from_type: Passed type shall not be None" 
    u_size = 0
    if (s_type == "uint8_t") or (s_type == "int8_t"):
        u_size = 1
    elif (s_type == "uint16_t") or (s_type == "int16_t"):
        u_size = 2
    elif (s_type == "uint32_t") or (s_type == "int32_t") or (s_type == "float32_t"):
        u_size = 4
    elif (s_type == "uint64_t") or (s_type == "int64_t") or (s_type == "float64_t"):
        u_size = 8
    else:
        print("Error: Invalid type specifier")
        return None
    return u_size    
# end of public function definition -------------------------------------------


# start of script execution ---------------------------------------------------
# end of script execution -----------------------------------------------------
