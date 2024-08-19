"""Модуль для сохранения результатов соревнования"""
import io
import os
from string import Template

import pandas as pd
import smbclient
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from smbclient.shutil import open_file
from smbprotocol.exceptions import SMBException
# from cryptography.exceptions import InvalidKey


DEBUG = False
if DEBUG:
    open_file = open  # noqa


class OOEContest:
    def __init__(self, str_rsa_public=''):
        """Класс для работы с голосованием по конкурсу"""
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_dir = current_dir
        self.fir_output_dir = r'alt'
        self.filename_template = Template('${login}_${suffix}.enc')

        self.__judges = {
            'login1': 'judge1name',
            'login2': 'judge2name',
            'login3': 'judge3name',
            'login4': 'judge4name',
            'login5': 'judge5name',
            'login6': 'judge6name',
            'login7': 'judge7name',
            'login8': 'judge8name',
        }
        self.__participants = {
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
        self.__default_str_rsa_private = """
-----BEGIN PRIVATE KEY-----
MIIEuwIBADALBgkqhkiG9w0BAQoEggSnMIIEowIBAAKCAQEAxiqzDR46KD52W5iY
Xz3zqVwmqj9ZKAvlE15oj5lcF5iww432Kq+QmZqujc7Vj5UzdzCcCExDHDn2UWO/
kEVUzoHNZaKxQweJrrscjz0zuS0P9hukHXMBD0Y2/rldGulDKFh7+ZsLjeNcxn92
lLN+p1uBFeTvjWkBBlQloBc3V7CAgv4khNXpVu0MkJSyfo4sqmJ2cFCzk6x+MMiT
eNVoEEAl7ICS24Wr7xQk5Kz2x6naalj/8dMa9uAFVnIITXdqud5yBRkeiXJ8BTKH
Y+iqv8W4SyvKCnbcmITcQhegRIxxPX57/7YFoxsZpJK32rB2EtNbOf8mSSs/X9/O
1FsJ9QIDAQABAoIBACcpEv8ZpRaE2XDaY+oWXQtv2Xg1UpIWX6uHMZSHEura0rui
Vy4ySZoBNlNxt0RLkMMSCROetnhif+mvk5CYEt1IS2W1U+BSIgQ0l706s/j5Dblt
1u2251O0ZXPK/7ostIfJjJ5T5GGit5fGYpGaMwIxk/3WovxH7troUBMl41rhfZ1D
xdCG7sZpPqXKEqsGn5pN8rNHrMJeYNdZkXQvmyAkLbLq8qNXqht+OomrgJrncFg4
aqHb7c1yGCXgcI914635nvNp13VWT/7fkh9kHvZL1of3xM3FjucH5ZORS9+pBe45
sDBo8AhkFtPo9rZtQ77h8sWwBm1fmN96LHsfmTUCgYEA/yaRb1Df0VBD1aRMH8mu
u1tkk3CWBLNfq7odTbSiyXEJ/7ahTko9AJHEwwuKFRETHJIPpc1Dz0s/H3eoICOE
NCkVXvFmyhetclLsjthjtdr3NGcTRKtoLyxTm9H8kAVDkjO2v9nZbCc5to86UqwL
I+BMmBe6Fl2DTNsEte+pJksCgYEAxtOSQ2E2aLokrUk2ejan7MsTsH1/gCB136dE
fS15f0vofRVsCT3XmCXlph/wsDWHyv8c/5DZ3Nmq3lHmJSBu7kz/xVBJNmUz2BP4
MES1tuCFcNHidphGbSEaK/1mwvrGYPr2b4yvqSwZYdF9bQqrrr4gLebQsVQVaTyq
oT0raL8CgYBKGo9+vwRiLGenMvKRAOhoreCGGdrYPqh4nbNJED9/Nf9rb0VmEZWq
BqwY4c8W00CzuZAl3XnmSLpqjzwbKXWKGKyGSKJL65iKbZ8a1aoP9Sp647zq4sV9
fehChzhNM9ouKirXiZPmH3ZZmTudKy6JGunj+nAncr1hovK5TIPaBQKBgFKn7/08
866T+91iO1iRUjw5rGTJt3CfjgE9e1aCyiimeO9PMYuh/vfMgW0PiDLo/hvg9MA2
CqwqfUNRTtkOY6+DqSzxFI6dgfEJVDtUxSpSqobdakUdRuHlSgkRnl/eewwkKMD0
/q3YnHCy826aagcKGTyb4RRnPUNzqge/80TnAoGBAKys+VchKPLAR9ylY/H6Vl6w
DA10e5H0ShmOdlrNkfSslNatPiJj5gcir0StVPlJuof7DXczBKgDY/h5wNiRkeHH
x3j5cNKgIsvl3bdG5iVw+jaCs6nUUip6dPYfH+hzS1AiRPUXw2+Fut+kiWZctPFs
V1uslhcFh+ZzIqSM8vi/
-----END PRIVATE KEY-----
"""

        self.__str_rsa_public = str_rsa_public
        if not self.__str_rsa_public:
            self.__str_rsa_public = self.__default_str_rsa_public

        try:
            self.__rsa_public = serialization.load_pem_public_key(
                self.__str_rsa_public.encode(),
                backend=default_backend()
            )
        except ValueError as e:
            # logging.error(f'Not valid public key: {e}')
            raise ValueError(f'Not valid public key: {e}')
        except Exception as e:
            # logging.error(f'Error while loading public key: {e}')
            raise ValueError(f'Error while loading public key: {e}')

    @staticmethod
    def check_return(param):
        return str(param)

    @staticmethod
    def showVersion():  # noqa
        """Версия программы для AKU5"""
        return 'OOEContest 2024-08-16 v0.10'

    def save_data(self, login: str, data: list):
        """Метод для сохранения данных о голосовании по логину судьи"""
        try:
            participants = [
                f'participant{self.__get_participant_num(checkbox)}'
                for checkbox in data
            ]
            votes = '\n'.join(participants)
        except Exception as e:
            # logging.error(f'Error while parsing data: {e}')
            raise Exception(f'Error while parsing data: {e}')

        fernet, encrypted_fernet_key = self.__get_fernet()
        encrypted_votes = fernet.encrypt(votes.encode())
        encrypted_votes_and_key = (
                encrypted_votes
                + encrypted_fernet_key
                + f'*****{str(len(encrypted_fernet_key))}'.encode()
        )

        output_path = self.__generate_unique_filename(login)
        try:
            with open(output_path, 'wb') as f:
                f.write(encrypted_votes_and_key)
                # logging
        except Exception as e:
            # logging
            raise Exception(f'Error while saving data: {e}')
        if self.__default_str_rsa_public == self.__str_rsa_public:
            # logging
            return '300'
        # logging
        return '200'

    def __get_fernet(self):
        """
        Метод для получения объекта Fernet для симметричного шифрования
        и зашифрованного ключа этого объекта
        """
        fernet_key = Fernet.generate_key()
        fernet = Fernet(fernet_key)
        encrypted_fernet_key = self.__rsa_public.encrypt(
            fernet_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return fernet, encrypted_fernet_key

    @staticmethod
    def __get_participant_num(checkbox: str):
        """Метод для получения номера участника из чек-бокса"""
        # В переменной data должен быть список чек-боксов с like
        #  т.к. чек-бокс выглядит так: checkbox34_1, нужно извлечь номера
        #  участников для сохранения итога
        #  data = ["checkbox34_1", "checkbox32_1", "checkbox31_1",...]
        checkbox = checkbox.split('_')[0]
        number = ''.join(list(filter(lambda x: x.isdigit(), checkbox)))
        return number

    def __generate_unique_filename(self, login):
        """Метод для генерации нового имени файла"""
        suffix = 1
        filename = self.filename_template.substitute(
            login=login, suffix=suffix)
        output_path = os.path.join(self.output_dir, filename)

        while os.path.exists(output_path):
            suffix += 1
            filename = self.filename_template.substitute(
                login=login, suffix=suffix)
            output_path = os.path.join(self.output_dir, filename)

        return output_path

    def save_results_to_excel(
            self, str_rsa_private: str = '', judges: dict = None, rnd=''):
        """Метод для сохранения результатов голосования в excel файл"""
        # judges = '{"login1": "judge1name", "login2": "judge2name",...}'
        # logging.info(f'Called save_results_to_excel({judges}, {rnd})')
        rsa_private_filepath = str_rsa_private  # TODO переименовать переменную
        if not rsa_private_filepath:
            bytes_rsa_private = self.__default_str_rsa_private.encode()
        else:
            bytes_rsa_private = self.__get_rsa_from_file(rsa_private_filepath)
        private_rsa = self.__get_rsa_from_value(bytes_rsa_private)

        if not judges or not isinstance(judges, dict):
            # logging.info(f'Using default judges')
            # print(f'Using default judges')
            judges = self.__judges

        all_data = {}
        for login, judge_name in judges.items():
            all_data[judge_name] = self.__read_data(login, private_rsa)

        result_output_path = os.path.join(
            self.fir_output_dir, 'results.xlsx')
        byte_stream = io.BytesIO()
        self.__build_results_dataframe(all_data).to_excel(byte_stream)
        byte_stream.seek(0)
        session = self.__create_smb_session()
        try:
            # with open(result_output_path, 'wb') as f:
            with open_file(result_output_path, 'wb') as f:
                f.write(byte_stream.read())
        except Exception as e:
            # logging.error(f'Error while saving results: {e}')
            return f'Error while saving results: {e}'
        finally:
            if session:
                session.disconnect()
            byte_stream.close()
            smbclient.reset_connection_cache()

        if bytes_rsa_private == self.__default_str_rsa_private.encode():
            # logging
            return '300'
        # logging
        return '200'

    def __get_rsa_from_file(self, rsa_filepath: str):
        """Метод для получения ключа rsa из файла"""
        session = self.__create_smb_session()
        try:
            with open_file(rsa_filepath, 'rb') as f:
                bytes_rsa_private = f.read()
            return bytes_rsa_private
        except Exception as e:
            # logging.error(f'Error while reading rsa-key from file: {e}')
            raise(SMBException(f'Error while reading rsa-key from file: {e}'))
        finally:
            if session:
                session.disconnect()

    @staticmethod
    def __create_smb_session():
        """Метод для создания сессии протокола samba"""
        smb_server = 'server'
        smb_user = r'login'
        smb_pass = 'pass'
        try:
            session = smbclient.register_session(
                server=smb_server,
                username=smb_user,
                password=smb_pass)
            return session
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def __get_rsa_from_value(bytes_rsa_private: bytes):
        try:
            private_rsa = serialization.load_pem_private_key(
                bytes_rsa_private,
                password=None,
                backend=default_backend()
            )
            return private_rsa
        except ValueError as e:
            # logging.error(f'Not valid public key: {e}')
            raise ValueError(f'Not valid private key: {e}')
        except Exception as e:
            # logging.error(f'Error while loading public key: {e}')
            raise ValueError(f'Error while loading private key: {e}')

    def __read_data(self, login: str, private_rsa):
        """Метод для чтения данных о голосовании по логину"""
        judge_data = {}

        for filename, filepath in self.__find_judge_files(login).items():
            # try:
            with open(filepath, 'rb') as f:
                data = f.read()
            data = data.split(b'*****')[0]
            votes, fernet_key_encrypted = data[:-256], data[-256:]
            fernet_key = private_rsa.decrypt(
                fernet_key_encrypted,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            fernet = Fernet(fernet_key)
            decrypted_data = fernet.decrypt(votes).decode().split('\n')
            judge_data[filename] = decrypted_data
            # except Exception as e:
                # logging.error(f'Error while reading data: {e}')
                # print(e)
                # continue
        return judge_data

    def __find_judge_files(self, login):
        """Метод для поиска файлов с данным логином"""
        matching_files = {}

        for _, _, files in os.walk(self.output_dir):
            for file in files:
                if file.startswith(login) and file.endswith('.enc'):
                    file_num = file.split('_')[-1]
                    file_num = ''.join(
                        list(filter(lambda x: x.isdigit(), file_num)))
                    filepath = os.path.join(self.output_dir, file)
                    matching_files[file_num] = filepath

        return matching_files

    def __build_results_dataframe(self, all_data):
        # Если писать все данные из всех файлов, то какие оценки учитывать,
        #  а какие нет, если по каждому судье будет несколько файлов
        index = list(self.__participants.values()) + ['Сумма голосов']
        judges_list = []
        for judge_name, judge_data in all_data.items():
            for file_num in judge_data.keys():
                judges_list.append(f'{judge_name}_{file_num}')
        columns = (['Ранг'] + judges_list + ['Сумма голосов'])
        result_df = pd.DataFrame(index=index, columns=columns)

        for judge_name, judge_data in all_data.items():
            for file_num, data in judge_data.items():
                judge_col = f'{judge_name}_{file_num}'
                for participant in data:
                    participant_name = self.__participants.get(participant)
                    result_df.loc[participant_name, judge_col] = 1
                result_df.loc['Сумма голосов', judge_col] = result_df[
                    judge_col].sum()
        result_df['Сумма голосов'] = result_df.sum(axis=1)
        return result_df
