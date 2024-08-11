from OOEContest import OOEContest


if __name__ == '__main__':
    instance = OOEContest()
    print(instance.get_judge_data('login'))

    print(instance.update_votes('login', 'checkbox1_2'))
    print(instance.update_votes('login', 'checkbox3_2'))
    print(instance.update_votes('login', 'checkbox3_2'))
    print(instance.update_votes('login', 'checkbox20_2'))
    print(instance.update_votes('login', 'checkbox4_2'))
    print(instance.update_votes('login', 'checkbox5_2'))
    print(instance.update_votes('login', 'checkbox6_2'))
    print(instance.update_votes('login', 'checkbox7_2'))
    print(instance.update_votes('login', 'checkbox8_2'))
    print(instance.update_votes('login', 'checkbox9_2'))
    print(instance.update_votes('login', 'checkbox10_2'))
    print(instance.update_votes('login', 'checkbox11_2'))
    print(instance.update_votes('login', 'checkbox12_2'))
    print(instance.update_votes('login', 'checkbox13_2'))
    print(instance.update_votes('login', 'checkbox14_2'))
    print(instance.update_votes('login', 'checkbox15_2'))
    print(instance.update_votes('login', 'checkbox16_2'))
    print(instance.update_votes('login', 'checkbox17_2'))

    print(instance.finish_voting('login'))
    print(instance.renew_voting('login'))
