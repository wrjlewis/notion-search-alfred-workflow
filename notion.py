# coding=utf-8

import httplib
import json
import os
import os.path
import struct
import sys
import urllib
import unicodedata

from payload import Payload
from searchresult import SearchResult

# config
notionSpaceId = os.environ['notionSpaceId']
cookie = os.environ['cookie']

# get useDesktopClient env variable and convert to boolean for use later, default to false
useDesktopClient = os.environ['useDesktopClient']
if (useDesktopClient == 'true') | (useDesktopClient == 'True') | (useDesktopClient == 'TRUE'):
    useDesktopClient = True
else:
    useDesktopClient = False

# get isNavigableOnly env variable and convert to boolean for use later, default to true
isNavigableOnly = os.environ['isNavigableOnly']
if (isNavigableOnly == 'false') | (isNavigableOnly == 'False') | (isNavigableOnly == 'FALSE'):
    isNavigableOnly = False
else:
    isNavigableOnly = True

# get enableIcons env variable and convert to boolean for use later, default to true
enableIcons = os.environ['enableIcons']
if (enableIcons == 'false') | (enableIcons == 'False') | (enableIcons == 'FALSE'):
    enableIcons = False
else:
    enableIcons = True


def buildnotionsearchquerydata():
    query = {}

    query["type"] = "BlocksInSpace"
    query["query"] = unicodeAlfredQuery
    query["spaceId"] = notionSpaceId
    query["limit"] = 9
    filters = {}
    filters["isDeletedOnly"] = False
    filters["excludeTemplates"] = False
    filters["isNavigableOnly"] = isNavigableOnly
    filters["requireEditPermissions"] = False
    ancestors = []
    filters["ancestors"] = ancestors
    createdby = []
    filters["createdBy"] = createdby
    editedby = []
    filters["editedBy"] = editedby
    lasteditedtime = []
    filters["lastEditedTime"] = lasteditedtime
    createdtime = []
    filters["createdTime"] = createdtime
    query["filters"] = filters
    query["sort"] = "Relevance"
    query["source"] = "quick_find"

    jsonData = json.dumps(query)
    return jsonData


def getnotionurl():
    if useDesktopClient:
        return "notion://www.notion.so/"
    else:
        return "https://www.notion.so/"


def decodeemoji(emoji):
    if emoji:
        b = emoji.encode('utf_32_le')
        count = len(b) // 4
        # If count is over 10, we don't have an emoji
        if count > 10:
            return None
        cp = struct.unpack('<%dI' % count, b)
        hexlist = []
        for x in cp:
            hexlist.append(hex(x)[2:])
        return hexlist
    return None


def downloadandgetfilepath(searchresultobjectid, imageurl):
    # create icons dir if it doesn't already exist
    if not os.path.isdir('./icons'):
        path = "./icons"
        access_rights = 0o755
        os.mkdir(path, access_rights)

    downloadurl = "/image/" \
                  + urllib.quote(imageurl.encode('utf8'), safe='') \
                  + "?width=120&cache=v2"
    filetype = downloadurl[downloadurl.rfind('.'):]
    filetype = filetype[:filetype.rfind('?')]
    if '%3F' in filetype:
        filetype = filetype[:filetype.rfind('%3F')]
    filepath = "icons/" + searchresultobjectid + filetype

    headers = {"Cookie": cookie}
    conn = httplib.HTTPSConnection("www.notion.so")
    conn.request("GET", downloadurl, "", headers)
    response = conn.getresponse()
    data = response.read()

    with open(filepath, 'wb') as f:
        f.write(data)
    return filepath


def geticonpath(searchresultobjectid, notionicon):
    iconpath = None

    # is icon an emoji? If so, get hex values and construct the matching image file path in emojiicons/
    hexlist = decodeemoji(notionicon)
    if hexlist:
        emojicodepoints = ""
        count = 0
        for x in hexlist:
            count += 1
            if count > 1:
                emojicodepoints += "_"
            emojicodepoints += x
        iconpath = "emojiicons/" + emojicodepoints + ".png"
        # check if emoji image exists - if not, remove last unicode codepoint and try again
        if not os.path.isfile(iconpath):
            while emojicodepoints.count("_") > 0:
                emojicodepoints = emojicodepoints.rsplit('_', 1)[0]
                iconpath = "emojiicons/" + emojicodepoints + ".png"
                if os.path.isfile(iconpath):
                    break

    else:
        # is icon a web url? If so, download it to icons/
        if "http" in notionicon:
            iconpath = downloadandgetfilepath(searchresultobjectid, notionicon)

    return iconpath


# Get query from Alfred
alfredQuery = str(sys.argv[1])
unicodeAlfredQuery = unicodedata.normalize('NFC', alfredQuery.decode('utf-8', 'ignore'))

# Call Notion

headers = {"Content-type": "application/json",
           "Cookie": cookie}
conn = httplib.HTTPSConnection("www.notion.so")
conn.request("POST", "/api/v3/search",
             buildnotionsearchquerydata(), headers)
response = conn.getresponse()

data = response.read()
data = data.replace("<gzkNfoUU>", "")
data = data.replace("</gzkNfoUU>", "")

conn.close()

# Extract search results from notion response
searchResultList = []
searchResults = Payload(data)
for x in searchResults.results:
    searchResultObject = SearchResult(x.get('id'))
    if "properties" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value'):
        searchResultObject.title = \
            searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('properties').get('title')[
                0][0]
    else:
        searchResultObject.title = x.get('highlight').get('text')
    if "pathText" in x.get('highlight'):
        searchResultObject.subtitle = x.get('highlight').get('pathText')
    else:
        searchResultObject.subtitle = " "
    if "format" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value'):
        if "page_icon" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('format'):
            if enableIcons:
                searchResultObject.icon = geticonpath(searchResultObject.id,
                                                      searchResults.recordMap.get('block').get(searchResultObject.id)
                                                      .get('value').get('format').get('page_icon'))
            else:
                searchResultObject.icon = None
                searchResultObject.title = searchResults.recordMap.get('block').get(searchResultObject.id).get(
                    'value').get('format').get('page_icon') + " " + searchResultObject.title
    searchResultObject.link = getnotionurl() + searchResultObject.id.replace("-", "")
    searchResultList.append(searchResultObject)

itemList = []
for searchResultObject in searchResultList:
    item = {}
    item["uid"] = searchResultObject.id
    item["type"] = "default"
    item["title"] = searchResultObject.title
    item["arg"] = searchResultObject.link
    item["subtitle"] = searchResultObject.subtitle
    if searchResultObject.icon:
        icon = {}
        icon["path"] = searchResultObject.icon
        item["icon"] = icon
    item["autocomplete"] = searchResultObject.title
    itemList.append(item)

items = {}
if not itemList:
    item = {}
    item["uid"] = 1
    item["type"] = "default"
    item["title"] = "No results - go to Notion homepage"
    item["arg"] = getnotionurl()
    itemList.append(item)
items["items"] = itemList
items_json = json.dumps(items)

sys.stdout.write(items_json)
