import itchat  

superlist = []

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	id = msg.fromUserName
	if msg.text == "aaa": 
		superlist.append(id)
		itchat.send("Kingsman Mode!!!",toUserName=id) 
		print("Kingsman Mode!!!")
	if msg.text == "qqq":
		superlist.remove(id)
		itchat.send("Moron Mode!!!",toUserName=id) 
		print("Moron Mode!!!")
	if id in superlist:
		if(msg.text=='weather'):
			print("Weather is: Unknown")
		#itchat.send(msg.text,toUserName=msg.fromUserName) 

#itchat.auto_login()
#itchat.run() 
