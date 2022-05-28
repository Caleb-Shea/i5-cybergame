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


# OPS


# RESEARCH
