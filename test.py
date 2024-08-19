from random import shuffle

from OOEContest import OOEContest

private_key_pem = 'private.pem'

logins = [
    'login1',
    'login2',
    'login3',
    'login4',
    'login5',
    'login6',
    'login7',
    'login8',
]

if __name__ == '__main__':
    instance = OOEContest()
    for _ in range(2):
        for login in logins:
            participants = list(range(1, 31))
            shuffle(participants)
            data = []
            for i in range(15):
                data.append(f'checkbox{participants.pop()}_1')
            instance.save_data(login, data)
    instance.save_results_to_excel(private_key_pem)
