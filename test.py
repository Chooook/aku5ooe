from random import shuffle

from OOEContest import OOEContest


if __name__ == '__main__':
    instance = OOEContest()
    login = '00000000'

    print(instance.get_judge_data(login))
    participants = list(range(1, 31))
    shuffle(participants)
    for i in range(15):
        p = participants.pop()
        print(instance.update_votes(login, f'checkbox{p}_1'))
        print(instance.update_votes(login, f'checkbox{p}_1'))
    print(instance.finish_voting(login))
    print(instance.renew_voting(login))
    # instance.save_results_to_excel()
