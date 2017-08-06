import telnetlib
import logging
import re


class Reader:
    _DEFAULT_TIMEOUT = 4
    _ENCODING = "utf8"

    def __init__(self, login, password, url, port, timeout=_DEFAULT_TIMEOUT):
        self.url = url
        self.port = port
        self.timeout = timeout
        self.login = login
        self.password = password
        self.values = []
        self.update()

    @staticmethod
    def __to_bytes(raw_string):
        # return bytes(raw_string, Reader._ENCODING) # python 3.x
        # return bytes(raw_string) # python 3.x
        # s = codecs.decode(s.encode("UTF-8"), 'hex_codec')
        return raw_string

    def value(self, index):
        """
        :param index: number of output 1..5
        :return: value: 0 or 1
        """
        return self.values[index-1]

    def update(self):
        """
        :return: update current value
        """
        telnet = None
        try:
            logging.debug("attempt to connect")
            telnet = telnetlib.Telnet(self.url, self.port, self.timeout)
            logging.debug("connected: %s" % telnet)
            telnet.read_until(Reader.__to_bytes("login:"))
            # telnet.write(Reader.__to_bytes(self.admin+"\n\r"))
            telnet.write(Reader.__to_bytes(self.login+"\n\r"))
            logging.debug("waiting for password request")
            telnet.read_until(Reader.__to_bytes("word:"))
            logging.debug("enter password:")
            telnet.write(Reader.__to_bytes(self.password+"\n\r"))
            telnet.read_until(Reader.__to_bytes("\n\r: "))
            logging.debug("select menu information")
            telnet.write(Reader.__to_bytes("i"))
            telnet.read_until(Reader.__to_bytes("\n\r: "))
            logging.debug("select menu digital")
            telnet.write(Reader.__to_bytes("d"))
            self.values = []
            digital_data = telnet.read_until(Reader.__to_bytes("\n\r: "))
            for line in str(digital_data).split("\n\r"):
                if line.startswith("DG"):
                    self.values.append(re.sub("[^0-9]*", "", line)[1])
        except Exception as e:
            print("can't connect:"+e.message)
        finally:
            if telnet != None:
                try:
                    telnet.close()
                except Exception:
                    pass
