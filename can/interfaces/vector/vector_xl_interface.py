# this interface is for windows only, otherwise use socketCAN

import logging

from can.interfaces.vector import *

logger = logging.getLogger('can.vectorXL')


from can.bus import BusABC
from can.message import Message


bootTimeEpoch = 0
try:
    import uptime
    import datetime

    bootTimeEpoch = (uptime.boottime() - datetime.datetime.utcfromtimestamp(0)).total_seconds()
except:
    bootTimeEpoch = 0

# Set up logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger('can.vectorXL')


# setup the string for the device
def set_string(deviceID, baudrate='250'):
    # config = deviceID + '; ' + baudrate
    config = "%s; %s" % (deviceID, baudrate)

    return (config)


# TODO: Issue 36 with data being zeros or anything other than 8 must be fixed
def message_convert_tx(msg):
    messagetx = XLevent()

    length = len(msg.data)
    messagetx.tagData.msg.dlc = c_ushort(length)

    messagetx.tag = XL_TRANSMIT_MSG
    messagetx.tagData.msg.id = c_uint32(XL_CAN_EXT_MSG_ID.value | msg.arbitration_id)

    for i in range(length):
        messagetx.tagData.msg.data[i] = c_uint8(msg.data[i])

    messagetx.tagData.msg.flags = c_ushort(0)
    if msg.is_error_frame:
        messagetx.tagData.msg.flags |= XL_CAN_MSG_FLAG_ERROR_FRAME.value

    if msg.is_remote_frame:
        messagetx.tagData.msg.flags |= XL_CAN_MSG_FLAG_REMOTE_FRAME.value

    # if msg.id_type:
    #     messagetx.tagData.msg.flags |= IS_ID_TYPE

    return messagetx


def message_convert_rx(messagerx):
    """convert the message from the CANAL type to pythoncan type"""
    ID_TYPE = bool(messagerx.tagData.msg.id & XL_CAN_EXT_MSG_ID.value)
    REMOTE_FRAME = bool(messagerx.tagData.msg.flags & XL_CAN_MSG_FLAG_REMOTE_FRAME.value)
    ERROR_FRAME = bool(messagerx.tagData.msg.flags & XL_CAN_MSG_FLAG_ERROR_FRAME.value)

    msgrx = Message(timestamp=messagerx.timeStamp,
                    is_remote_frame=REMOTE_FRAME,
                    extended_id=ID_TYPE,
                    is_error_frame=ERROR_FRAME,
                    arbitration_id=messagerx.tagData.msg.id & 0x7FFFFFFF,
                    dlc=messagerx.tagData.msg.dlc,
                    data=messagerx.tagData.msg.data[:messagerx.tagData.msg.dlc]
                    )

    return msgrx


# interface functions
class VectorXLBus(BusABC):
    def __init__(self, channel, *args, **kwargs):

        self.can = vectorXL()

        # enable_flags = c_ulong
        #
        # # set flags on the connection
        # if 'flags' in kwargs:
        #     enable_flags = kwargs["flags"]
        #
        # else:
        #     enable_flags = 0x00000008

        # # code to get the serial number of the device
        # if 'serial' in kwargs:
        #
        #     deviceID = kwargs["serial"]
        #
        # else:
        #     deviceID = serial()

        # set baudrate
        if 'baud' in kwargs:

            br = kwargs["baud"]

            # set custom baud rate (ex:500000 bitrate must be 500)
            # max rate is 1000 kbps
            baudrate = int(br) * 1000

        # set default value
        else:
            baudrate = 250 * 1000

        # connector = set_string(deviceID, baudrate)

        self.handle = self.can.Initialize()
        if not self.handle == -1:
            self.can.CANGoOnBus(self.handle, baudrate)

    def send(self, msg):

        tx = message_convert_tx(msg)
        self.can.Send(self.handle, tx)

    def recv(self, timeout=None):

        messagerx = XLevent()

        # if timeout is None:
        status = self.can.Receive(self.handle, byref(messagerx))

        # else:
        #     time = c_ulong
        #     time = timeout
        #     status = self.can.BlockingReceive(self.handle, byref(messagerx), time)

        if status is 0:
            rx = message_convert_rx(messagerx)
        else:
            logger.error('Canal Error %s', status)
            rx = None

        return rx

    def set_filters(self, can_filters=None):
        pass

    def flush_tx_buffer(self):
        self.can.xlCanFlushTransmitQueue(self.handle)

    def shutdown(self):
        """Shut down the device safely"""
        status = self.can.xlClosePort(self.handle)
