class SSH(object):

    def __init__(self, device_name, username, password, buffer="65535",
                 delay="1", port="22"):
        self.device_name = device_name
        self.username = username
        self.password = password
        self.buffer = buffer
        self.delay = delay
        self.port = int(port)

    def connect(self):
        import paramiko
        import time

        self.pre_conn = paramiko.SSHClient()
        self.pre_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.pre_conn.connect(self.device_name, username=self.username,
                              password=self.password, allow_agent=False,
                              look_for_keys=False, port=self.port)
        self.client_conn = self.pre_conn.invoke_shell()
        time.sleep(float(self.delay))
        return self.client_conn.recv(self.buffer)

    def close(self):
        return self.pre_conn.close()

    def clear_buffer(self):
        if self.client_conn.recv_ready():
            return self.client_conn.recv(self.buffer)
        else:
            return None

    def set_su(self, su_password):
        import re

        if re.search('>$', self.command('\n')):
            su = self.command('enable')
            if re.search('Password:', su):
                send_pwd = self.command(su_password)
                return send_pwd
        elif re.search('#$', self.command('\n')):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command='term len 0'):
        self.clear_buffer()
        return self.client_conn.sendall(command + "\n")

    def command(self, command):
        import time

        self.client_conn.sendall(command + "\n")
        not_done = True
        output = ""
        #self.clear_buffer()
        while not_done:
            time.sleep(float(self.delay))
            if self.client_conn.recv_ready():
                output += self.client_conn.recv(self.buffer)
            else:
                not_done = False
        return output


class Telnet(object):

    def __init__(self, device_name, username, password, delay="2", port="23"):
        self.device_name = device_name
        self.username = username
        self.password = password
        self.delay = float(delay)
        self.port = int(port)

    def connect(self):
        import telnetlib
        import sys

        self.access = telnetlib.Telnet(self.device_name, self.port)
        login_prompt = self.access.read_until("\(Username: \)|\(login: \)",
                                              self.delay)
        if 'login' in login_prompt:
            self.is_nexus = True
            self.access.write(self.username + '\n')
        elif 'Username' in login_prompt:
            self.is_nexus = False
            self.access.write(self.username + '\n')
        password_prompt = self.access.read_until('Password:',
                                                 self.delay)
        self.access.write(self.password + '\n')
        return self.access

    def close(self):
        return self.access.close()

    def clear_buffer(self):
        pass

    def set_enable(self, enable_password):
        import re

        if re.search('>$', self.command('\n')):
            self.access.write('enable\n')
            enable = self.access.read_until('Password')
            return self.access.write(enable_password + '\n')
        elif re.search('#$', self.command('\n')):
            return "Action: None. Already in enable mode."
        else:
            return "Error: Unable to determine user privilege status."

    def disable_paging(self, command='term len 0'):
        self.access.write(command + '\n')
        return self.access.read_until("\(#\)|\(>\)", self.delay)

    def command(self, command):
        self.access.write(command + '\n')
        return self.access.read_until("\(#\)|\(>\)", self.delay)


class SNMPv2(object):

    def __init__(self, device_name, snmp_community, symbol_name="sysDescr",
                 mib_index="0", mib_name="SNMPv2-MIB", snmp_version="2c",
                 snmp_port="161"):
        self.device_name = device_name
        self.snmp_community = snmp_community
        self.symbol_name = symbol_name
        self.mib_index = mib_index
        self.mib_name = mib_name
        self.snmp_version = snmp_version
        self.snmp_port = snmp_port

    def get(self):
        from pysnmp.entity.rfc3413.oneliner import cmdgen

        cmdGen = cmdgen.CommandGenerator()
        error_indication, error_status, error_index, data = cmdGen.getCmd(
            cmdgen.CommunityData(self.snmp_community),
            cmdgen.UdpTransportTarget((self.device_name, self.snmp_port)),
            cmdgen.MibVariable(self.mib_name, self.symbol_name,
                               self.mib_index),
            lookupNames=True, lookupValues=True)

        if error_indication:
            self.error_indication = error_indication
            return self.error_indication
        elif error_status:
            self.error_status = error_status
            return self.error_status
        else:
            self.data = data
            return self.data

    def extract(self):
            for name, value in self.data:
                return value.prettyPrint()
