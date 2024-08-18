"""Модуль для сохранения результатов соревнования"""
import io
import os
from string import Template

import pandas as pd
from cryptography.fernet import Fernet
import smbclient
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from smbclient.shutil import open_file


class OOEContest:
    def __init__(self, str_rsa_public=""):
        """Класс для работы с голосованием по конкурсу"""
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_path = current_dir
        self.fir_output_path = r'alt'
        self.filename_template = Template('$login.enc')

        self.__judges_dict = {
            'login1': 'judge1name',
            'login2': 'judge2name',
            'login3': 'judge3name',
            'login4': 'judge4name',
            'login5': 'judge5name',
            'login6': 'judge6name',
            'login7': 'judge7name',
            'login8': 'judge8name',
        }
        self.__participants_dict = {
            'participant1': 'partname1',
            'participant2': 'partname2',
            'participant3': 'partname3',
            'participant4': 'partname4',
            'participant5': 'partname5',
            'participant6': 'partname6',
            'participant7': 'partname7',
            'participant8': 'partname8',
            'participant9': 'partname9',
            'participant10': 'partname10',
            'participant11': 'partname11',
            'participant12': 'partname12',
            'participant13': 'partname13',
            'participant14': 'partname14',
            'participant15': 'partname15',
            'participant16': 'partname16',
            'participant17': 'partname17',
            'participant18': 'partname18',
            'participant19': 'partname19',
            'participant20': 'partname20',
            'participant21': 'partname21',
            'participant22': 'partname22',
            'participant23': 'partname23',
            'participant24': 'partname24',
            'participant25': 'partname25',
            'participant26': 'partname26',
            'participant27': 'partname27',
            'participant28': 'partname28',
            'participant29': 'partname29',
            'participant30': 'partname30',
        }

        self.__str_rsa_public = str_rsa_public
        self.__default_str_rsa_public = """
-----BEGIN PUBLIC KEY-----
MIIBIDALBgkqhkiG9w0BAQoDggEPADCCAQoCggEBAMYqsw0eOig+dluYmF8986lc
Jqo/WSgL5RNeaI+ZXBeYsMON9iqvkJmaro3O1Y+VM3cwnAhMQxw59lFjv5BFVM6B
zWWisUMHia67HI89M7ktD/YbpB1zAQ9GNv65XRrpQyhYe/mbC43jXMZ/dpSzfqdb
gRXk741pAQZUJaAXN1ewgIL+JITV6VbtDJCUsn6OLKpidnBQs5OsfjDIk3jVaBBA
JeyAktuFq+8UJOSs9sep2mpY//HTGvbgBVZyCE13arnecgUZHolyfAUyh2Poqr/F
uEsrygp23JiE3EIXoESMcT1+e/+2BaMbGaSSt9qwdhLTWzn/JkkrP1/fztRbCfUC
AwEAAQ==
-----END PUBLIC KEY-----
"""
        if not self.__str_rsa_public:
            self.__str_rsa_public = self.__default_str_rsa_public
        self.__rsa_public = serialization.load_pem_public_key(
            self.__str_rsa_public.encode(),
            backend=default_backend()
        )
        self.__default_str_rsa_private = """
-----BEGIN PRIVATE KEY-----
MIIEuwIBADALBgkqhkiG9w0BAQoEggSnMIIEowIBAAKCAQEAyb2TG9kMmsXpRyEw
sTeaxng/rr/uZIzaDQXu9U6TuEQkLKEwRlkX5LxUqrAI9vxPAMi+YQu1fVDwJakw
TMPIZlOLXjpSvJp7CIg1y7BSGM19YZP6cxhgXPQcvAjaJcDndBNXpG1SJ8sdDGv4
NVfqs75BOxhaqMzLYO0DgzAOeCDh44ihcsCrz4tl5sBE5peLk4VCdGapWjdVZ5Pb
h1h+sNgOavomHxqZbgo5yGIp2tFdWaDYdtYHNiCocihBXGSR5hBgAAJcyiPDTT0a
fUo5/D/y8CPvk6z5vctqaRXAmkCzYlBNAn7fI8V21+t/i8V9qIO5Y4zkkidfOYS6
Y2pFcwIDAQABAoIBADk8XTvF4TMaGlyRWJC232UWoa6xCnAhnA2c1NZpBDT/tCmr
U5hp14MQQY8poWl9XOayjXzYBxY2O+Pbc/Ybh8QsSLqjnmyfAXACwQx4ilo6Fqv0
AVbdIB3PLkXU1xtl9uSyRifC0k+y6xtmmIV923tCa5xaBQKmE798jwYNwNUosWby
3XZ6/fHo7ngpQJJlzCUP4sTNuejMuQgRHVCTt8/ZncuzMZ3ruLkNi7WqHkdZ8VnN
c9LXL6whkJAohz73i3+gipIyE8/+Zc05yNOJyNgDLMnnVa/TtJ8ls9wp/XTlt1H8
HxnhWNJRWw0wxbf+Di1n7XEibbCXAawnplIFxDECgYEA/VktYOOgLT+zKfO80Nsf
iTXdO8OAqiR2LpEisE96V+nykn8FJEmBaXVmPdGO/qPf2o36VLMCin56Dv9VW9Uj
WjcdEwk8EPDBMjunux02U/QPsKStaqAnJXZpEVQdnD36cDuz5bLxL2AOrmVt5s78
cHG9auv2lZ/eE59u/PBiVhECgYEAy9oegEDOjbxhORrXjM4Qbhq29ct1G6spVN4p
/tcsQqLU212igOEcYhH06RB4emVxT9tCbLZ9zqJVkhDQMUR+0TCuY0dvEUHj2nct
oMio673hiOr+dz/nVG3LCqqqrF1jJujMl1ynmHysnCy+Od7bpnLBLEzkwWNM4Nq6
tGa2z0MCgYEA9+24adP4oa9v3wNG6UE3GGjdCypklJzABwxDXTU6LiSlHVYuqvdA
LPsVxjN485tdax18OD1CpFPnkRuw5gCr6xJ6YnGsFYv2FPmqSIPq8berTxupFeqK
xK+fXLTrkUZZ+lGC2KwIOWuQknxyU+iFxGiajLNEieJ8SsnArMl2AnECgYByG7WJ
Gz3EDxfpDEJuOgbuaxvROMNj6oqnS/j8AtxurJEz/hTxyZDGwMB0GdkmwlQMXHKx
QfHoUexOaATyHyJR3MsxHZJpeZWe+6lZ4BjWZSKzLr+kZuwJ0a+fV+tTsq7G3/du
HtpdvCQvA8izwjD32jKRprVCH2CwWR+7zec02wKBgG02iVAexKguHjaQDe1IPwb1
P5SaHr3UzmoeRUWOY7SQl5OiAkvt/FIknbcQ7FHmeN24G5IvDS4tH391L5QSdKcc
Ma/5UHTIkjxUsTJWGwDU/blHLaAXLoOGMWmaQNXY0UiPvtdV1UJeILFURi5G59B1
lx8fAoXVy9Dac4OTr4Hy
-----END PRIVATE KEY-----
"""

    @staticmethod
    def check_return(param):
        return str(param)

    @staticmethod
    def showVersion():
        """Версия программы для AKU5"""
        return 'OOEContest 2024-08-16 v0.10'

    def save_data(self, login: str, data: list):
        """Метод для сохранения данных о голосовании по логину судьи"""

        # В переменной data должен быть логин и список чек-боксов с like
        #  т.к. чек-бокс выглядит так: checkbox34_1, нужно извлечь номера
        #  участников для правильного сохранения итога
        # data = '["checkbox34_1", "checkbox32_1", "checkbox31_1",...]'
        def get_participant(checkbox: str):
            checkbox = checkbox.split('_')[0]
            number = ''.join(list(filter(lambda x: x.isdigit(), checkbox)))
            return number

        try:
            fernet, fernet_key_encrypted = self.__get_fernet_key()
            participants = [
                f'participant{get_participant(checkbox)}' for checkbox in data
            ]
            to_write = '\n'.join(participants)  # like csv, header in filename
            encrypted = fernet.encrypt(to_write.encode())
            encrypted_with_key = (
                    encrypted
                    + fernet_key_encrypted
                    + f'*****{str(len(fernet_key_encrypted))}'.encode()
            )
            filename = self.filename_template.substitute(login=login)
            path = os.path.join(self.output_path, filename)
            with open(path, 'wb') as f:
                f.write(encrypted_with_key)
            if self.__default_str_rsa_public == self.__str_rsa_public:
                return '300'
            return '200'
        except Exception as e:
            return str(e)

    def __get_fernet_key(self):
        """Метод для получения симметричного ключа для шифрования"""
        fernet_key = Fernet.generate_key()
        fernet = Fernet(fernet_key)
        fernet_key_encrypted = self.__rsa_public.encrypt(
            fernet_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return fernet, fernet_key_encrypted

    def __read_data(self, login: str, str_rsa_private: bytes):
        """Метод для чтения данных о голосовании по логину"""
        filename = self.filename_template.substitute(login=login)
        path = os.path.join(self.output_path, filename)
        with open(path, 'rb') as f:
            data = f.read()
        data, fernet_len = data.split(b'*****')
        data, fernet_key_encrypted = data[:-256], data[-256:]
        private_rsa = serialization.load_pem_private_key(
            str_rsa_private,
            password=None,
            backend=default_backend()
        )
        fernet_key = private_rsa.decrypt(
            fernet_key_encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        fernet = Fernet(fernet_key)
        decrypted_data = fernet.decrypt(data).decode()
        # os.remove(path)
        return decrypted_data

    def save_results_to_excel(
            self, str_rsa_private: str = "", judges: dict = None):
        """Метод для сохранения результатов голосования в excel файл"""
        # judges = '{"login1": "judge1name", "login2": "judge2name",...}'
        return_code = '200'
        if not str_rsa_private:
            str_rsa_private = self.__default_str_rsa_private.encode()
            return_code = '300'
        else:
            session = self.__create_smb_session()
            with open_file(str_rsa_private, 'rb') as f:
                str_rsa_private = f.read()
            session.disconnect()
        try:
            if not judges:
                judges = self.__judges_dict
            columns = (
                    ['Ранг']
                    + list(judges.values())
                    + ['Сумма голосов']
            )
            index = list(self.__participants_dict.values()) + ['Сумма голосов']
            result_df = pd.DataFrame(index=index, columns=columns)
            for login in judges:
                judge_name = judges.get(login)
                try:
                    judge_data = self.__read_data(login, str_rsa_private)
                    judge_data = judge_data.split('\n')
                except Exception as e:
                    print(e)
                    continue
                for participant in judge_data:
                    participant_name = self.__participants_dict.get(participant)
                    result_df.loc[participant_name, judge_name] = 1
                result_df.loc['Сумма голосов', judge_name] = result_df[
                    judge_name].sum()
            result_df['Сумма голосов'] = result_df.sum(axis=1)

            result_output_path = os.path.join(
                self.fir_output_path, 'results.xlsx')
            byte_stream = io.BytesIO()
            result_df.to_excel(byte_stream)
            byte_stream.seek(0)
            session = self.__create_smb_session()
            # with open(result_output_path, 'wb') as f:
            with open_file(result_output_path, 'wb') as f:
                f.write(byte_stream.read())
            session.disconnect()
            byte_stream.close()
            smbclient.reset_connection_cache()
            return return_code
        except Exception as e:
            return str(e)

    @staticmethod
    def __create_smb_session():
        """Метод для создания сессии протокола samba"""
        smb_server = 'server'
        smb_user = r'login'
        smb_pass = 'pass'
        session = smbclient.register_session(
            server=smb_server,
            username=smb_user,
            password=smb_pass)
        return session
