import json
import os

import smbclient
from smbclient.shutil import open_file
# from smbclient.shutil import copyfile as smbcf


class OOEContest:
    def __init__(self):
        """Класс для работы с голосованием по конкурсу"""
        self.smb_server = сервер
        self.smb_user = логин
        self.smb_pass = пароль
        self.smb_session = self.create_smb_session()

        self.json_filename = 'contest_info.json'
        self.smb_output_path = папка
        self.alt_smb_output_path = папка
        self.smb_json_path = os.path.join(
            self.smb_output_path, self.json_filename)
        self.alt_smb_json_path = os.path.join(
            self.alt_smb_output_path, self.json_filename)
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.current_dir, self.json_filename)

        self.logins = ['Логин',
                       'Логин',
                       'Логин',
                       'Логин',
                       'Логин',
                       'Логин',
                       'Логин',
                       'Логин',
                       'Логин']

    @staticmethod
    def showVersion():
        return 'OOEContest 2024-08-07 v0.3'

    def create_smb_session(self):
        smb_client_session = smbclient.register_session(
            server=self.smb_server,
            username=self.smb_user,
            password=self.smb_pass)
        return smb_client_session

    def get_judge_data(self, login: str = None):
        """Метод для получения данных о голосовании по логину судьи"""
        if login not in self.logins:
            return
        with open_file(self.alt_smb_json_path, 'r') as f:
            stored_data = json.load(f)[login]
        return json.dumps(stored_data)

    def update_votes(self, login: str, new_data: str):
        """Метод для обновления данных о голосовании по логину судьи"""
        # добавить переменную на фронте для проверки, завершено голосование
        # или нет, если да - обновление данных недоступно
        if login not in self.logins:
            return

        with open_file(self.alt_smb_json_path, 'r') as f:
            all_data = json.load(f)
        finished = all_data[login]['finished']
        stored_values = all_data[login]['participants']

        if finished:
            return self.get_judge_data(login)

        new_data = list(filter(lambda x: x.isdigit(), new_data))

        if new_data.pop(-1) == '1':
            vote_type = 'like'
        else:
            vote_type = 'dislike'

        participant = f'participant{"".join(new_data)}'

        if vote_type == 'like':
            stored_values[participant]['like'] = True
            stored_values[participant]['dislike'] = False
        else:
            stored_values[participant]['like'] = False
            stored_values[participant]['dislike'] = True

        to_change = all_data[login]['participants']
        to_change.update(stored_values)
        with open_file(self.alt_smb_json_path, 'w') as f:
            json.dump(all_data, f, indent=2)
        with open_file(self.smb_json_path, 'w') as f:
            json.dump(all_data, f, indent=2)
        # smbcf(self.alt_smb_json_path, self.smb_json_path)
        return self.get_judge_data(login)

    def finish_voting(self, login: str):
        """Метод для завершения голосования по логину судьи"""
        if login not in self.logins:
            return None

        with open_file(self.alt_smb_json_path, 'r') as f:
            all_data = json.load(f)

        # для завершения голосования должно быть 15 голосов
        counter = 0
        for participant in all_data[login]['participants']:
            if all_data[login]['participants'][participant]['like'] is True:
                counter += 1
        if counter != 15:
            return self.get_judge_data(login)

        all_data[login]['finished'] = True
        with open_file(self.alt_smb_json_path, 'w') as f:
            json.dump(all_data, f, indent=2)
        with open_file(self.smb_json_path, 'w') as f:
            json.dump(all_data, f, indent=2)
        # smbcf(self.alt_smb_json_path, self.smb_json_path)

        participants = list(all_data[login]['participants'].keys())
        positive_votes = {login: [
            participant for participant in participants
            if all_data[login]['participants'][participant]['like'] is True
        ]}
        alt_smb_judge_results_path = os.path.join(self.alt_smb_output_path,
                                                  f'{login}_results.json')
        smb_judge_results_path = os.path.join(self.smb_output_path,
                                              f'{login}_results.json')
        with open_file(alt_smb_judge_results_path, 'w') as f:
            json.dump(positive_votes, f, indent=2)
        with open_file(smb_judge_results_path, 'w') as f:
            json.dump(positive_votes, f, indent=2)
        # smbcf(alt_smb_judge_results_path, smb_judge_results_path)

        return self.get_judge_data(login)
