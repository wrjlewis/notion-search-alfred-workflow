# notion-search-alfred-workflow
An Alfred workflow to search Notion.so with instant results

![img](https://raw.githubusercontent.com/wrjlewis/notion-search-alfred-workflow/master/Screenshot.png)

**Alfred 5 version**

[Github Repository](https://github.com/wrjlewis/notion-search-alfred5-workflow)

[Latest Download](https://github.com/wrjlewis/notion-search-alfred5-workflow/releases/latest/download/Notion.Search.alfredworkflow)

**Alfred 4 version**

[Github Repository](https://github.com/wrjlewis/notion-search-alfred-workflow)

[Latest Download](https://github.com/wrjlewis/notion-search-alfred-workflow/releases/latest/download/Notion.Search.alfredworkflow)

Simply type your keyword into Alfred (default: ns) and provide a query to see instant search results from Notion that mimic the Quick Find function in the Notion webapp. 

Pressing enter on a search result takes you to that page in Notion in your default web browser or notion app.

Hold Cmd + press enter on any search result to copy the url to your clipboard. 

**Additional features**

* Comes with pre-configured support for [OneUpdater](https://github.com/vitorgalvao/alfred-workflows/tree/master/OneUpdater) for automatic version updates.

* The workflow also provides the ability to quickly see your __recently viewed pages__. Simply type the 'ns' keyword to start the workflow, as you would before you search, and your most recently viewed notion pages are displayed. 

* Open a new notion page by typing 'nsn', this only supports the web app currently, it's very handy!

![img](https://raw.githubusercontent.com/wrjlewis/notion-search-alfred5-workflow/main/alfred%20notion%20search.gif)

## Workflow Variables

- `cookie`: Needed for your Notion token.
- `notionSpaceId`: Your organisation identifier.
- `useDesktopClient`: Defaults to False. Determines whether to open Notion links in the desktop client rather than the web app.

It's recommended to leave the following variables to their defaults, unless you're confident: 

- `isNavigableOnly`: Defaults to False. This settings allows you to search objects within a page, ie notion objects that cannot be found through the left hand side navigation pane. Setting to True only returns results that can be found through the left hand side navigation pane, but removes subtitles from Alred search results. 
- `enableIcons`: Defaults to True. This toggles support for Notion icons to be shown natively in Alfred search results, for a better design/UX experience. Custom Notion icons are downloaded on demand.
- `iconCacheDays`: Defaults to the recommended value of 365 days for the best performance. Defines the number of days to cache custom icons. Min 0, max 365.
- `showRecentlyViewedPages`: Defaults to True. This toggle determines if recently viewed pages should be shown when there is no query provided by the user and the user id is present in the supplied cookie (user id is needed for the api call to show recently viewed pages).

## Install Steps
### Install Python3

Many people will have Python3 already on their machine, if you haven't you can try to run `python3` from a Terminal window and it should prompt you to install the Xcode CLI tools automatically (which include Python).

Otherwise you can read a more detailed guide on installing Python [here](https://docs.python-guide.org/starting/install3/osx/). 

### Install cairosvg (optional)

Installing cairosvg will allow svg icons to be shown in Alfred search results, providing a more visually appealing experience. Open terminal and run the following command:

`pip3 install cairosvg`

Install cairosvgs's dependency, cairo. With [Homebrew](https://brew.sh/) for example:

`brew install cairo`

If you haven't used homebrew before, you may want to skip this optional step or install homebrew (easy with a quick google search).

UPDATE: There seems to be an issue with cairosvg on apple silicon, use this fix at your own risk but this worked for me and now SVG icons show again:

```
brew install cairo pango gdk-pixbuf libxml2 libxslt libffi
sudo mkdir /usr/local/lib/
sudo ln -s /opt/homebrew/lib/libcairo-2.dll /usr/local/lib/libcairo-2.dll
sudo ln -s /opt/homebrew/lib/libcairo.so.2 /usr/local/lib/libcairo.so.2
sudo ln -s /opt/homebrew/lib/libcairo.2.dylib /usr/local/lib/libcairo.2.dylib
```

### Get your workflow variables

I recommend using chrome to retrieve these values. If you can only use safari you can copy the 'token_v2' value by following the equivalent steps above and populating the cookie env variable in Alfred so it looks like this `token_v2=XXXXXXXXXXXX` (however this means the recently viewed pages feature will not work for you).

Visit the Notion webapp and use your browser developer tools to see the network requests being made when you type in anything to the quick find search bar. In Chrome select 'View' in the toolbar > Developer > Developer Tools. Then select the Network tab in the developer tools window.

Here you'll see a request called `search`, check the request headers to copy the `cookie` value and check the request payload to copy your `notionSpaceId`, as shown in the screenshots below.

Known issue: Some users have experienced issues with copying these values directly from developer tools, but have seen success by copying and pasting the values into TextEdit or a different text editor first, this probably "strips out" or removes any problematic formatting.

[![img](https://i.imgur.com/ytewFzE.gif)](https://i.imgur.com/ytewFzE.gif)


__Get your `cookie` headers__
They should look something like this 

```
notion_browser_id=1bcfbfb9-e98c-9f03; logglytrbckingsession=eb1c82cb-fd; bjs_bnonymous_id=%22bdbf1088-b33c-9bdb-b67c-1e; _fbp=fb.1.12821; intercom-id-gpfdrxfd=b61ec62d-; token_v2=b39099...

```

[![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/cookie.png)](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)


__Get your `spaceId`__
It should look something like this

```
celcl9aa-c3l7-7504-ca19-0c985e34ll8d
```

[![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)

### Install the Notion Alfred worflow

Download and double click the latest release for your version of Alfred, following the links at the top of this page.

### Add these values to the Notion Alfred workflow

In the Alfred worfklow in the upper right corner click the `[x]` icon and add the values from above to the corresponding value field

[![img](https://i.imgur.com/Pe6nwey.jpg)](https://i.imgur.com/Pe6nwey.jpg)

## Troubleshooting

The script may fail due to an SSL error.  If the script isn't working, turn on debugging by clicking on the little cockroach in the alfred workflow screen.  If you see an error like:

``` [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: ..... ```

Run this from the terminal app:

``` sudo '/Applications/Python 3.9/Install Certificates.command' ```

The single quotes are required.
If this file doesn't exist, run "python --version" to find out what version you have
and update the directory accordingly.

## Tips

- If you prefer using the Mac app of Notion, set the `useDesktopClient` environment variable in Alfred to `True`.
- If you experience performance issues or slow searches, you may wish to set `enableIcons` to false. This changes the search results design so icons are in line with the title, it also disables the downloading of any Notion custom icons that you come across whilst searching. 

## Download:
Follow the links at the top of this page.

## Forum topics:
https://www.alfredforum.com/topic/14451-notionso-instant-search-workflow/
https://www.reddit.com/r/NotionSo/comments/f58u1y/notionso_instant_search_workflow_for_alfred/
