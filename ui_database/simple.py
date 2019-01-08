from tinydb import TinyDB, Query
db = TinyDB('questions.json')

q = Query()

#db.insert({'lan':'PL','num': 1, 'type':'general', 'question': 'Czy potrzebujesz pomocy'})

result = db.get((q.lan == 'PL') & (q.num == 1))

question = result.get('question')

print question
