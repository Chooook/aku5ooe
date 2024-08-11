from random import shuffle
from OOEContest import OOEContest


if __name__ == '__main__':
    instance = OOEContest()
    login = 'login7'
    print(instance.get_judge_data(login))
    participants = list(range(1, 31))
    shuffle(participants)

    for i in range(15):
        print(instance.update_votes(login, f'checkbox{participants.pop()}_1'))

    print(instance.finish_voting(login))
    print(instance.renew_voting(login))
    instance.save_results_to_excel()
