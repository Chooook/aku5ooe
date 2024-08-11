import json
import os
from string import Template

from cryptography.fernet import Fernet
import smbclient
from smbclient.shutil import open_file


class OOEContest:
    # TODO: добавить в init логин и передавать при вызове функций с mashup
    def __init__(self):
        """Класс для работы с голосованием по конкурсу"""
        self.smb_server = ...
        self.smb_user = ...
        self.smb_pass = ...
        self.smb_session = self.__create_smb_session()

        # self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.filename_template = Template('$login.enc')
        self.result_filename_template = Template(
            'results_$login.enc')
        self.output_path = r''
        self.alt_output_path = r''
        # key = Fernet.generate_key()
        # key_str = key.decode()  # Преобразуем ключ в строку
        self.key = '-bOZDhcq6g_24sRETJcsZ_LmLHfQ2hGJIM8jhJ37Mbw='.encode()
        self.fernet = Fernet(self.key)
        # Usage:
        # encrypted_message = self.fernet.encrypt(b"info")
        # decrypted_message = self.fernet.decrypt(encrypted_message)
        # b"info" == decrypted_message.decode()

        self.default_data = json.dumps(
            {"finished": False,
             "participants": {
                 "participant1": {"like": False, "dislike": False},
                 "participant2": {"like": False, "dislike": False},
                 "participant3": {"like": False, "dislike": False},
                 "participant4": {"like": False, "dislike": False},
                 "participant5": {"like": False, "dislike": False},
                 "participant6": {"like": False, "dislike": False},
                 "participant7": {"like": False, "dislike": False},
                 "participant8": {"like": False, "dislike": False},
                 "participant9": {"like": False, "dislike": False},
                 "participant10": {"like": False, "dislike": False},
                 "participant11": {"like": False, "dislike": False},
                 "participant12": {"like": False, "dislike": False},
                 "participant13": {"like": False, "dislike": False},
                 "participant14": {"like": False, "dislike": False},
                 "participant15": {"like": False, "dislike": False},
                 "participant16": {"like": False, "dislike": False},
                 "participant17": {"like": False, "dislike": False},
                 "participant18": {"like": False, "dislike": False},
                 "participant19": {"like": False, "dislike": False},
                 "participant20": {"like": False, "dislike": False},
                 "participant21": {"like": False, "dislike": False},
                 "participant22": {"like": False, "dislike": False},
                 "participant23": {"like": False, "dislike": False},
                 "participant24": {"like": False, "dislike": False},
                 "participant25": {"like": False, "dislike": False},
                 "participant26": {"like": False, "dislike": False},
                 "participant27": {"like": False, "dislike": False},
                 "participant28": {"like": False, "dislike": False},
                 "participant29": {"like": False, "dislike": False},
                 "participant30": {"like": False, "dislike": False}}},
            indent=2)
        self.default_data_encrypted = self.fernet.encrypt(
            self.default_data.encode())

    @staticmethod
    def showVersion():
        return 'OOEContest 2024-08-12 v0.4'

    def __create_smb_session(self):
        smb_client_session = smbclient.register_session(
            server=self.smb_server,
            username=self.smb_user,
            password=self.smb_pass)
        return smb_client_session

    def __get_paths(self, login: str, finish=False):
        if finish:
            filename = self.result_filename_template.substitute(login=login)
        else:
            filename = self.filename_template.substitute(login=login)
        path = os.path.join(self.output_path, filename)
        alt_path = os.path.join(self.alt_output_path, filename)
        return path, alt_path

    def __read_file(self, login: str):
        _, alt_path = self.__get_paths(login)
        if not smbclient.path.exists(alt_path):
            self.__create_login_files(login)
        with open_file(alt_path, 'rb') as f:
            decrypted = self.fernet.decrypt(f.read()).decode().lower()
            judge_data = json.loads(decrypted)
        return judge_data

    def __write_files(self, login: str, judge_data, finish=False):
        path, alt_path = self.__get_paths(login, finish)
        to_encrypt = json.dumps(judge_data, indent=2).encode()
        encrypted_data = self.fernet.encrypt(to_encrypt)
        with open_file(alt_path, 'wb') as f:
            f.write(encrypted_data)
        with open_file(path, 'wb') as f:
            f.write(encrypted_data)

    def __create_login_files(self, login: str):
        path, alt_path = self.__get_paths(login)

        with open_file(alt_path, 'wb') as f:
            f.write(self.default_data_encrypted)
        with open_file(path, 'wb') as f:
            f.write(self.default_data_encrypted)

    def get_judge_data(self, login: str = None):
        """Метод для получения данных о голосовании по логину судьи"""
        return json.dumps(self.__read_file(login))

    def update_votes(self, login: str, new_data: str):
        """Метод для обновления данных о голосовании по логину судьи"""
        # добавить переменную на фронте для проверки, завершено голосование
        # или нет, если да - обновление данных недоступно
        judge_data = self.__read_file(login)
        finished = judge_data['finished']
        votes = judge_data['participants']

        if finished:
            return json.dumps(judge_data)

        # на входе параметр new_data содержит id чекбокса
        new_data = list(filter(lambda x: x.isdigit(), new_data))

        if new_data.pop(-1) == '1':
            vote_type = 'like'
        else:
            vote_type = 'dislike'

        participant = f'participant{"".join(new_data)}'

        if vote_type == 'like':
            if votes[participant]['like'] is True:
                votes[participant]['like'] = False
            else:
                votes[participant]['like'] = True
                votes[participant]['dislike'] = False
        else:
            if votes[participant]['dislike'] is True:
                votes[participant]['dislike'] = False
            else:
                votes[participant]['like'] = False
                votes[participant]['dislike'] = True

        self.__write_files(login, judge_data)
        return json.dumps(judge_data)

    def finish_voting(self, login: str):
        """Метод для завершения голосования по логину судьи"""

        judge_data = self.__read_file(login)

        # для завершения голосования должно быть 15 голосов
        counter = 0
        for participant in judge_data['participants']:
            if judge_data['participants'][participant]['like'] is True:
                counter += 1
        if counter != 15:
            return json.dumps(judge_data)

        judge_data['finished'] = True
        self.__write_files(login, judge_data)

        participants = list(judge_data['participants'].keys())
        positive_votes = {login: [
            participant for participant in participants
            if judge_data['participants'][participant]['like'] is True
        ]}

        self.__write_files(login, positive_votes, finish=True)

        return json.dumps(judge_data)

    def renew_voting(self, login: str):
        """Метод для перезапуска голосования по логину судьи"""

        judge_data = self.__read_file(login)
        judge_data['finished'] = False
        self.__write_files(login, judge_data)
        return json.dumps(judge_data)
