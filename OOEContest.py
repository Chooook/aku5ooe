import json
import os
from string import Template

import smbclient
from smbclient.shutil import open_file


class OOEContest:
    def __init__(self):
        """Класс для работы с голосованием по конкурсу"""
        self.smb_server = ...
        self.smb_user = ...
        self.smb_pass = ...
        self.smb_session = self.create_smb_session()

        self.json_filename_template = Template('$login.json')
        self.finished_json_filename_template = Template(
            'results_$login.json')
        self.output_path = '.'
        self.alt_output_path = './alt'
        # self.current_dir = os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def showVersion():
        return 'OOEContest 2024-08-07 v0.3'

    def create_smb_session(self):
        smb_client_session = smbclient.register_session(
            server=self.smb_server,
            username=self.smb_user,
            password=self.smb_pass)
        return smb_client_session

    def get_paths(self, login: str):
        path = os.path.join(self.output_path,
                            self.json_filename_template.substitute(
                                login=login))
        alt_path = os.path.join(self.alt_output_path,
                                self.json_filename_template.substitute(
                                    login=login))
        return path, alt_path

    def create_login_files(self, login: str):
        path, alt_path = self.get_paths(login)
        default_data = {"finished": False,
                        "participants": {
                            "participant1": {
                                "like": False,
                                "dislike": False
                            },
                            "participant2": {
                                "like": False,
                                "dislike": False
                            },
                            "participant3": {
                                "like": False,
                                "dislike": False
                            },
                            "participant4": {
                                "like": False,
                                "dislike": False
                            },
                            "participant5": {
                                "like": False,
                                "dislike": False
                            },
                            "participant6": {
                                "like": False,
                                "dislike": False
                            },
                            "participant7": {
                                "like": False,
                                "dislike": False
                            },
                            "participant8": {
                                "like": False,
                                "dislike": False
                            },
                            "participant9": {
                                "like": False,
                                "dislike": False
                            },
                            "participant10": {
                                "like": False,
                                "dislike": False
                            },
                            "participant11": {
                                "like": False,
                                "dislike": False
                            },
                            "participant12": {
                                "like": False,
                                "dislike": False
                            },
                            "participant13": {
                                "like": False,
                                "dislike": False
                            },
                            "participant14": {
                                "like": False,
                                "dislike": False
                            },
                            "participant15": {
                                "like": False,
                                "dislike": False
                            },
                            "participant16": {
                                "like": False,
                                "dislike": False
                            },
                            "participant17": {
                                "like": False,
                                "dislike": False
                            },
                            "participant18": {
                                "like": False,
                                "dislike": False
                            },
                            "participant19": {
                                "like": False,
                                "dislike": False
                            },
                            "participant20": {
                                "like": False,
                                "dislike": False
                            },
                            "participant21": {
                                "like": False,
                                "dislike": False
                            },
                            "participant22": {
                                "like": False,
                                "dislike": False
                            },
                            "participant23": {
                                "like": False,
                                "dislike": False
                            },
                            "participant24": {
                                "like": False,
                                "dislike": False
                            },
                            "participant25": {
                                "like": False,
                                "dislike": False
                            },
                            "participant26": {
                                "like": False,
                                "dislike": False
                            },
                            "participant27": {
                                "like": False,
                                "dislike": False
                            },
                            "participant28": {
                                "like": False,
                                "dislike": False
                            },
                            "participant29": {
                                "like": False,
                                "dislike": False
                            },
                            "participant30": {
                                "like": False,
                                "dislike": False
                            }}}

        with open_file(alt_path, 'w') as f:
            json.dump(default_data, f, indent=2)
        with open_file(path, 'w') as f:
            json.dump(default_data, f, indent=2)

    def get_judge_data(self, login: str = None):
        """Метод для получения данных о голосовании по логину судьи"""
        _, alt_path = self.get_paths(login)
        if not smbclient.path.exists(alt_path):
            self.create_login_files(login)
        with open_file(alt_path, 'r') as f:
            judge_data = json.load(f)

        return json.dumps(judge_data)

    def update_votes(self, login: str, new_data: str):
        """Метод для обновления данных о голосовании по логину судьи"""
        # добавить переменную на фронте для проверки, завершено голосование
        # или нет, если да - обновление данных недоступно
        path, alt_path = self.get_paths(login)
        if not smbclient.path.exists(alt_path):
            self.create_login_files(login)

        with open_file(alt_path, 'r') as f:
            judge_data = json.load(f)
        finished = judge_data['finished']
        stored_values = judge_data['participants']

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
            if stored_values[participant]['like'] is True:
                stored_values[participant]['like'] = False
            else:
                stored_values[participant]['like'] = True
                stored_values[participant]['dislike'] = False
        else:
            if stored_values[participant]['dislike'] is True:
                stored_values[participant]['dislike'] = False
            else:
                stored_values[participant]['like'] = False
                stored_values[participant]['dislike'] = True

        with open_file(alt_path, 'w') as f:
            json.dump(judge_data, f, indent=2)
        with open_file(path, 'w') as f:
            json.dump(judge_data, f, indent=2)
        return json.dumps(judge_data)

    def finish_voting(self, login: str):
        """Метод для завершения голосования по логину судьи"""

        path, alt_path = self.get_paths(login)
        if not smbclient.path.exists(alt_path):
            self.create_login_files(login)

        with open_file(alt_path, 'r') as f:
            judge_data = json.load(f)

        # для завершения голосования должно быть 15 голосов
        counter = 0
        for participant in judge_data['participants']:
            if judge_data['participants'][participant]['like'] is True:
                counter += 1
        if counter != 15:
            return json.dumps(judge_data)

        judge_data['finished'] = True
        with open_file(alt_path, 'w') as f:
            json.dump(judge_data, f, indent=2)
        with open_file(path, 'w') as f:
            json.dump(judge_data, f, indent=2)

        participants = list(judge_data['participants'].keys())
        positive_votes = {login: [
            participant for participant in participants
            if judge_data['participants'][participant]['like'] is True
        ]}
        judge_results_path = os.path.join(
            self.output_path,
            self.finished_json_filename_template.substitute(login=login))
        alt_judge_results_path = os.path.join(
            self.alt_output_path,
            self.finished_json_filename_template.substitute(login=login))
        with open_file(judge_results_path, 'w') as f:
            json.dump(positive_votes, f, indent=2)
        with open_file(alt_judge_results_path, 'w') as f:
            json.dump(positive_votes, f, indent=2)

        return json.dumps(judge_data)
