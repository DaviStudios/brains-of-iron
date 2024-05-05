import random
import os
import json

client = {
 'name': '',
 'ideology': '',
 'cash': 0,
 'currency': '',
 'analytics': {
  'civil rights': 50,
 },
 'issues': [],
 'president': '',
 'items': [],
 'power': 0,
 'population': 1000,
}

year = 1960

issues = {
 'ban harry potter': {
  'y': lambda: client['analytics'].update({'civil rights': client['analytics']['civil rights'] - 10}),
  'n': lambda: client['analytics'].update({'civil rights': client['analytics']['civil rights'] + 10})
 },
 'execute the homeless': {
  'y': lambda: client['analytics'].update({'civil rights': client['analytics']['civil rights'] - 30}),
  'n': lambda: client['analytics'].update({'civil rights': client['analytics']['civil rights'] + 15})
 },
}

mLeaders = []

def newLeader(name = None):
 if name is None:
  fns = ['Vojton', 'Vojta', 'David', 'Lezin', 'Stazin', 'Karol', 'Jon']
  lns = ['Krajin', 'Chlejba', 'Jozif', 'Vlad', 'Vladimir']
  name = random.choice(fns) + ' ' + random.choice(lns)
 client['president'] = name
 if client['ideology'] == 'Monarchist':
  was = '1'
  for i in mLeaders:
   if i == name:
    was = str(int(was) + 1)
  client['president'] = name + ' the ' + was + '.'
  mLeaders.append(name)
  with open('data/pastM.json', 'w') as f:
   f.write(json.dumps(mLeaders))
  

def save():
 with open('data/save.json', 'w') as f:
  f.write(json.dumps(client))
 with open('data/year.txt', 'w') as f:
  f.write(str(year))

if os.path.exists('data/pastM.json'):
 with open('data/pastM.json', 'r') as f:
  mLeaders = json.loads(f.read())

if os.path.exists('data/save.json'):
 with open('data/save.json', 'r') as f:
  client = json.loads(f.read())
 with open('data/year.txt', 'r') as y:
  year = int(y.read())
else:
 print('Create your country!')
 name = input('Name > ')
 print('Ideologies = \n d = democracy\n m = monarchist\n c = communist')
 ideology = input('Ideology > ')
 currency = input('Currency name > ')
 if ideology == 'd':
  client['name'] = name
  client['ideology'] = 'Democratic'
  client['currency'] = currency
  client['cash'] = random.randint(7000, 11000)
  client['power'] = random.randint(10, 20)
  client['analytics']['civil rights'] = random.randint(80, 100)
  save()
 elif ideology == 'c':
  client['name'] = name
  client['ideology'] = 'Communist'
  client['currency'] = currency
  client['cash'] = random.randint(5000, 7000)
  client['power'] = random.randint(20, 30)
  client['analytics']['civil rights'] = random.randint(40, 60)
  save()
 elif ideology == 'm':
  client['name'] = name
  client['ideology'] = 'Monarchist'
  client['currency'] = currency
  client['cash'] = random.randint(12000, 15000)
  client['power'] = random.randint(30, 45)
  client['analytics']['civil rights'] = random.randint(50, 70)
  save()
 newLeader()

def Taxes():
 averageSalary = 0
 if client['ideology'] == 'Democratic':
  averageSalary = round(client['population'] + (client['cash'] /45) ) + client['power']
 elif client['ideology'] == 'Communist':
  averageSalary = round(client['population'] + (client['cash'] /40) ) + random.randint(500, 1000) + client['power']
 elif client['ideology'] == 'Monarchist':
  averageSalary = round(client['population'] + (client['cash'] /35) ) + random.randint(700, 1200) + client['power']
 client['cash'] += averageSalary
 return averageSalary + random.randint(50,100)

def issue():
 issue = random.choice(list(issues))
 client['issues'].append(issue)

opts = """
1 - Issues
2 - Info
3 - Shop
4 - Usage
"""

shop = {
 'food': 4750,
 'division': 25750,
}

usage = {
 'division': lambda: client.update({'power': client.get('power', 0) + random.randint(5, 8)})
}

leaderC = 0

leaderM = 0

while True:
 client['population'] += round((client['population'] / 15)  + random.randint(1,4))
 leaderC += 1
 if leaderC == 4:
  if client['ideology'] == 'Democratic':
   newLeader()
   leaderC = 0
  elif client['ideology'] == 'Monarchist':
   leaderC = 0
   leaderM += 1
   if leaderM == 10:
    newLeader()
    leaderM = 0
 elif leaderC == 2:
  issue()
  print('New Issue!')
 elif leaderC == 3:
  if 'food' in client['items']:
   client['items'].remove('food')
   client['analytics']['civil rights'] += 10
  else:
   client['population'] += round(((client['population'] / 15)  + random.randint(1,4)) / 2)
   client['analytics']['civil rights'] -= 15
   print('Your population is starving! Go buy more food!')

 if client['analytics']['civil rights'] > 20 and client['analytics']['civil rights'] < 40:
  if client['ideology'] == 'Democratic':
   print('Some people have overtaken your government! You are now an monarchist!')
   client['ideology'] = 'Monarchist'
   newLeader()
 if client['analytics']['civil rights'] > 10 and client['analytics']['civil rights'] < 21:
  if client['ideology'] == 'Monarchist' or client['Ideology'] == 'Democratic':
   print('Some people have overtaken your government! You are now an communist!')
   client['ideology'] = 'Communist'
   newLeader()
  
 year += 1
 save()
 print(' ')
 print('You gained ' + str(Taxes()) + ' ' + client['currency'] + 's in taxes this year!')
 print('Year: ' + str(year))
 print(opts)
 choice = input('> ')
 if choice == '1':
  for i in client['issues']:
   print(i)
  print('Choose an issue to resolve')
  choice = input('> ')
  if choice in client['issues']:
   name = choice
   choice = input('y/n> ')
   if choice in issues:
    issues[name][choice]()
    print('Check analytics!')
   else:
    print('Issue dismissed.')
  else:
   print('Issue not found.')
 elif choice == '2':
  print('Name: ' + client['name'])
  print('Ideology: ' + client['ideology'])
  print('Cash: ' + str(client['cash']))
  print('Population: ' + str(client['population']))
  print('Leader: ' + client['president'])
  print('Power: ' + str(client['power']))
  print('Civil Rights: ' + str(client['analytics']['civil rights']))
  print('Items: ')
  for i in client['items']:
   if i in usage:
    i = i + ' / usable'
   else:
    i = i + ' / nonusable'
   print( ' -' + i)
 elif choice == '3':
  for i in shop:
   print(i + ' = ' + str(shop[i]) + ' ' + client['currency'] + 's')
  choice = input('> ')
  if choice in shop:
   if client['cash'] >= shop[choice]:
    client['cash'] -= shop[choice]
    client['items'].append(choice)
    print('Purchased ' + choice + '!')
   else:
    print('Not enough ' + client['currency'] + 's!')
  else:
   print('Sorry! Don\'t know that item!')
 elif choice == '4':
  for i in usage:
   if i in client['items']:
    print(i)
  choice = input('> ')
  if choice in usage and choice in client['items']:
   usage[choice]()
   client['items'].remove(choice)
 else:
  print('Unknown option!')
   
