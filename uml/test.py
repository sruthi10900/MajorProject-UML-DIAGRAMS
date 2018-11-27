import turtle
#from django.shortcuts import render
import nltk
import collections
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import OrderedDict
from PIL import Image
from turtle import *
from flask import Flask,render_template,request
app = Flask(__name__)
extra_classes=[]
actors=[]
verbs=[]
dict={}
extra=[]
classes={}
actor_func={}
dicttemp={}
'''import canvasvg
import os
import tempfile
import shutil'''
@app.route('/')
def result():
	html_form = '''
		<body style="background-color:#40CECA;">
    	<form action="/classes1" method="post">
		<br>
		<center>
    		Enter your specifications:<br> <textarea rows="4" cols="50" name="txt"> </textarea><br><br><input type="submit" value="submit" name="class">
		</center>
    	</form>
		</body>

    '''
	
	return html_form

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
@app.route('/classes1',methods=['POST','GET'])
def classes1():
	# Create your views here.
	#txt="User can send invitation to connect and Admin can grant invitation. They can also send multimedia and receiving multimedia. They can record multimedia as well."
	#txt="Writer drafts a story and revises story and Editor reviews story and suggests edits. The Agent sells story whereas distributor packages story. Bookseller delivers the story to customers. Also he helps edits."
	#txt="User can send. Admin grants the invitation."
	#txt="User fills the details. She selects the slot. Admin records details. User makes the payment. If the payment is successful, the Admin generates the registrationid and displays it to User."
	
	txt =request.form.get('txt')
	print(txt)
	tokens=nltk.word_tokenize(txt)
	print (tokens)
	tokenpos=nltk.pos_tag(tokens)
	print (tokenpos)	
	#print (token)
	from django.http import HttpResponse
	
	ps=PorterStemmer()
	lmtzr=WordNetLemmatizer()
	i=0
	token=[list(row) for row in tokenpos]
	for w in tokens:
		token[i][0]=lmtzr.lemmatize(w,pos="v")
		#token[i][0]=ps.stem(w)
		i=i+1
	print(len(tokens))
	i=0
	flag=0
	for w in token:
		if i+1<len(token) and token[i][1]=='NNP':
			if i+1<len(token) and token[i+1][1]=='NNP' and token[i+1][0] not in ['number','no','code','date','type','volume','birth','id','address','name']: 
				actors.append(token[i+1][0])
				dict[token[i+1][0]]=[]
				i=i+1
			   
			else:
				actors.append(token[i][0])
				dict[token[i][0]]=[]
		elif i+1<len(token) and token[i][1]=='NN' and token[i-1][1]=='DT':
			print ("hie")
			print(token[i][0])
			if token[i][0].endswith('er') or token[i][0].endswith('or'):
				print("hiwee")
				actors.append(token[i][0])
				dict[token[i][0]]=[]
				
		i=i+1
	print (actors)

	i=0
	j=0
	for w in token:
		
		if token[i][1]=='VB' or token[i][1]=='VBD' or token[i][1]=='VBG' or token[i][1]=='VBN' or token[i][1]=='VBP' or token[i][1]=='VBZ':
			if i+1<len(token) and (token[i+1][1]=='NN' or token[i+1][1]=='NNS'):
				str=token[i][0]+" "+token[i+1][0]
				if str not in verbs:
				
					verbs.append(str)
			elif i+1<len(token) and token[i+1][1]=='DT':
				if i+2<len(token) and (token[i+2][1]=='NN' or token[i+2][1]=='NNS'):
					str=token[i][0]+" "+token[i+1][0]+" "+token[i+2][0]
					if str not in verbs:
						verbs.append(str)
			else:
				str=token[i][0]
				if str not in verbs and str!='be':
					verbs.append(str)
		i=i+1
	j=0
	print (verbs)
	i=0
	k=0


	while i<=len(token)-1:
		print("kk")
		
		if token[i][1]=='NNP' or token[i][1]=='NN':
			j=i+1
			temp=[]
			
			while j<len(token) and token[j][1]!='NNP':
				
				if token[j][1]=='.':
						
						k=j
						while j<len(token)-1 and token[j+1][1]!='.' and k<len(token) -1:
							k=k+1
							
							if token[k][1]=='NNP':
								break
							elif token[k][1]=='VB' or token[k][1]=='VBD' or token[k][1]=='VBG' or token[k][1]=='VBN' or token[k][1]=='VBP' or token[k][1]=='VBZ':
								if k+1<len(token) and token[k+1][1]=='NN' or token[k+1][1]=='NNS':
									str=token[k][0]+" "+token[k+1][0]
									if str not in extra:
										extra.append(str)
								elif k+1<len(token) and token[k+1][1]=='DT':
									if k+2<len(token) and token[k+2][1]=='NN' or token[k+2][1]=='NNS':
										str=token[k][0]+" "+token[k+1][0]+" "+token[k+2][0]
										if str not in extra:
											extra.append(str)
								else:
									str=token[k][0]
									if str not in extra and str!='be':
										extra.append(str)
				if token[j][1]=='VB' or token[j][1]=='VBD' or token[j][1]=='VBG' or token[j][1]=='VBN' or token[j][1]=='VBP' or token[j][1]=='VBZ':
						if j+1<len(token) and token[j+1][1]=='NN' or token[j+1][1]=='NNS':
							str=token[j][0]+" "+token[j+1][0]
							if str not in dict[token[i][0]]:
								dict[token[i][0]].append(str)
						elif j+1<len(token) and token[j+1][1]=='DT':
							if j+2<len(token) and token[j+2][1]=='NN' or token[j+2][1]=='NNS':
								str=token[j][0]+" "+token[j+1][0]+" "+token[j+2][0]
								if str not in dict[token[i][0]]:
									dict[token[i][0]].append(str)
						else:
							str=token[j][0]
							if str not in dict[token[i][0]] and str!='be':
								dict[token[i][0]].append(str)
				
				
				#print (temp)
				j=j+1
		if j!=0:
			i=j
		else:
			i=i+1
	i=0
	j=0
	print (dict)
	while i<len(token) and token[i][1]!='PRP':
		if i<len(token)-1:
			if token[i+1][0]=='they' or token[i+1][0]=='They':
				j=i+1
				k=j
				rev=i
				act=[]
				while rev>=0 :
					if token[rev][1]=='NNP' and token[rev][0] in actors:
						
						act.append(token[rev][0])
					rev=rev-1
			
				while token[j][1]!='.' and token[j][1] not in actors and token[j][1]!='he' and token[j][1]!='He'  and token[j][1]!='she'  and token[j][1]!='She':
					j=j+1
				#print(j)
				while k<=j:
					#print(k)
					if token[k][1]=='VB' or token[k][1]=='VBD' or token[k][1]=='VBG' or token[k][1]=='VBN' or token[k][1]=='VBP' or token[k][1]=='VBZ':
							if k+1<len(token): 
								if token[k+1][1]=='NN' or token[k+1][1]=='NNS':
									str=token[k][0]+" "+token[k+1][0]
									if str in extra:
										extra.remove(str)
									l=0
									while l<len(act):
										if str not in dict[act[l]]:
											dict[act[l]].append(str)
										l=l+1
									l=0
								elif k+1<len(token) and token[k+1][1]=='DT':
									if k+2<len(token) and token[k+2][1]=='NN' or token[k+2][1]=='NNS':
										str=token[k][0]+" "+token[k+1][0]+" "+token[k+2][0]
										if str in extra:
											extra.remove(str)
										l=0
										while l<len(act):
											if str not in dict[act[l]] and str!='be':
												dict[act[l]].append(str)
											l=l+1
										l=0
								else:
									l=0
									str=token[k][0]
									if str  in extra:
										extra.remove(str)
				  
									while l<len(dict):
										if str not in dict[act[l]] and str!='be':
											dict[act[l]].append(str)
										l=l+1
									l=0
					k=k+1
				i=i+1
			elif token[i+1][0]=='he' or token[i+1][0]=='He' or token[i+1][0]=='she' or token[i+1][0]=='She':
					
					j=i+1
					print(j)
					rev=i
					while token[rev][0] not in actors:
						rev=rev-1
					act=token[rev][0]
					
					while token[j][1]!='.' and token[j][1]!='NNP':
						#print (j)
						if token[j][1]=='VB' or token[j][1]=='VBD' or token[j][1]=='VBG' or token[j][1]=='VBN' or token[j][1]=='VBP' or token[j][1]=='VBZ':
							#print (token[j][0])
							if j+1<len(token): 
								
								if token[j+1][1]=='NN' or token[j+1][1]=='NNS':
									
									str=token[j][0]+" "+token[j+1][0]
									if str in extra:
										#print("keerthana Goli")
										extra.remove(str)
						
									if str not in dict[act]:
										dict[act].append(str)
									
								elif j+1<len(token) and token[j+1][1]=='DT':
									
									if j+2<len(token) and token[j+2][1]=='NN' or token[j+2][1]=='NNS':
										str=token[j][0]+" "+token[j+1][0]+" "+token[j+2][0]
										if str in extra:
											extra.remove(str)
									
										if str not in dict[act]:
											dict[act].append(str)
										
								else:
									
									str=token[j][0]
									if str  in extra:
										extra.remove(str)
					
									if str not in dict[act] and str!='be':
										 dict[act].append(str)
									
						j=j+1
					i=i+1
					
						
		i=i+1
		
	j=0
	i=0
	for w in actors:
		j=0
		while j<len(dict[actors[i]]):
			#print (dict[actors[i]][j])
			for y in extra:
				if(dict[actors[i]][j]==y):	
					
					dict[actors[i]].pop(j)
					j=j-1
					
			j=j+1
		i=i+1
	print (dict)
	print (extra)
	k=len(actors)

	
	for a in actors :
		classes[a]=[]
	classes["Database"]=[]
	for a in actors:
		str1=a+"Id"
		str2=a+"Name"
		str3=a+"Password"
		if str1 not in classes[a]:
			classes[a].append(str1)
		if str2 not in classes[a]:
			classes[a].append(str2)
		if str3 not in classes[a]:
			classes[a].append(str3)

	for a in actors:
		if a!="Database" and classes[a] not in classes["Database"]:
			classes["Database"].append(classes[a])

	print (classes)

	
	for w in classes:
		actor_func[w]=[]
	for a in dict:
		for v in dict[a]:
			str=v+"()"
			actor_func[a].append(str)
	actor_func["Database"]=[]
	for i in classes:
		if i!="Database":
			for j in classes[i]:
				str="add"+j
				actor_func["Database"].append(str)
	print (actor_func)

	
	for w in verbs: 
		tokens=nltk.word_tokenize(w)
		
		for x in tokens:
			for l in tokenpos:
				if x==l[0]:
					if l[1]=='NN':
						if l[0] not in extra_classes:
							extra_classes.append(l[0])
					
	print (extra_classes)
	print("hi")
	print (dict)
	return render_template('hello.html',result=extra_classes)
@app.route('/classes',methods=['POST','GET'])
def functn():
	return render_template('new1.html',result=extra_classes)
@app.route('/usecase',methods=['POST','GET'])
def usecase():
	
	p=Turtle()
	p.x=10
	p.y=10
	p.goto(p.x,p.y)

	# set a shape and colour
	p.shape("circle")
	p.shapesize(3,10,2)
	p.fillcolor("red")
	p.pencolor("black")

	p.penup() # no drawing
	#goto(-100,-100)

	# main draw loop
	p.x=0
	p.y=0
	k=len(verbs)
	i=1
	#print(k)
	tur=Turtle()
	tur.xcor=100
	tur.ycor=400
	tur.penup()
	a=0
	screen=turtle.Screen()
	screen.addshape("resize.gif")
	tur.shape("resize.gif")
	tur.shapesize(4,4,2)
	tur.fillcolor("red")
	actpos={}
	j=0
	while j< len(actors):
		actpos[actors[j]]=()
		j=j+1
	#print(actpos)
	while a < len(actors):
		if actors[a]=='User' or actors[a]=='Customer' or actors[a]=='Client':
			pos=tur.setpos(-300,0)
			#print(tur.position())
		
			actpos[actors[a]]=tur.position()
			tur.stamp()
			tur.setpos(-300,-70)
			tur.write(actors[a],move=False, align="left",font=("Arial",10,"normal"))
		elif actors[a]=='Admin' or actors[a]=='Librarian':
			pos=tur.setpos(300,0)
			#print(tur.position)
		
			actpos[actors[a]]=tur.position()
			tur.stamp()
			tur.setpos(300,-70)
			tur.write(actors[a],move=False, align="left",font=("Arial",10,"normal"))
		else:
			pos=tur.setpos(-300,tur.ycor-100)
		#tur.ycor=tur.ycor-100
		#print(tur.position())
		
			actpos[actors[a]]=tur.position()
			tur.stamp()
			tur.setpos(-300,tur.ycor-170)
			tur.write(actors[a],move=False, align="left",font=("Arial",10,"normal"))
			tur.ycor=tur.ycor-150
		a=a+1
		tur.hideturtle()
	flag=0
	p.hideturtle()
	z=0
	while i<=k:
	
		if(z%2==0):
			p.y=p.y+100*z
		else:
			p.y=p.y-100*z
		p.goto(p.x,p.y)
		z=z+1
		ts=p.stamp()
		p.write(verbs[i-1],move=False, align="center",font=("Arial",10,"normal"))
		tpos=p.position()
		p.pendown()
		gp=''
		flag=0
		w=0
		for w in dict:
			for gp in dict[w]:
				if verbs[i-1]==gp:
					for act in actpos:
						if act==w:
							#print(act)
							p.pendown()
							#print(actpos[act])
							p.goto(actpos[act])
							p.penup()
							#p.goto(tpos)
							#p.x=-30
							#print(p.xcor())
							#print(tpos)
							p.goto(tpos)
	
	
	
		i=i+1
	ts=turtle.getscreen()
	#ts.getcanvas().postscript(file="abc.eps")
	#img=Image.open("abc.eps")
	#img.load(scale=3)
	#img.show()
	#img.save("foo.jpg",quality=95)
	exitonclick()
	#return_data["p"]=dict
	return render_template('hello1.html' ,result=select_classes)
select_classes=[]
@app.route('/attfunc',methods=['POST'])
def attributes():
	
	for i in extra_classes:
		if request.form.get(i):
			select_classes.append(i)
			classes[i]=[]
			actor_func[i]=[]
	return render_template('attfunc.html',result=select_classes)


@app.route('/typedatt',methods=['POST'])
def entered_attributes():
	
	for i in select_classes:
		txt1=request.form.get(i)
		atts=[]
		atts=nltk.word_tokenize(txt1)
		for k in atts:
			classes[i].append(k)
		print(txt1)
	print (classes)	
	#classes = collections.OrderedDict(sorted(classes.items()))
	print (classes)
	return render_template('typedatt.html',result=select_classes)

	
@app.route('/hello',methods=['POST'])
def entered_functions():
	
	for i in select_classes:
		txt1=request.form.get(i)
		atts=[]
		atts=nltk.word_tokenize(txt1)
		for k in atts:
			actor_func[i].append(k+"()")
	print(actor_func)
	return render_template('hello.html',result=select_classes)
@app.route('/hello1',methods=['POST','GET'])
def diagram():	
	c=0
	k=Turtle()
	k.penup()	
	p=Turtle()
	tur=Turtle()
	tur.win_width, tur.win_height, tur.bg_color = 2000, 2000, 'white'
	turtle.setup()
	turtle.screensize(tur.win_width, tur.win_height, tur.bg_color)
	cor={}
	for z in classes:
		cor[z]=[]
	tur.x=-450
	tur.y= 800
	tur.shape("square")
	tur.shapesize(13,15,2)
	tur.fillcolor("white")
	flag=1
	tur.penup()
	'''tur.shapesize(13,15,2)
	tur.fillcolor("white")
	tur.goto(tur.x,tur.y)
	tur.stamp()'''
	i=0;
	p.penup()
	p.tempx=0
	p.tempy=0
	for i in classes:
		
		tur.goto(tur.x,tur.y)
		tur.stamp()
		'''if i=='Admin':
			p.tempx=tur.x
			p.tempy=tur.y'''
		p.goto(tur.x,tur.y+100)
		p.write(i)
		p.goto(tur.x-105,p.ycor()-20)
		p.pendown()
		p.x=p.xcor()-50
		p.y=p.ycor()
		p.xtemp=p.xcor()
		p.ytemp=p.ycor()
		p.goto(p.x,p.y)
		p.forward(298)
		'''k=Turtle()
		k.x=p.xcor()
		k.y=k.ycor()'''
		p.penup()
		p.goto(p.xtemp,p.ytemp-20)
		for j in classes[i]:
				if j=="Database":
					for k in classes[j]:
						for l in range(k):
							p.goto(p.xcor(),p.ycor()-20)
							p.write(l)
				else:
					p.goto(p.xcor(),p.ycor()-20)
					p.write(j)
				
		#p.goto(p.xcor(),p.ycor()-20)
		p.pendown()
		p.x=p.xcor()-50
		p.y=p.ycor()
		p.xtemp=p.xcor();
		p.ytemp=p.ycor()
		p.goto(p.x,p.y)
		'''if p.tempx!=0:
			p.goto(p.tempx+150,p.tempy)
			p.pendown()'''
		p.goto(p.x,p.y)
		p.forward(298)
		p.penup()
		p.goto(p.xtemp,p.ytemp-20)
		for n in actor_func[i]:
			p.goto(p.xcor(),p.ycor()-20)
			p.write(n)
		
		if flag==1:
			flag=0
			c=1
			k.setpos(tur.x+150,tur.y)
			tur.x=tur.x+800
			
		#else:
			
		if flag==0 and c==1:
			print("hi")
			c=0
			#tur.goto(tur.x,tur.y)
			#tur.stamp()
		elif flag==0 and c==0:
			k.setpos(tur.x-140,tur.y)
			tur.y=tur.y-300
			
			
			
		cor[i].append(k.xcor())
		cor[i].append(k.ycor())
	xc=0
	xy=0
	print cor
	for p in cor:
		if p=='Admin':
			xc=cor[p][0]
			xy=cor[p][1]
	print(xc)
	print(xy)
	for m in cor:
		k.goto(xc,xy)
		if m!="Admin":
			k.pendown()
			k.goto(cor[m][0],cor[m][1])
			k.penup()
			#k.goto(xc,xy)
			
			
	'''p.goto(-140,100)
	p.write("hello",move=True,align="left")
	p.penup()
	p.goto(-140,95)
	p.pendown()
	p.forward(300)'''
	ts=turtle.getscreen()
	ts.getcanvas().postscript(file="abc.eps")
	img=Image.open("abc.eps")
	img.load(scale=3)
	#img.show()
	img.save("foo.jpg",quality=95)
	exitonclick()
	#return_data["p"]=dict
	#return render_template("hello1.html")
	

	
	
	
if __name__ == '__main__':
   app.run(debug=True)
