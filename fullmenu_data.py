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


#ACQUISITIONS
names = ['GSSAP', 'GPS', 'ISS', 'AEHF']
money_costs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
personnel_required = [1, 2, 3, 4, 5]
descs = ['Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'Make things go BOOM.']

sats = []
for i in range(9):
    sat = {'name': random.choice(names),
           'money_cost': random.choice(costs),
           'personnel_required': random.choice(personnel_required),
           'desc': random.choice(descs)}
    sats.append(sat)

# OPS


# RESEARCH
