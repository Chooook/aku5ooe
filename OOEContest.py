"""Модуль для сохранения результатов соревнования"""

import io
import json
import os
from string import Template

import pandas as pd
from cryptography.fernet import Fernet
import smbclient
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from http import HTTPStatus
from smbclient.shutil import open_file


class OOEContest:
    def __init__(self):
        """Класс для работы с голосованием по конкурсу"""
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.filename_template = Template('$login.enc')
        self.output_path = current_dir
        self.fir_output_path = r'alt'

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

        str_rsa_public = """
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
        self.__rsa_public = serialization.load_pem_public_key(
            str_rsa_public.encode(),
            backend=default_backend()
        )

    @staticmethod
    def showVersion():
        """Версия программы для AKU5"""
        return 'OOEContest 2024-08-12 v0.4'

    def save_data(self, login: str, data: str):
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
            data = json.loads(data)
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
            return HTTPStatus(200)
        except Exception:
            return HTTPStatus(400)

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

    def __read_data(self, login: str, str_rsa_private: str):
        """Метод для чтения данных о голосовании по логину"""
        filename = self.filename_template.substitute(login=login)
        path = os.path.join(self.output_path, filename)
        with open(path, 'rb') as f:
            data = f.read()
        data, fernet_len = data.split(b'*****')
        data, fernet_key_encrypted = data[:-256], data[-256:]
        str_rsa_private = str_rsa_private.replace(r'\n', '')
        private_rsa = serialization.load_pem_private_key(
            str_rsa_private.encode(),
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
        os.remove(path)
        return decrypted_data

    def save_results_to_excel(self, str_rsa_private: str):
        """Метод для сохранения результатов голосования в excel файл"""
        try:
            columns = (
                    ['Ранг']
                    + list(self.__judges_dict.values())
                    + ['Сумма голосов']
            )
            index = list(self.__participants_dict.values()) + ['Сумма голосов']
            result_df = pd.DataFrame(index=index, columns=columns)
            for login in self.__judges_dict.keys():
                judge_name = self.__judges_dict.get(login)
                try:
                    judge_data = self.__read_data(login, str_rsa_private)
                    judge_data = judge_data.split('\n')
                except Exception:
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
            return HTTPStatus(200)
        except Exception:
            return HTTPStatus(400)

    @staticmethod
    def __create_smb_session():
        """Метод для создания сессии протокола samba"""
        smb_server = 'server'
        smb_user = r'login'
        smb_pass = 'pass'
        return smbclient.register_session(
            server=smb_server,
            username=smb_user,
            password=smb_pass)
