import random

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

intel_briefs = [{'name': 'NASA Conference', 'personnel_req': 20, 'sat_req': [], 'color': 'acq', 'desc': 'Attend a NASA conference to study new satellite technology.'},
                {'name': 'Aerial Recon [China]', 'personnel_req': 30, 'sat_req': ['GPS_2'], 'color': 'ops', 'desc': 'Conduct covert recon operations around the South China Sea.'},
                {'name': 'name', 'personnel_req': 1, 'sat_req': [], 'color': 'intel', 'desc': 'desc'},
                {'name': 'name1', 'personnel_req': 2, 'sat_req': [], 'color': 'intel', 'desc': 'desc1'},
                {'name': 'name2', 'personnel_req': 3, 'sat_req': [], 'color': 'intel', 'desc': 'desc2'},
                {'name': 'name3', 'personnel_req': 4, 'sat_req': [], 'color': 'intel', 'desc': 'desc3'},
                {'name': 'name4', 'personnel_req': 5, 'sat_req': [], 'color': 'intel', 'desc': 'desc4'},
                {'name': 'name5', 'personnel_req': 6, 'sat_req': [], 'color': 'intel', 'desc': 'desc5'}]

#ACQUISITIONS
acq_data = [{'name': 'GPS', 'money_cost': 10000, 'personnel_req': 15, 'desc': 'A satellite made for navigation and location based purposes.'},
            {'name': 'ABD', 'money_cost': 8000, 'personnel_req': 10, 'desc': 'Something cool idk.'},
            {'name': 'SPI', 'money_cost': 12000, 'personnel_req': 12, 'desc': 'Stolen Russian spy tech. May have a bug or two.'},
            {'name': 'MDef', 'money_cost': 5000, 'personnel_req': 10, 'desc': 'Missile defence system.'},
            {'name': 'ABCDE', 'money_cost': 13000, 'personnel_req': 1, 'desc': 'A Big Case of Death Engines *shrug*'},
            {'name': 'IROOI', 'money_cost': 80000, 'personnel_req': 800, 'desc': 'I ran out of ideas lmao'},
            {'name': 'ICBM', 'money_cost': 7500, 'personnel_req': 3, 'desc': 'Big bomb go BOOM'},
            {'name': 'B.O.L.L.S.', 'money_cost': 20000, 'personnel_req': 20, 'desc': 'Big Offensive Lock-on Laser System'},
            {'name': 'Nukes', 'money_cost': 50000, 'personnel_req': 40, 'desc': 'hehehe.. get nuked'}]
