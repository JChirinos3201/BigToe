#! /usr/bin/python3
import uuid

def go():
  while True:
    a = input('Want a uuid? (y/N)\t')
    if a.lower() == 'y':
      print(str(uuid.uuid4()))
    else:
      break
      
go()
    