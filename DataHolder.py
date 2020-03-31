#Object for storing Data from web searches.
#An instance contained within the WebSurfer class.

class DataKeeper(object):

	def __init__(self):
		#Strings to add the collected data to.
		self.timeTable = ""
		self.facebook = "\nFacebook notifications:\n"
		self.facebookTot = 0 #Count how many facebook notifications
		self.outlook = ""
		

	def updateTimeTable(self,events):
		#Add daily timetable info to timetable string
		if events == []:
			self.timeTable += '\nNo Uni Today.'
		
		else:
			self.timeTable += '\nToday you have:\n'
			for what, where in events:
				self.timeTable += '\t' + what + ' at ' + where + '.\n'

	def updateFacebook(self, friendRequests, messages, notifications):
		#Add facebook data to facebook string and increment count.
		try:
			self.facebook += "\tYou have {} friend request.\n".format(int(friendRequests))
			self.facebookTot += int(friendRequests)

		except:
			pass

		try:
			self.facebook += "\tYou have {} messages.\n".format(int(messages))
			self.facebookTot += int(messages)

		except:
			pass

		try:
			self.facebook += "\tYou have {} other notifications.\n".format(int(notifications))
			self.facebookTot += int(notifications)

		except:
			pass

		if self.facebook == "\nFacebook notifications:\n":
			self.facebook = "\nYou have no new Facebook notifications."

		return self.facebookTot
	
	def updateOutlook(self, unread=0, sender="", subject="", contents=""):
		#Add email information to outlook string
		if unread == 0:
			self.outlook += "\nYou have no new emails.\n"

		else:
			self.outlook += "\nYou have {} new emails.\n".format(unread)
			self.outlook += "\tThe first is from {}\n".format(sender)
			self.outlook += "\tSubject: {}\n".format(subject)
			self.outlook += "\t{}\n".format(contents)

	def reportTimeTable(self):
		#Display timetable data
		print(self.timeTable)

	def reportFacebook(self):
		#Display facebook data
		print(self.facebook)

	def reportOutlook(self):
		#Display outlook data
		print(self.outlook)

				
	