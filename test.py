from random import shuffle

from OOEContest import OOEContest

private_key_pem = """
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
    for login in logins:
        participants = list(range(1, 31))
        shuffle(participants)
        data = []
        for i in range(15):
            data.append(f'checkbox{participants.pop()}_1')
        data = '["' + '", "'.join(data) + '"]'
        instance.save_data(login, data)
    instance.save_results_to_excel(private_key_pem)
