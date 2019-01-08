#to install tinydb: pip install tinydb

from tinydb import TinyDB, Query
db = TinyDB('questions.json')

db.insert({'int': 1, 'question': 'do you need help?'})

result = db.get(Query()['int'] == 1)

question = result.get('question')

print question
