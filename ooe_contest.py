import json
import os


class OOEContest:
    def __init__(self):
        """Класс для работы с голосованием по конкурсу"""
        self.version = 0.1

        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.json_filename = 'contest_info.json'
        self.json_path = os.path.join(self.current_dir, self.json_filename)
        # если возможно достать список логинов - лучше использовать их
        self.emails = ['ovch@omega.sbrf.ru',
                       'judge2@omega.sbrf.ru',
                       'judge3@omega.sbrf.ru',
                       'judge4@omega.sbrf.ru',
                       'judge5@omega.sbrf.ru',
                       'judge6@omega.sbrf.ru',
                       'judge7@omega.sbrf.ru',
                       'judge8@omega.sbrf.ru']

    def get_judge_data(self, email: str = None):
        """Метод для получения данных о голосовании по email судьи"""
        email = email.lower()
        if email not in self.emails:
            return None

        with open(self.json_path, 'r') as f:
            stored_data = json.load(f)[email]
        return json.dumps(stored_data)

    def update_votes(self, email: str, new_data: str):
        """Метод для обновления данных о голосовании по email судьи"""
        # добавить переменную на фронте для проверки, завершено голосование
        # или нет, если да - обновление данных недоступно
        email = email.lower()
        if email not in self.emails:
            return None
        print(new_data)
        new_data: dict = json.loads(new_data)

        with open(self.json_path, 'r') as f:
            all_data = json.load(f)
            finished = all_data[email]['finished']
            stored_values = all_data[email]['participants']

        if finished:
            return self.get_judge_data(email)

        for participant in new_data:
            new_values = new_data[participant]
            if 'like' in new_values:
                stored_values[participant]['like'] = (new_values['like'])
            if 'read' in new_values:
                stored_values[participant]['read'] = (new_values['read'])

        with open(self.json_path, 'w') as f:
            to_change = all_data[email]['participants']
            to_change.update(stored_values)
            json.dump(all_data, f, indent=2)
        return self.get_judge_data(email)

    def finish_voting(self, email: str):
        """Метод для завершения голосования по email судьи"""
        email = email.lower()
        if email not in self.emails:
            return None

        with open(self.json_path, 'r') as f:
            all_data = json.load(f)

        # для завершения голосования должно быть 15 голосов
        counter = 0
        for participant in all_data[email]['participants']:
            if all_data[email]['participants'][participant]['like'] is True:
                counter += 1
        if counter != 15:
            return self.get_judge_data(email)

        with open(self.json_path, 'w') as f:
            all_data[email]['finished'] = True
            json.dump(all_data, f, indent=2)

        participants = list(all_data[email]['participants'].keys())
        positive_votes = {email: [
            participant for participant in participants
            if all_data[email]['participants'][participant]['like'] is True
        ]}
        judge_results_path = os.path.join(self.current_dir,
                                          f'{email}_results.json')
        with open(judge_results_path, 'w') as f:
            json.dump(positive_votes, f, indent=2)

        return self.get_judge_data(email)


if __name__ == '__main__':
    instance = OOEContest()
    instance.get_judge_data('ovch@omega.sbrf.ru')
    instance.update_votes('ovch@omega.sbrf.ru',
                          '{"participant1": {"like": false}'
                          ',"participant2": {"like": false}'
                          ',"participant3": {"like": false}'
                          ',"participant4": {"like": false}'
                          ',"participant5": {"like": false}'
                          ',"participant6": {"like": false}'
                          ',"participant7": {"like": false}'
                          ',"participant8": {"like": false}'
                          ',"participant9": {"like": false}'
                          ',"participant10": {"like": false}'
                          ',"participant11": {"like": false}'
                          ',"participant12": {"like": false}'
                          ',"participant13": {"like": false}'
                          ',"participant14": {"like": false}'
                          ',"participant15": {"like": false}}')
    instance.finish_voting('ovch@omega.sbrf.ru')
