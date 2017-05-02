from uuid import uuid1 as uuid
from datetime import datetime, timedelta

from .error import ApiException
from .role import Role

class SessionException(ApiException):
	status_code = 401

class SessionManager(object):
	def __init__(self, timeout = 900, max_user_sessions = 10):
		self.timeout = timedelta(seconds=timeout)
		self.max_user_sessions = max_user_sessions
		self.sessions = {}
		self.user_sessions = {}
		self.customer_sessions = {}

	@classmethod
	def from_object(self, config):
		timeout = config['api'].getint('session_timeout', 900)
		max_user_sessions = config['api'].getint('session_max_per_user', 10)
		return self(timeout = timeout,
				max_user_sessions = max_user_sessions)

	def lookup(self, session_id):
		try:
			session = self.sessions[session_id]

			if datetime.utcnow() > session["expire_time"]:
				self.__delete(session_id)
				raise SessionException("Session expired", payload=session)

			self.__update_expire_time(session)
			return session

		except KeyError:
			raise SessionException("Missing session", payload=session_id)

	def create(self, user):
		"""
		Create user session with given user information

		The exception should never be raised since we use UUID as session ID
		"""
		session_id = str(uuid())

		if session_id in self.sessions:
			raise SessionException("Session \"" + session_id +
					"\" already exists")

		if user.role == Role.customer:
			""" This is customer, store as customer session """
			if user.id in self.customer_sessions:
				if len(self.customer_sessions[user.id]) > self.max_user_sessions:
					raise SessionException("Reached maximum of allowed sessions "
							"per customer")
				self.customer_sessions[user.id].append(session_id)
			else:
				self.customer_sessions[user.id] = [session_id]
		elif (user.role == Role.admin or
				user.role == Role.user or
				user.role == Role.guest):
			""" This is user, store as user session """
			if user.id in self.user_sessions:
				if len(self.user_sessions[user.id]) > self.max_user_sessions:
					raise SessionException("Reached maximum of allowed sessions "
							"per user")
				self.user_sessions[user.id].append(session_id)
			else:
				self.user_sessions[user.id] = [session_id]
		else:
			raise SessionException("Unsupported role")

		self.sessions[session_id] = {
			"user" : user,
			"expire_time" : datetime.utcnow() + self.timeout,
			"session_id" : session_id
		}

		return(session_id)

	def delete(self, session_id):
		try:
			self.__delete(session_id)
		except KeyError:
			raise SessionException("Missing session", payload=session_id)

	def __delete(self, session_id):
		role = self.sessions[session_id]['user'].role
		if role == Role.customer:
			self.customer_sessions[self.sessions[session_id]['user'].id].remove(session_id)
		elif role == Role.admin or role == Role.user or role == Role.guest:
			self.user_sessions[self.sessions[session_id]['user'].id].remove(session_id)
		else:
			raise SessionException("Unsupported role")
		del self.sessions[session_id]

	def __update_expire_time(self, session):
		session['expire_time'] = session['expire_time'] + self.timeout

