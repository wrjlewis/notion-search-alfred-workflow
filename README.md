# notion-search-alfred-workflow
An Alfred workflow to search Notion.so with instant results

Simply type your keyword into Alfred (default: ns) to see instant search results from Notion that mimic the Quick Find function in the Notion webapp. Selecting a search result takes you to that page in Notion in your default web browser.

Comes with pre-configured support for [OneUpdater](https://github.com/vitorgalvao/alfred-workflows/tree/master/OneUpdater) for automatic version updates.

Includes the ability to quickly see your recently viewed pages which are shown when triggering the workflow. Simply type the 'ns' keyword to start the workflow, as you would before you search, and your most recently viewed notion pages are displayed. There is env variable to toggle this feature if you'd like to turn this off (detailed below).

![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/31d36ee9e75c343045f2a1f313b03373669a7730/notion-demo.gif)

## User Configuration

- `Cookie`: Needed for your Notion token. I don't know how long a Notion token lasts but I suspect indefinitely if you use notion regularly.
- `Space ID`: Your organisation identifier.
- `Navigable Only`: Defaults to True. Setting to false allows you to search objects within a page, ie notion objects that cannot be found through the left hand side navigation pane.
- `Use Desktop Client`: Defaults to False. Determines whether to open Notion links in the desktop client rather than the web app.
- `Enable Icons`: Defaults to True. This toggles support for Notion icons to be shown natively in Alfred search results, for a better design/UX experience. Custom Notion icons are downloaded on demand.
- `Show Recently Viewed`: Defaults to True. This toggle determines if recently viewed pages should be shown when there is no query provided by the user and the user id is present in the supplied cookie (user id is needed for the api call to show recently viewed pages).

## Obtaining your user configuration

> **Note**: Using the webapp is important, the Mac OS app for example will hide the cookies.

Visit the Notion webapp and use your browser developer tools to see the network requests being made when you type in anything to the quick find search bar.

Here you'll see a request called `search`, check the request headers to copy the `cookie` value and check the request payload to copy your `notionSpaceId`.

Known issue: Some users have experienced issues with copying these values directly from developer tools, but have seen success by copying and pasting the values into TextEdit or a different text editor first, this probably "strips out" or removes any problematic formatting.

[![img](https://i.imgur.com/ytewFzE.gif)](https://i.imgur.com/ytewFzE.gif)


### Get your `cookie` headers
They should look something like this

```
notion_browser_id=1bcfbfb9-e98c-9f03; logglytrbckingsession=eb1c82cb-fd; bjs_bnonymous_id=%22bdbf1088-b33c-9bdb-b67c-1e; _fbp=fb.1.12821; intercom-id-gpfdrxfd=b61ec62d-; token_v2=b39099...

```

[![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/cookie.png)](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)


### Get your `spaceId`
It should look something like this

```
celcl9aa-c3l7-7504-ca19-0c985e34ll8d
```

I recommend using chrome to retrieve these values. If you can only use safari you can copy the 'token_v2' value by following the equivalent steps above and populating the cookie env variable in Alfred so it looks like this `token_v2=XXXXXXXXXXXX`.

## Tips

- If you prefer using the Mac app of Notion, set the `useDesktopClient` environment variable in Alfred to `True`.
- If you experience performance issues or slow searches, you may wish to set `enableIcons` to false. This changes the search results design so icons are in line with the title, it also disables the downloading of any Notion custom icons that you come across whilst searching.

## Download:
https://github.com/wrjlewis/notion-search-alfred-workflow/releases/latest/download/Notion.Search.alfredworkflow

## Forum topics:
https://www.alfredforum.com/topic/14451-notionso-instant-search-workflow/
https://www.reddit.com/r/NotionSo/comments/f58u1y/notionso_instant_search_workflow_for_alfred/
