import telnetlib
import logging
import re
import xml.dom.minidom

class Device:
    """
    proxy object for one device, use :update: for updating data and :__getitem__: for retrieving last updated data
    """
    _DEFAULT_TIMEOUT = 4
    _ENCODING = "utf8"
    PORT_DIGITAL_PREFIX = "DG"
    PORT_ANALOG_PREFIX = "AN"

    def __init__(self, login, password, url, port, timeout=_DEFAULT_TIMEOUT):
        self.url = url
        self.port = port
        self.timeout = timeout
        self.login = login
        self.password = password
        self.values = dict()
        self.update()

    @staticmethod
    def __to_bytes(raw_string):
        # return bytes(raw_string, Reader._ENCODING) # python 3.x
        # return bytes(raw_string) # python 3.x
        # s = codecs.decode(s.encode("UTF-8"), 'hex_codec')
        return raw_string

    def __getitem__(self, item):
        """
        :param item: name of the port :Device.PORT_DIGITAL_PREFIX:1..4 / :Device.PORT_ANALOG_PREFIX:1..4
        :return: value from port
        """
        return self.values[item]

    def update(self):
        """
        :return: update current device
        """
        telnet = None
        try:
            logging.debug("attempt to connect")
            telnet = telnetlib.Telnet(str(self.url), str(self.port), self.timeout)
            logging.debug("connected: %s" % telnet)
            telnet.read_until(Device.__to_bytes("login:"))
            # telnet.write(Reader.__to_bytes(self.admin+"\n\r"))
            telnet.write(Device.__to_bytes(str(self.login) + "\n\r"))
            logging.debug("waiting for password request")
            telnet.read_until(Device.__to_bytes("word:"))
            logging.debug("enter password:")
            telnet.write(Device.__to_bytes(str(self.password) + "\n\r"))

            telnet.read_until(Device.__to_bytes("\n\r: "))
            logging.debug("select menu information")
            telnet.write(Device.__to_bytes("i"))
            telnet.read_until(Device.__to_bytes("\n\r: "))
            logging.debug("select menu digital")
            telnet.write(Device.__to_bytes("f"))
            self.values = dict()
            digital_data = telnet.read_until(Device.__to_bytes("\n\r: "))
            digital_index = 0
            analog_index = 0
            for line in str(digital_data).split("\n\r"):
                if line.startswith("DG"):
                    digital_index += 1
                    self.values[Device.PORT_DIGITAL_PREFIX+str(digital_index)] = (re.sub("[^0-9]*", "", line)[1])
                if line.startswith("AN"):
                    analog_index += 1
                    start_index = line.index(":")
                    end_index = line.index("=", start_index)
                    self.values[Device.PORT_ANALOG_PREFIX+str(analog_index)] = line[start_index+1:end_index]
        except Exception as e:
            print("can't connect:" + e.message)
        finally:
            if telnet != None:
                try:
                    telnet.close()
                except Exception:
                    pass


class ConfigHolder(object):
    """
    configuration of all devices
    """
    TAG_DEVICE = "device"
    TAG_LOGIN = "login"
    TAG_PASSWORD = "password"
    TAG_URL = "url"
    TAG_PORT = "port"

    def __init__(self, file_name):
        xml_file = xml.dom.minidom.parse(file_name)
        xml_nodes = xml_file.getElementsByTagName(ConfigHolder.TAG_DEVICE)
        self.devices = []
        for each_node in xml_nodes:
            self.devices.append(DeviceSettings(each_node.getElementsByTagName(ConfigHolder.TAG_LOGIN)[0].childNodes[0].data,
                                               each_node.getElementsByTagName(ConfigHolder.TAG_PASSWORD)[0].childNodes[0].data,
                                               each_node.getElementsByTagName(ConfigHolder.TAG_URL)[0].childNodes[0].data,
                                               each_node.getElementsByTagName(ConfigHolder.TAG_PORT)[0].childNodes[0].data))
        self.index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.devices)

    def __getitem__(self, item):
        return self.devices[item]

    def next(self):
        if self.index >= len(self.devices):
            self.index = 0
            raise StopIteration
        return_value = self.devices[self.index]
        self.index += 1
        return return_value


class DeviceSettings:
    """
    settings for one device
    """
    def __init__(self, login, password, url, port):
        self.login = login
        self.password = password
        self.url = url
        self.port = port

    def __str__(self):
        return self.login+" "+self.password+" "+self.url+" "+self.port