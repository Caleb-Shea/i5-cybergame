import random

names = ['RALPH', 'MIKE', 'CHARLIE', 'ALEX', 'ZEKE']
costs = [100, 200, 300, 400]
desc = ['This is a person that can do cool things.']

staff = []
for i in range(10):
    person = {'name': random.choice(names),
              'cost': random.choice(costs),
              'desc': random.choice(desc)}
    staff.append(person)
