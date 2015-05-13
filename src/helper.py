from config import db
from flask import jsonify
from jsonschema import validate, exceptions,ValidationError
def validate_user(user):
   schema = {
	"type" : "object",
	"properties" : {
	    "username" : { "type" : "string" },
	    "batch" : { "type" : "number" },
	    "department" : { "type" : "string" },
	},
    }
   try:
	validate(user,schema)
   except (ValidationError), e :
	print e.message
	return False
   tempUser = db.users.find_one({'username': user["username"]});
   print tempUser
   print user["username"]
   if tempUser is not None:
        return False
   return True

def valid_login(username):
  user = db.users.find_one({'username' : username})
  if user is not None:
    return jsonify({'logged_in':1})

  return jsonify({'logged_in':0})