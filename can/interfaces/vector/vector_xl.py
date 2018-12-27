# This wrapper is for windows or direct access via
# API.  Socket CAN is recommended under Unix/Linux systems

from ctypes import *
from struct import *
import logging
from can.interfaces.vectorXL_constants import *

# sys.path.append("C:\\Users\\Public\\Documents\\Vector XL Driver Library\\bin")
# clr.AddReference("vxlapi_NET")
# from vxlapi_NET import *

# import collections
logging.basicConfig(filename='vector.log', level=logging.DEBUG)
# type definitions

flags = c_ulong
pConfigureStr = c_char_p
handle = c_long(0)
timeout = c_ulong


# filter = c_ulong

# from CAN driver API for vxlapi.dll
# short - 16 bits
# int - 32 bits
# long - 32 bits
# char - 8 bits
class s_xl_can_msg(Structure):
    _pack_ = 1
    _fields_ = [('id', c_uint32),
                ('flags', c_uint16),
                ('dlc', c_uint16),
                ('res1', c_uint64),
                ('data', c_uint8 * 8),
                ('res2', c_uint64)]


class s_xl_chip_state(Structure):
    _pack_ = 1
    _fields_ = [('busStatus', c_uint8),
                ('txErrorCount', c_uint8),
                ('rxErrorCount', c_uint8)]


# class s_xl_lin_msg_api(Structure):
# 	_fields_=[('pulseCode', c_uint8),
# 			('time', c_uint64)]

class s_xl_sync_pulse(Structure):
    _pack_ = 1
    _fields_ = [('pulseCode', c_uint8),
                ('time', c_uint64)]


class s_xl_daio_data(Structure):
    _pack_ = 1
    _fields_ = [('flags', c_uint16),
                ('timestamp_correction', c_uint32),
                ('mask_digital', c_uint8),
                ('value_digital', c_uint8),
                ('mask_analog', c_uint8),
                ('reserved0', c_uint8),
                ('value_analog', c_uint16 * 4),
                ('pwm_frequency', c_uint32),
                ('pwm_value', c_uint16),
                ('reserved1', c_uint32),
                ('reserved2', c_uint32)]


class s_xl_transceiver(Structure):
    _pack_ = 1
    _fields_ = [('event_reason', c_uint8),
                ('is_present', c_uint8)]


class XL_IO_DIGITAL_DATA(Structure):
    _pack_ = 1
    _fields_ = [('digitalInputData', c_uint32)]


class XL_IO_ANALOG_DATA(Structure):
    _pack_ = 1
    _fields_ = [('measuredAnalogData0', c_uint32),
                ('measuredAnalogData1', c_uint32),
                ('measuredAnalogData2', c_uint32),
                ('measuredAnalogData3', c_uint32)]


class data(Union):
    _pack_ = 1
    _fields_ = [('digital', XL_IO_DIGITAL_DATA),
                ('analog', XL_IO_ANALOG_DATA)]


class s_xl_daio_piggy_data(Structure):
    _pack_ = 1
    _fields_ = [('daioEvtTag', c_uint32),
                ('triggerType', c_uint32),
                ('data', data)]


class s_xl_tag_data(Union):
    _fields_ = [('msg', s_xl_can_msg),
                ('chipState', s_xl_chip_state),
                # 				('linMsgApi', x_xl_lin_msg_api),
                ('syncPulse', s_xl_sync_pulse),
                ('daioData', s_xl_daio_data),
                ('transceiver', s_xl_transceiver),
                ('daioPiggyData', s_xl_daio_piggy_data)]


XLeventTag = c_uint8


# data type for the CAN Message
class XLevent(Structure):
    _pack_ = 1
    _fields_ = [('tag', XLeventTag),
                ('chanIndex', c_uint8),
                ('transId', c_uint16),
                ('portHandle', c_uint16),
                ('flags', c_uint8),
                ('reserved', c_uint8),
                ('timeStamp', c_uint64),
                ('tagData', s_xl_tag_data)]


msg = XLevent()


class can_struct(Structure):
    _pack_ = 1
    _fields_ = [('bitRate', c_uint32),
                ('sjw', c_uint8),
                ('tseg1', c_uint8),
                ('tseg2', c_uint8),
                ('sam', c_uint8),
                ('outputMode', c_uint8)]#,
                #('reserved', c_uint8 * 23)]

class most_struct(Structure):
    _pack_ = 1
    _fields_ = [('activeSpeedGrade', c_uint32),
                ('compatibleSpeedGrade', c_uint32),
                ('inicFwVersion', c_uint32)]

class flexray_struct(Structure):
    _pack_ = 1
    _fields_ = [('status', c_uint32),
                ('cfgMode', c_uint32),
                ('baudrate', c_uint32)]

class ethernet_struct(Structure):
    _pack_ = 1
    _fields_ = [('macAddr', c_uint8 * 6),
                ('connector', c_uint8),
                ('phy', c_uint8),
                ('link', c_uint8),
                ('speed', c_uint8),
                ('clockMode', c_uint8),
                ('bypass', c_uint8)]

class data_union(Union):
    _fields_ = [('can', can_struct),
                ('most', most_struct),
                ('flexray', flexray_struct),
                ('ehternet', ethernet_struct),
                ('raw', c_uint8 * 32)]

class XLbusParams(Structure):
    _pack_ = 1
    _fields_ = [('busType', c_uint32),
                ('data', data_union)]


class XLchannelConfig(Structure):
    _pack_ = 1
    _fields_ = [('name', c_char * (XL_MAX_LENGTH + 1)),
                ('hwType', c_uint8),
                ('hwIndex', c_uint8),
                ('hwChannel', c_ubyte),
                ('transceiverType', c_ushort),
                ('transceiverState', c_uint16),
                ('configError', c_uint16),
                ('channelIndex', c_uint8),
                ('channelMask', c_ulonglong),
                ('channelCapabilities', c_uint32),
                ('channelBusCapabilities', c_uint32),
                ('isOnBus', c_uint8),
                ('connectedBusType', c_uint32),
                ('busParams', XLbusParams),
                ('driverVersion', c_uint32),
                ('interfaceVersion', c_uint32),
                ('raw_data', c_uint32 * 10),
                ('serialNumber', c_uint32),
                ('articleNumber', c_uint32),
                ('transceiverName', c_char * (XL_MAX_LENGTH + 1)),
                ('specialCabFlags', c_uint32),
                ('dominantTimeout', c_uint32),
                ('dominantRecessiveDelay', c_uint8),
                ('recessiveDominantDelay', c_uint8),
                ('connectionInfo', c_uint8),
                ('currentlyAvailableTimestamps', c_uint8),
                ('minimalSupplyVoltage', c_uint16),
                ('maximalSupplyVoltage', c_uint16),
                ('maximalBaudRate', c_uint32),
                ('fpgaCoreCapabilities', c_uint8),
                ('specialDeviceStatus', c_uint8),
                ('channelBusActiveCapabilities', c_uint16),
                ('breakOffset', c_uint16),
                ('delimiterOffset', c_uint16),
                ('reserved', c_uint32 * 3)]


class XLdriverConfig(Structure):
    _pack_ = 1
    _fields_ = [('dllVersion', c_uint32),  # 0x300 means V3.0
                ('channelCount', c_uint32),
                ('reserved', c_uint32 * 10),
                ('channel', XLchannelConfig * XL_CONFIG_MAX_CHANNELS)]


permissionMask = XLaccess(-1)
m_xlChannelMask_both = XLaccess
size = c_uint32
# xldriverconfig = XLdriverConfig()

applicationName = "Python Vector XL"
b_applicationName = applicationName.encode('utf-8')
maxAppChannels = 1

class vectorXL:
    def __init__(self):
        self.__m_dllBasic = windll.LoadLibrary("vxlapi.dll")#dll_path)#

        if self.__m_dllBasic == None:
            logging.warning('DLL failed to load')
        self.channelMask = [0] * 1

    def Initialize(self):
        lxldriverconfig = XLdriverConfig()
        appChannel = 0
        chan1Found = 0
        hwType = c_uint16(-1)
        hwIndex = c_uint16(-1)
        hwChannel = c_uint16(-1)
        status = self.__m_dllBasic.xlOpenDriver()
        if status != XL_SUCCESS.value:
            return -1#status
        status = self.__m_dllBasic.xlGetDriverConfig(byref(lxldriverconfig))
        self.xldriverconfig = lxldriverconfig
        print(self.xldriverconfig.dllVersion)
        print(self.xldriverconfig.channelCount)
        for x in range(0, self.xldriverconfig.channelCount):
            print(self.xldriverconfig.channel[x].name)
            print("HW type:", self.xldriverconfig.channel[x].hwType)
            print("Driver version:", self.xldriverconfig.channel[x].driverVersion)
            print("Serial number:", self.xldriverconfig.channel[x].serialNumber)
            print("Can bitrate:", self.xldriverconfig.channel[x].busParams.data.can.bitRate)
            print("Can sjw:", self.xldriverconfig.channel[x].busParams.data.can.sjw)
            print("Can tseg1:", self.xldriverconfig.channel[x].busParams.data.can.tseg1)
            print("Can tseg2:", self.xldriverconfig.channel[x].busParams.data.can.tseg2)
            print("Can sam:", self.xldriverconfig.channel[x].busParams.data.can.sam)
            print("Can outputMode:", self.xldriverconfig.channel[x].busParams.data.can.outputMode)
        if status != XL_SUCCESS.value:
            return -1#status

        status = self.__m_dllBasic.xlGetApplConfig(c_char_p(b_applicationName), 0, byref(hwType), byref(hwIndex), byref(hwChannel), XL_BUS_TYPE_CAN)
        # Set the params into registry(default values...!)
        if status:
            for x in range(0,self.xldriverconfig.channelCount):
                if self.xldriverconfig.channel[x].channelBusCapabilities & XL_BUS_ACTIVE_CAP_CAN and appChannel < maxAppChannels:
                    hwType = self.xldriverconfig.channel[x].hwType
                    hwIndex = self.xldriverconfig.channel[x].hwIndex
                    hwChannel = self.xldriverconfig.channel[x].hwChannel

                    status = self.__m_dllBasic.xlSetApplConfig(c_char_p(b_applicationName),
                                                               appChannel,
                                                               hwType,
                                                               hwIndex,
                                                               hwChannel,
                                                               XL_BUS_TYPE_CAN)
                    if status:
                        return -1
                    self.channelMask[appChannel] = self.__m_dllBasic.xlGetChannelMask(hwType, hwIndex, hwChannel)
                    appChannel += 1
        else:
            self.channelMask[0] = self.__m_dllBasic.xlGetChannelMask(hwType, hwIndex, hwChannel)
            for x in range(0,self.xldriverconfig.channelCount):
                if self.xldriverconfig.channel[x].channelMask == self.channelMask[0] and self.xldriverconfig.channel[x].channelBusCapabilities & XL_BUS_ACTIVE_CAP_CAN:
                    chan1Found = 1
                    break

            if not chan1Found:
                return -1#XL_ERROR
            # get the second channel
            # status = self.__m_dllBasic.xlGetApplConfig(c_char_p(b_applicationName), 1, byref(hwType), byref(hwIndex), byref(hwChannel), XL_BUS_TYPE_CAN)
            # if status:
            #     return 0#status;
            # self.channelMask[1] = self.__m_dllBasic.xlGetChannelMask(hwType, hwIndex, hwChannel)
            # for x in range(0, xldriverconfig.channelCount):
            #     if xldriverconfig.channel[x].channelMask == self.channelMask[1] and xldriverconfig.channel[x].channelBusCapabilities & XL_BUS_ACTIVE_CAP_CAN:
            #         chan2Found = 1
            #         break
            #
            # if not chan2Found:
            #     return -1#XL_ERROR

        m_xlChannelMask_both = XLaccess(self.channelMask[0])
        permissionMask = XLaccess(m_xlChannelMask_both.value)
        status = self.__m_dllBasic.xlOpenPort(byref(handle), c_char_p(b_applicationName),
                                     m_xlChannelMask_both, byref(permissionMask),
                                     1024, XL_INTERFACE_VERSION, XL_BUS_TYPE_CAN)
        if status:
            handle.value = -1
        return handle

    def CANGoOnBus(self, handle, baudrate):
        m_xlChannelMask_both = XLaccess(self.channelMask[0])
        self.__m_dllBasic.xlCanSetChannelBitrate(handle, m_xlChannelMask_both, baudrate)
        self.__m_dllBasic.xlActivateChannel(handle, m_xlChannelMask_both, XL_BUS_TYPE_CAN, XL_ACTIVATE_RESET_CLOCK)

    def CANGoOffBus(self, handle):
        self.__m_dllBasic.xlDeactivateChannel(handle, m_xlChannelMask_both)

    def xlClosePort(self, handle):
        try:
            self.CANGoOffBus(handle, m_xlChannelMask_both)
            res = self.__m_dllBasic.xlClosePort(handle)
            self.__m_dllBasic.xlCloseDriver()
            return res
        except:
            logging.warning('Failed to close')
            raise

    def xlCanFlushTransmitQueue(self, handle):
        self.__m_dllBasic.xlCanFlushTransmitQueue(handle, m_xlChannelMask_both)

    def Send(self, handle, msg):
        try:
            size = c_uint(1)
            m_xlChannelMask_both = XLaccess(self.channelMask[0])
            return self.__m_dllBasic.xlCanTransmit(handle, XLaccess(self.channelMask[0]), byref(size), byref(msg))
        except:
            logging.warning('Sending error')
            raise

    def Receive(self, handle, msg):
        try:
            size = c_uint(1)
            return self.__m_dllBasic.xlReceive(handle, byref(size), msg)
        except:
            logging.warning('Receive error')
            raise

    def get_version(self):
        try:
            version = str((self.xldriverconfig.channel[self.channelMask[0]].driverVersion & 0xFF000000) >> 24) + '.' + str((self.xldriverconfig.channel[self.channelMask[0]].driverVersion & 0xFF0000) >> 16) + '.' + str(self.xldriverconfig.channel[self.channelMask[0]].driverVersion & 0xFFFF)
            return version
        except:
            logging.warning('Failed to get version info')
            raise

    def get_dll_version(self):
        try:
            version = str((self.xldriverconfig.dllVersion & 0xFF000000) >> 24) + '.' + str((self.xldriverconfig.dllVersion & 0xFFF000) >> 12) + '.' + str(self.xldriverconfig.dllVersion & 0xFFF)
            return version
        except:
            logging.warning('Failed to get DLL version')
            raise

    def get_vendor_string(self):
        try:
            return 'Vector'
        except:
            logging.warning('Failed to get vendor string')
            raise
