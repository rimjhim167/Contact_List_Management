from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient 
from bson.objectid import ObjectId 
from bson.errors import InvalidId

cl = MongoClient('localhost', 27017)    #connection to mongoDB
db = cl.contact   
con = db.contact 

app = Flask(__name__)
title = "Contact List Management"
heading="Contact List"

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")  #data from database
def lists ():
	con_l = con.find().sort([("name", 1),("date", -1)])
	a1="active"
	return render_template('index.html',a1=a1,con=con_l,t=title,h=heading)

@app.route("/")

@app.route("/action", methods=['POST'])	#insert into database
def action ():
	
	name=request.values.get("name")
	cont=request.values.get("cont")
	date=request.values.get("date")
	abt=request.values.get("abt")
	if cont:
			con.insert({ "name":name, "con":cont, "date":date, "abt":abt})
	return redirect("/list")

@app.route("/remove")		#delete from database
def remove ():
	key=request.values.get("_id")
	con.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")	
def update ():
	id=request.values.get("_id")
	c=con.find({"_id":ObjectId(id)})
	return render_template('update.html',c=c,h=heading,t=title)

@app.route("/action3", methods=['POST'])	#update in database
def action3 ():
	name=request.values.get("name")
	cont=request.values.get("con")
	date=request.values.get("date")
	abt=request.values.get("abt")
	id=request.values.get("_id")
	if id:
		con.update({"_id": ObjectId(id)}, {'$set':{ "name":name, "con":cont, "date":date, "abt":abt }})
	return redirect("/")

@app.route("/search", methods=['GET'])	#finding reference to searchs in database and then search
def search():
	n=request.values.get("n")
	ref=request.values.get("ref")
	if(ref=="id"):
		try:
			con_l = con.find({ref:ObjectId(n)})
			if not con_l:
				return render_template('index.html',con=con_l, t=title,h=heading, error="No such ObjectId is present")
		except InvalidId as err:
			pass
			return render_template('index.html',con=con_l,t=title,h=heading,error="Invalid ObjectId format given")
	else:
		con_l = con.find({ref:n})
	return render_template('search.html',con=con_l,t=title,h=heading)

@app.route("/about")
def about():
	return render_template('about.html',t=title,h=heading)


if __name__ == "__main__":
    app.run(debug=True)

