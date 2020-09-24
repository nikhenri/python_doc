IPv4:
    docParser_base_str: "OTI_IPV4_BASE_ADD"
    register:
        0x0:
            name: "IPV4_IP_ADDR"
            type: "RW"
            desc: "ip address of offload engine"
            field: 
                31-0:
                    name: "IP_ADD"
                    rst: "0x13356219"
                    desc: "ip address of offload engine"
        
        0x4: 
            name: "IPV4_SUB_NET_MASK"
            type: "RW"
            desc: "sub net mask"
            field: 
                31-0: 
                    name: "SUBNET_MASK"
                    rst: "0XFFFFFF00"
                    desc: "sub net mask"

        0x8: 
            name: "IPV4_DEFAULT_GATEWAY"
            type: "RW"
            desc: "default gateway"    
            field: 
                31-0: 
                    name: "DFLT_GW"
                    rst: "0x0"
                    desc: "default gateway"

        0xC: 
            name: "IPV4_TX_FRAME_CNT"
            type: "RO"
            desc: "increment at each frame sent to l2"
            field: 
                31-0: 
                    name: "TX_FRAME_CNT"
                    rst: "0x0"
                    desc: "increment at each frame sent to l2"

        0x10: 
            name: "IPV4_RX_FRAME_CNT"
            type: "RO"
            desc: "increment at each frame received from l2. increment even frame contain error"
            field: 
                31-0: 
                    name: "RX_FRAME_CNT"
                    rst: "0x0"
                    desc: "increment at each frame received from l2. increment even frame contain error"
                
        0x14: 
            name: "IPV4_RX_ERROR_CHECKSUM_CNT"
            type: "RO"
            desc: "increment each time a checksum error is detected in the ipv4 header"
            field: 
                31-0: 
                    name: "RX_ERROR_CHECKSUM_CNT"
                    rst: "0x0"
                    desc: "increment each time a checksum error is detected in the ipv4 header"

        0x18: 
            name: "IPV4_RX_ERROR_HEADER_CNT"
            type: "RO"
            desc: "increment each time the ipv4 header version not equal to 4 or hls not equal to 5 or flags not equal to 2"
            field: 
                31-0: 
                    name: "RX_ERROR_HEADER_CNT"
                    rst: "0x0"
                    desc: "increment each time the ipv4 header version not equal to 4 or hls not equal to 5 or flags not equal to 2"

        0x1C:
            name: "IPV4_STATUS"
            type: "RO"
            desc: "ipv4 status"
            field:
                0:
                    name: "DFLT_GW_TABLE_ID_VALID"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

        0x20:
            name: "TEST1"
            type: "RO"
            desc: "TEST1"
            field:
                31:
                    name: "DFLT_GW_TABLE_ID_VALID31"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

                9-5:
                    name: "DFLT_GW_TABLE_ID_VALID9_5"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

                3:
                    name: "DFLT_GW_TABLE_ID_VALID3"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

                0:
                    name: "DFLT_GW_TABLE_ID_VALID0"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"



        0x24:
            name: "TEST2"
            type: "RO"
            desc: "TEST1"
            field:
                30:
                    name: "DFLT_GW_TABLE_ID_VALID30"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

                29-9:
                    name: "DFLT_GW_TABLE_ID_VALID29_9"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

                1:
                    name: "DFLT_GW_TABLE_ID_VALID1"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"

        0x28:
            name: "TEST3"
            type: "RO"
            desc: "TEST1"
            field:
                3:
                    name: "DFLT_GW_TABLE_ID_VALID33"
                    rst: "0x0"
                    desc: "Indicate the IPv4 default gateway MAC address is resolved"


        0x28:
            name: "TEST4"
            type: "RW"
            desc: "TEST4"
            field:
                64-63:
                    name: "DFLT_GW_TABLE_ID_VALID64"
                    rst: "0x0"
                    desc: "Indicate nothing"