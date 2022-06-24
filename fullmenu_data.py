import random


# PERSONNEL
names = ['RALPH', 'MIKE', 'CHARLIE', 'ALEX', 'ZEKE']
costs = [100, 200, 300, 400]
descs = ['This is a person that can do cool things.']

staff = []
for i in range(10):
    person = {'name': random.choice(names),
              'cost': random.choice(costs),
              'desc': random.choice(descs)}
    staff.append(person)

# INTEL
names = ['REMOTE ACCESS', 'DEFENCE', 'OFFENCE', 'AI', 'AI [II]']
costs = [100*i for i in range(20)]
descs = ['This is a brief that will increase our cyber capabilities.', 'This is a brief that will allow us to do cool things.']

briefs = []
for i in range(20):
    brief = {'name': random.choice(names),
             'cost': random.choice(costs),
             'desc': random.choice(descs)}
    briefs.append(brief)

# CYBER
off_cyber = []
def_cyber = []


#ACQUISITIONS
acq_data = [{'name': 'GPS', 'money_cost': 10000, 'personnel_required': 15, 'desc': 'A satellite made for navigation and location based purposes.'},
            {'name': 'ABD', 'money_cost': 8000, 'personnel_required': 10, 'desc': 'Something cool idk.'},
            {'name': 'SPI', 'money_cost': 12000, 'personnel_required': 12, 'desc': 'Stolen Russian spy tech. May have a bug or two.'},
            {'name': 'MDef', 'money_cost': 5000, 'personnel_required': 10, 'desc': 'Missile defence system.'},
            {'name': 'ABCDE', 'money_cost': 13000, 'personnel_required': 1, 'desc': 'A Big Case of Death Engines *shrug*'},
            {'name': 'IROOI', 'money_cost': 80000, 'personnel_required': 800, 'desc': 'I ran out of ideas lmao'},
            {'name': 'ICBM', 'money_cost': 7500, 'personnel_required': 3, 'desc': 'Big bomb go BOOM'},
            {'name': 'B.O.L.L.S.', 'money_cost': 20000, 'personnel_required': 20, 'desc': 'Big Offensive Lock-on Laser System'},
            {'name': 'Nukes', 'money_cost': 50000, 'personnel_required': 40, 'desc': 'hehehe.. get nuked'}]

# OPS


# RESEARCH
