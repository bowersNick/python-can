# ///////////////////////////////////////////////////////////
# Type definitions
# ///////////////////////////////////////////////////////////
from ctypes import *

XLStatus 				= c_ubyte
XLBusTypes				= c_ulong
XLHwTypes				= c_ubyte
XLInterfaceVersion      = c_ubyte
XLFlag                  = c_uint16
XLTag                   = c_uint8
XLaccess                = c_uint64

XL_CONFIG_MAX_CHANNELS = 64
XL_MAX_LENGTH = 31

XL_CAN_EXT_MSG_ID           = c_uint32(0x80000000)


XL_CAN_MSG_FLAG_ERROR_FRAME = XLFlag(0x1) #The event is an error frame (rx*).
XL_CAN_MSG_FLAG_OVERRUN     = XLFlag(0x2)#An overrun occurred, events have been lost (rx, tx*).
XL_CAN_MSG_FLAG_NERR        = XLFlag(0x4)#The transceiver reported an error while the message was received (rx*).
XL_CAN_MSG_FLAG_WAKEUP      = XLFlag(0x8)#High voltage message for Single Wire (rx, tx*). To flush the queue and transmit a high voltage message combine the flags
XL_CAN_MSG_FLAG_REMOTE_FRAME= XLFlag(0x10) #The event is a remote frame (rx, tx*).
XL_CAN_MSG_FLAG_RESERVED_1  = XLFlag(0x20)
XL_CAN_MSG_FLAG_TX_COMPLETED= XLFlag(0x40) #Notification for successful message transmission (rx*).
XL_CAN_MSG_FLAG_TX_REQUEST  = XLFlag(0x80)#Request notification for message transmission (rx*).
XL_CAN_MSG_FLAG_SRR_BIT_DOM = XLFlag(0x0200)


# //
# // common event tags
# //
XL_RECEIVE_MSG                          = XLTag(0x0001)
XL_CHIP_STATE                           = XLTag(0x0004)
XL_TRANSCEIVER_INFO                     = XLTag(0x0006)
XL_TRANSCEIVER                          = (XL_TRANSCEIVER_INFO)
XL_TIMER_EVENT                          = XLTag(0x0008)
XL_TIMER                                = (XL_TIMER_EVENT)
XL_TRANSMIT_MSG                         = XLTag(0x000A)
XL_SYNC_PULSE                           = XLTag(0x000B)
XL_APPLICATION_NOTIFICATION             = XLTag(0x000F)
# ///////////////////////////////////////////////////////////
# Value definitions
# ///////////////////////////////////////////////////////////

# Currently defined and supported PCAN channels
#
XL_SUCCESS					= XLStatus(0)
XL_ERR_QUEUE_IS_EMPTY		= XLStatus(10)
XL_ERR_QUEUE_IS_FULL		= XLStatus(11)
XL_ERR_TX_NOT_POSSIBLE		= XLStatus(12)
XL_ERR_NO_LICENSE			= XLStatus(14)
XL_ERR_WRONG_PARAMETER		= XLStatus(101)
XL_ERR_INVALID_CHAN_INDEX	= XLStatus(111)
XL_ERR_INVALID_ACCESS		= XLStatus(112)
XL_ERR_PORT_IS_OFFLINE		= XLStatus(113)
XL_ERR_CHAN_IS_ONLINE		= XLStatus(116)
XL_ERR_NOT_IMPLEMENTED		= XLStatus(117)
XL_ERR_INVALID_PORT			= XLStatus(118)
XL_ERR_HW_NOT_READY			= XLStatus(120)
XL_ERR_CMD_TIMEOUT			= XLStatus(121)
XL_ERR_HW_NOT_PRESENT		= XLStatus(129)
XL_ERR_INIT_ACCESS_MISSING	= XLStatus(158)
XL_ERR_CANNOT_OPEN_DRIVER	= XLStatus(201)
XL_ERR_WRONG_BUS_TYPE		= XLStatus(202)
XL_ERR_DLL_NOT_FOUND		= XLStatus(203)
XL_ERR_INVALID_CHANNEL_MASK	= XLStatus(204)
XL_ERR_NOT_SUPPORTED		= XLStatus(205)
XL_ERROR					= XLStatus(255)

XL_BUS_TYPE_NONE			= XLBusTypes(0x00000000)
XL_BUS_TYPE_CAN				= XLBusTypes(0x00000001)
XL_BUS_TYPE_LIN				= XLBusTypes(0x00000002)
XL_BUS_TYPE_FLEXRAY			= XLBusTypes(0x00000004)
XL_BUS_TYPE_AFDX			= XLBusTypes(0x00000008)
XL_BUS_TYPE_MOST			= XLBusTypes(0x00000010)
XL_BUS_TYPE_DAIO			= XLBusTypes(0x00000040)
XL_BUS_TYPE_J1708			= XLBusTypes(0x00000100)
XL_BUS_TYPE_ETHERNET		= XLBusTypes(0x00001000)

#activate - channel flags
XL_ACTIVATE_NONE            = 0
XL_ACTIVATE_RESET_CLOCK     = 8

XL_BUS_COMPATIBLE_CAN       = XL_BUS_TYPE_CAN
XL_BUS_COMPATIBLE_LIN       = XL_BUS_TYPE_LIN
XL_BUS_COMPATIBLE_FLEXRAY   = XL_BUS_TYPE_FLEXRAY
XL_BUS_COMPATIBLE_MOST      = XL_BUS_TYPE_MOST
XL_BUS_COMPATIBLE_DAIO      = XL_BUS_TYPE_DAIO          #//io cab/piggy
XL_BUS_COMPATIBLE_J1708     = XL_BUS_TYPE_J1708
XL_BUS_COMPATIBLE_ETHERNET  = XL_BUS_TYPE_ETHERNET

# the following bus types can be used with the current cab / piggy
XL_BUS_ACTIVE_CAP_CAN       = (XL_BUS_COMPATIBLE_CAN.value << 16)
XL_BUS_ACTIVE_CAP_LIN       = (XL_BUS_COMPATIBLE_LIN.value << 16)
XL_BUS_ACTIVE_CAP_FLEXRAY   = (XL_BUS_COMPATIBLE_FLEXRAY.value << 16)
XL_BUS_ACTIVE_CAP_MOST      = (XL_BUS_COMPATIBLE_MOST.value << 16)
XL_BUS_ACTIVE_CAP_DAIO      = (XL_BUS_COMPATIBLE_DAIO.value << 16)
XL_BUS_ACTIVE_CAP_J1708     = (XL_BUS_COMPATIBLE_J1708.value << 16)
XL_BUS_ACTIVE_CAP_ETHERNET  = (XL_BUS_COMPATIBLE_ETHERNET.value << 16)

# defines for the supported hardware
XL_HWTYPE_NONE                         =  XLHwTypes(0)
XL_HWTYPE_VIRTUAL                      =  XLHwTypes(1)
XL_HWTYPE_CANCARDX                     =  XLHwTypes(2)
XL_HWTYPE_CANAC2PCI                    =  XLHwTypes(6)
XL_HWTYPE_CANCARDY                     = XLHwTypes(12)
XL_HWTYPE_CANCARDXL                    = XLHwTypes(15)
XL_HWTYPE_CANCASEXL                    = XLHwTypes(21)
XL_HWTYPE_CANCASEXL_LOG_OBSOLETE       = XLHwTypes(23)
XL_HWTYPE_CANBOARDXL                   = XLHwTypes(25) #// CANboardXL, CANboardXL PCIe 
XL_HWTYPE_CANBOARDXL_PXI               = XLHwTypes(27) # // CANboardXL pxi 
XL_HWTYPE_VN2600                       = XLHwTypes(29)
XL_HWTYPE_VN2610                       = XL_HWTYPE_VN2600
XL_HWTYPE_VN3300                       = XLHwTypes(37)
XL_HWTYPE_VN3600                       = XLHwTypes(39)
XL_HWTYPE_VN7600                       = XLHwTypes(41)
XL_HWTYPE_CANCARDXLE                   = XLHwTypes(43)
XL_HWTYPE_VN8900                       = XLHwTypes(45)
XL_HWTYPE_VN8950                       = XLHwTypes(47)
XL_HWTYPE_VN2640                       = XLHwTypes(53)
XL_HWTYPE_VN1610                       = XLHwTypes(55)
XL_HWTYPE_VN1630                       = XLHwTypes(57)
XL_HWTYPE_VN1640                       = XLHwTypes(59)
XL_HWTYPE_VN8970                       = XLHwTypes(61)
XL_HWTYPE_VN1611                       = XLHwTypes(63)
XL_HWTYPE_VN5610                       = XLHwTypes(65)
XL_HWTYPE_VN7570                       = XLHwTypes(67)
XL_HWTYPE_IPCLIENT                     = XLHwTypes(69)
XL_HWTYPE_IPSERVER                     = XLHwTypes(71)
XL_HWTYPE_VX1121                       = XLHwTypes(73)
XL_HWTYPE_VX1131                       = XLHwTypes(75)
XL_HWTYPE_VT6204                       = XLHwTypes(77)
                                       
XL_MAX_HWTYPE                          = XLHwTypes(81)


# interface version for our events
XL_INTERFACE_VERSION_V2                 = XLInterfaceVersion(2)                                                                             
XL_INTERFACE_VERSION_V3                 = XLInterfaceVersion(3) 
XL_INTERFACE_VERSION_V4                 = XLInterfaceVersion(4)           
#current version
XL_INTERFACE_VERSION                    = XL_INTERFACE_VERSION_V3 


