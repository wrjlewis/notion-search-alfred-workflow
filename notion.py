import http.client
import json
import os
import os.path
import struct
import sys
import unicodedata
import time
import urllib.parse, urllib.error
from urllib.request import Request, urlopen
from http.cookies import SimpleCookie

cairosvgInstalled = False
try:
    from cairosvg import svg2png
    cairosvgInstalled = True
except: 
    pass

from payload import Payload
from searchresult import SearchResult

# config
notionSpaceId = os.environ['notionSpaceId']
cookie = os.environ['cookie']

# convert cookie string to dict for later use
bakedCookie = SimpleCookie()
bakedCookie.load(cookie)
# even though SimpleCookie is dictionary-like, it internally uses a Morsel object
# Manually construct a dictionary instead.
bakedCookies = {}
for key, morsel in bakedCookie.items():
    bakedCookies[key] = morsel.value

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

# get the number of days to cache custom icons. Min 0, max 365. Defaults to the maximum of 365 days
iconCacheDays = sorted([0, int(os.environ['iconCacheDays']), 365])[1]

# get showRecentlyViewedPages env variable and convert to boolean for use later, default to true
showRecentlyViewedPages = os.environ['showRecentlyViewedPages']
if (showRecentlyViewedPages == 'false') | (showRecentlyViewedPages == 'False') | (showRecentlyViewedPages == 'FALSE'):
    showRecentlyViewedPages = False
else:
    showRecentlyViewedPages = True

exception = ""

def buildnotionsearchquerydata():
    query = {}

    query["type"] = "BlocksInSpace"
    query["query"] = alfredQuery
    query["spaceId"] = notionSpaceId
    query["limit"] = 9
    filters = {}
    filters["isDeletedOnly"] = False
    filters["excludeTemplates"] = False
    filters["isNavigableOnly"] = isNavigableOnly
    filters["navigableBlockContentOnly"] = isNavigableOnly
    filters["requireEditPermissions"] = False
    ancestors = []
    filters["ancestors"] = ancestors
    createdby = []
    filters["createdBy"] = createdby
    editedby = []
    filters["editedBy"] = editedby
    lasteditedtime = {}
    filters["lastEditedTime"] = lasteditedtime
    createdtime = {}
    filters["createdTime"] = createdtime
    query["filters"] = filters
    query["sort"] = "Relevance"
    query["source"] = "quick_find_input_change"

    jsonData = json.dumps(query)
    return jsonData

def buildnotionrecentpagevisitsquery(userId):
    query = {}

    query["userId"] = userId
    query["spaceId"] = notionSpaceId
    query["limit"] = 9

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
    
    # has a full icon url been provided, if not construct it
    if ("https://www.notion.so" in imageurl):
        downloadurl = imageurl.split("https://www.notion.so",1)[1]
    else:
        downloadurl = "/image/" \
                    + urllib.parse.quote(imageurl.encode('utf8'), safe='') \
                    + "?table=block&id=" \
                    + searchresultobjectid \
                    + "&width=120&cache=v2"
    
    # construct filepath consisting of workspace id + filename 
    filepath = downloadurl[downloadurl.rfind('%2F') + 3:]
    filepath = filepath[:filepath.rfind('?')]
    if '%3F' in filepath:
        filepath = filepath[:filepath.rfind('%3F')]
    filepath = "icons/" + searchresultobjectid + "_" + filepath

    # figure out the filetype for later
    filetype = filepath[filepath.rfind('.') + 1:]

    # check if the file already exists and if so don't download again, according to cache settings
    if (os.path.isfile(filepath)):
        now = time.time()
        timeIconModified = os.path.getmtime(filepath)
        if ((now - timeIconModified) < (float(iconCacheDays) * 86400)):
            # if its a svg file, return the converted png filepath instead
            if (filetype == "svg"):
                svgfilepath = filepath[:-3] + "png"
                if (not os.path.isfile(svgfilepath)):
                    # if the converted png file doesn't exist yet, create it
                    return convertsvgtopng(filepath)
                filepath = svgfilepath
            return filepath

    headers = {"Cookie": cookie}
    conn = http.client.HTTPSConnection("www.notion.so")
    conn.request("GET", downloadurl, "", headers)
    response = conn.getresponse()
    data = response.read()

    with open(filepath, 'wb') as f:
        f.write(data)

    # if svg, convert to png. Check if cariosvg is installed first
    if (filetype == "svg"):
        filepath = convertsvgtopng(filepath)

    return filepath

def convertsvgtopng(filepath):
    if (cairosvgInstalled):
            pngfilepath = filepath[:-3] + "png"
            svg2png(url=filepath, write_to=pngfilepath)
            return pngfilepath
    else:
        return None


def geticonpath(searchresultobjectid, notionicon):
    iconpath = None
    svg = False

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
        # is icon a web url or svg icon? If so, download it to icons/
        if (notionicon[0:7] == "/icons/"):
            notionicon = "https://www.notion.so/image/https%3A%2F%2Fwww.notion.so%2Ficons%2F" + notionicon[7:] + "?"
        if "http" in notionicon:
            iconpath = downloadandgetfilepath(searchresultobjectid, notionicon)

    return iconpath

def createSubtitleChain(recordMap, id):
    stack = []
    parent_table = recordMap.get('block').get(id).get('value').get('parent_table')
    id = recordMap.get('block').get(id).get('value').get('parent_id')    
    for x in range(10):
        if (parent_table == "block"):
            try:
                stack.append(recordMap.get('block').get(id).get('value').get('properties').get('title')[0][0])
            except:
                pass
            parent_table = recordMap.get('block').get(id).get('value').get('parent_table')
            id = recordMap.get('block').get(id).get('value').get('parent_id')
        if (parent_table == "collection"):
            try:
                stack.append(recordMap.get('collection').get(id).get('value').get('name')[0][0])
            except:
                pass
            parent_table = recordMap.get('collection').get(id).get('value').get('parent_table')
            id = recordMap.get('collection').get(id).get('value').get('parent_id')
        if (parent_table == "space"):
            break

    subtitle = ""
    while (len(stack) > 0):
        subtitle = subtitle + str(stack.pop()) + " / "
    if (subtitle != ""):
        subtitle = subtitle[:-2]

    return subtitle

# Get query from Alfred
alfredQuery = str(sys.argv[1])
alfredQuery = unicodedata.normalize('NFC',alfredQuery)

searchResultList = []
# If no query is provided and we're able to get the userId from the cookie env variable, show recently viewed notion pages.
# Else show notion search results for the query given
if not (alfredQuery and alfredQuery.strip()): 
    try:
        if ("notion_user_id" in bakedCookies and showRecentlyViewedPages):
            headers = {"Content-type": "application/json",
                    "Cookie": cookie}
            conn = http.client.HTTPSConnection("www.notion.so")
            conn.request("POST", "/api/v3/getRecentPageVisits",
                        buildnotionrecentpagevisitsquery(bakedCookies.get("notion_user_id")), headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()

            # Extract search results from notion recent page visits response
            searchResults = Payload(data)
            for x in searchResults.pages:
                searchResultObject = SearchResult(x.get('id'))
                searchResultObject.title = x.get('name')
                searchResultObject.subtitle = createSubtitleChain(searchResults.recordMap, searchResultObject.id)
                searchResultObject.icon = None
                if enableIcons:
                    #check if there is an icon emoji or a fullIconUrl for the search result
                    if "iconEmoji" in x:
                        searchResultObject.icon = geticonpath(searchResultObject.id, x.get('iconEmoji'))
                    if "fullIconUrl" in x:
                        searchResultObject.icon = geticonpath(searchResultObject.id, x.get('fullIconUrl'))            
                
                searchResultObject.link = getnotionurl() + searchResultObject.id.replace("-", "")
                searchResultList.append(searchResultObject)
    except Exception as e: 
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        exception = str(line) + ": " + str(e)
else:
    try:
        headers = {"Content-type": "application/json",
            "Cookie": cookie}
        conn = http.client.HTTPSConnection("www.notion.so")
        conn.request("POST", "/api/v3/search",
                    buildnotionsearchquerydata(), headers)
        response = conn.getresponse()
        data = response.read()

        #Convert to string and replace
        data = data.decode("utf-8")
        dataStr = json.dumps(data).replace("<gzkNfoUU>", "")
        dataStr = dataStr.replace("</gzkNfoUU>", "")
        #Get obj back with replacement
        data = json.loads(dataStr)   
        conn.close()

    # Extract search results from notion search response
        searchResults = Payload(data)
        for x in searchResults.results:
            searchResultObject = SearchResult(x.get('id'))
            if "collection_id" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value'):
                collection_id = searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('collection_id')
                searchResultObject.title = searchResults.recordMap.get('collection').get(collection_id).get('value').get('name')[0][0]
            else:
                if "properties" in searchResults.recordMap.get('block').get(searchResultObject.id).get('value'):
                    searchResultObject.title = \
                        searchResults.recordMap.get('block').get(searchResultObject.id).get('value').get('properties').get('title')[0][0]
                else:
                    searchResultObject.title = x.get('highlight').get('text')
            searchResultObject.subtitle = createSubtitleChain(searchResults.recordMap, searchResultObject.id)
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
    except Exception as e: 
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        exception = str(line) + ": " + str(e)

itemList = []
for searchResultObject in searchResultList:
    item = {}
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

if exception:
    item = {}
    item["uid"] = 1
    item["type"] = "default"
    item["title"] = "There was an error:"
    item["subtitle"] = str(exception)
    item["arg"] = getnotionurl()
    itemList.append(item)

if not itemList:
    item = {}
    item["uid"] = 1
    item["type"] = "default"
    item["title"] = "Open Notion - No results, empty query, or error"
    item["subtitle"] = " "
    item["arg"] = getnotionurl()
    itemList.append(item)

items = {}
items["items"] = itemList
items_json = json.dumps(items)
sys.stdout.write(items_json)
