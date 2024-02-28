import json

from dorfaksoftcore.domain.Entity import Entity
from dorfaksoftcore.infrastructure.JavaScriptSerializer import JavaScriptSerializer


class LoadApplication(Entity):
	JSON_ALIAS = {"accessDenied": "a", "messageType": "mt", "message": "m", "data": "d", "newToken": "t", "apps": "ap"
		, "isFree": "f", "adsTypeService": "ats", "adsType": "at"}
	ACCESS_DENIED_TRUE = 1
	ACCESS_DENIED_FALSE = 0

	MESSAGE_TYPE_NONE = 0
	MESSAGE_TYPE_INFO = 1
	MESSAGE_TYPE_NEW_VERSION = 2
	MESSAGE_TYPE_ERROR = 3
	MESSAGE_TYPE_INVALID_TOKEN = 4

	ADS_TYPE_SERVICE_NONE = 0
	ADS_TYPE_SERVICE_TAPSELL = 1
	ADS_TYPE_SERVICE_TAPLIGH = 2
	ADS_TYPE_SERVICE_WEB = 3

	ADS_TYPE_PREROLLVIDEO = 0
	ADS_TYPE_NATIVEBANNER = 1
	ADS_TYPE_REWARDBASED = 2
	ADS_TYPE_WEB_VIEW = 3

	accessDenied = ACCESS_DENIED_FALSE
	messageType = MESSAGE_TYPE_NONE
	adsTypeService = ADS_TYPE_SERVICE_TAPLIGH
	adsType = ADS_TYPE_PREROLLVIDEO

	message = ""
	data = ""
	newToken = ""
	apps = []

	def setAccessDenied(self, accessDenied):
		self.accessDenied = accessDenied

	def setMessage(self, message):
		self.message = message

	def setMessageType(self, messageType):
		self.messageType = messageType

	def setAdsTypeService(self, adsTypeService):
		self.adsTypeService = adsTypeService

	def setAdsType(self, adsType):
		self.adsType = adsType

	def __init__(self, packageName=None):
		if packageName != None:
			# rows = AppDAOImpl().queryAll()
			rows=[]
			self.apps = []
			for row in rows:
				if (row.packageName != packageName):
					self.apps.append(row)

			# self.apps=JavaScriptSerializer().serialize(self.apps)
