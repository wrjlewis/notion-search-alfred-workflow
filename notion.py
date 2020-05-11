import sys
import json
import httplib, urllib
import os

#config
notionSpaceId = os.environ['notionSpaceId']
cookie = os.environ['cookie']
#get useDesktopClient env variable and convert to boolean for use later, default to false unless specified as true
useDesktopClient = os.environ['useDesktopClient']
if (useDesktopClient == 'true') | (useDesktopClient == 'True') | (useDesktopClient == 'TRUE'):
	useDesktopClient = True
else:
	useDesktopClient = False
#get isNavigableOnly env variable and convert to boolean for use later, default to true unless specified as false
isNavigableOnly = os.environ['isNavigableOnly']
if (isNavigableOnly == 'false') | (isNavigableOnly == 'False') | (isNavigableOnly == 'FALSE'):
	isNavigableOnly = False
else:
	isNavigableOnly = True

class Payload(object):
     def __init__(self, j):
         self.__dict__ = json.loads(j)

class searchResult(object):
	def __init__(self, id):
		self._id = id
		self._title = None
		self._icon = None
		self._link = None
		self._subtitle = None

	@property
	def id(self):
		return self._id    

	@property
	def title(self):
		return self._title

	@title.setter
	def title(self, value):
		self._title = value

	@property
	def icon(self):
		return self._icon

	@icon.setter
	def icon(self, value):
		self._icon = value

	@property
	def link(self):
		return self._link

	@link.setter
	def link(self, value):
		self._link = value

	@property
	def subtitle(self):
		return self._subtitle

	@subtitle.setter
	def subtitle(self, value):
		self._subtitle = value

def buildNotionSearchQueryData( str ):
	query = {}

	query["type"] = "BlocksInSpace"
	query["query"] = alfredQuery
	query["spaceId"] = notionSpaceId
	query["limit"] = 9
	filters = {}
	filters["isDeletedOnly"] = False
	filters["excludeTemplates"] = False
	filters["isNavigableOnly"] = isNavigableOnly
	filters["requireEditPermissions"] = False
	ancestors = []
	filters["ancestors"] = ancestors
	createdBy = []
	filters["createdBy"] = createdBy
	editedBy = []
	filters["editedBy"] = editedBy
	lastEditedTime = []
	filters["lastEditedTime"] = lastEditedTime
	createdTime = []
	filters["createdTime"] = createdTime
	query["filters"] = filters
	query["sort"] = "Relevance"
	query["source"] = "quick_find"
	
	jsonData = json.dumps(query)
	return jsonData

def getNotionUrl( useDesktopClient = None ):
	if (useDesktopClient):
		return "notion://www.notion.so/"
	else:
		return "https://www.notion.so/"

#Get query from Alfred
alfredQuery = str(sys.argv[1])

#Call Notion

headers = {"Content-type": "application/json",
           "Cookie": cookie}
conn = httplib.HTTPSConnection("www.notion.so")
conn.request("POST", "/api/v3/search",
             buildNotionSearchQueryData(alfredQuery), headers)
response = conn.getresponse()
#print response.status, response.reason
data = response.read()
data = data.replace("<gzkNfoUU>", "")
data = data.replace("</gzkNfoUU>", "")

#print data
conn.close()

#Extract search results from notion response
searchResultList = []
searchResults = Payload(data)
for x in searchResults.results:
	searchResultObject = searchResult(x.get('id'))
	if "properties" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value'):
		searchResultObject.title = searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('properties').get('title')[0][0]
	else:
		searchResultObject.title = x.get('highlight').get('text')
	if "pathText" in x.get('highlight'):
		searchResultObject.subtitle = x.get('highlight').get('pathText')
	else: 
		searchResultObject.subtitle = " ";
	if "format" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value'):
		if "page_icon" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('format'):
			searchResultObject.icon = searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('format').get('page_icon')
			searchResultObject.title = searchResultObject.icon + " " + searchResultObject.title 
	searchResultObject.link = getNotionUrl(useDesktopClient) + searchResultObject.id.replace("-", "")
	searchResultList.append(searchResultObject)

itemList = []
for searchResultObject in searchResultList:
	item = {}
	item["uid"] = searchResultObject.id
	item["type"] = "default"
	item["title"] = searchResultObject.title
	item["arg"] = searchResultObject.link
	item["subtitle"] = searchResultObject.subtitle
	#item["autocomplete"] = searchResultObject.title
	itemList.append(item)

items = {}
if not itemList:
	item = {}
	item["uid"] = 1
	item["type"] = "default"
	item["title"] = "No results - go to Notion homepage"
	item["arg"] = getNotionUrl(useDesktopClient)
	itemList.append(item)
items["items"] = itemList
items_json = json.dumps(items)

sys.stdout.write(items_json)