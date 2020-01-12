import os
import sqlite3
import keyring
from _hashlib import pbkdf2_hmac
from Crypto.Cipher import AES


class Chrome:
    browser = "Chrome"
    config = {
        'my_pass': keyring.get_password(
            '{} Safe Storage'.format(browser),
            browser),
        'iterations': 1003,
        'cookie_file': os.environ['HOME']+'/library/application support/google/chrome/Default/Cookies',
        'init_vector': b' ' * 16,
        'length': 16,
        'salt': b'saltysalt',
    }

    enc_key = pbkdf2_hmac(hash_name='sha1',
                          password=config['my_pass'].encode('utf8'),
                          salt=config['salt'],
                          iterations=config['iterations'],
                          dklen=config['length'])

    def cookie(self, host):
        cookies = dict()
        sql = f"select name,encrypted_value from cookies where host_key like '{host}';"
        with sqlite3.connect(self.config['cookie_file']) as conn:
            res = conn.execute(sql)
            l = res.fetchall()
            for i in l:
                key, enc_value = i
                cookies[key] = self.decrypt(enc_value)
        return cookies

    def decrypt(self, enc_value):
        # v10
        encrypted_value = enc_value[3:]

        cipher = AES.new(
            self.enc_key,
            AES.MODE_CBC,
            IV=self.config['init_vector'])
        decrypted = cipher.decrypt(encrypted_value)

        last = decrypted[-1]
        if isinstance(last, int):
            return decrypted[:-last].decode('utf8')
        return decrypted[:-ord(last)].decode('utf8')
