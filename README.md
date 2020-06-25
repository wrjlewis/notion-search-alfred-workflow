# notion-search-alfred-workflow
An Alfred workflow to search Notion.so with instant results

Simply type your keyword into Alfred (default: ns) to see instant search results from Notion that mimic the Quick Find function in the Notion webapp. Selecting a search result takes you to that page in Notion in your default web browser.

** Comes with pre-configured support for [OneUpdater](https://github.com/vitorgalvao/alfred-workflows/tree/master/OneUpdater) for automatic version updates **


![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/31d36ee9e75c343045f2a1f313b03373669a7730/notion-demo.gif)

## Workflow Variables

- `cookie`: Needed for your Notion token. I don't know how long a Notion token lasts but I suspect indefinitely if you use notion regularly.
- `notionSpaceId`: Your organisation identifier. 
- `isNavigableOnly`: Defaults to True. Setting to false allows you to search objects within a page, ie notion objects that cannot be found through the left hand side navigation pane.
- `useDesktopClient`: Defaults to False. Determines whether to open Notion links in the desktop client rather than the web app.
- `enableIcons`: Defaults to True. This toggles support for Notion icons to be shown natively in Alfred search results, for a better design/UX experience. Custom Notion icons are downloaded on demand.

## Obtaining your workflow variables

Visit the Notion webapp and use your browser developer tools to see the network requests being made when you type in anything to the quick find search bar. 

Here you'll see a request called `search`, check the request headers to copy the `cookie` value and check the request payload to copy your `notionSpaceId`.


[![img](https://i.imgur.com/ytewFzE.gif)](https://i.imgur.com/ytewFzE.gif)


### Get your `cookie` headers
They should look something like this 

```
notion_browser_id=1bcfbfb9-e98c-9f03-bfbe-e6f622e98721; logglytrbckingsession=eb1c82cb-fd88-9760-831f-bcc2b1fce01e; bjs_bnonymous_id=%22bdbf1088-b33c-9bdb-b67c-1e2cbbde11eb%22; _fbp=fb.1.1282102012213.1311670027; intercom-id-gpfdrxfd=b61ec62d-2b20-9c9d-8b12-b12736bb8f21; token_v2=b39099...

```

[![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/cookie.png)](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)


### Get your `spaceId`
It should look something like this

```
celcl9aa-c3l7-7504-ca19-0c985e34ll8d
```

[![img](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)](https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png)

### Adding the variables to the Alfred workflows

In the Alfred worfklow in the upper right corner click the `[x]` icon and add the values from above to the corresponding value field

[![img](https://i.imgur.com/Pe6nwey.jpg)](https://i.imgur.com/Pe6nwey.jpg)

## Tips

- If you prefer using the Mac app of Notion, set the `useDesktopClient` environment variable in Alfred to `True`.
- If you experience performance issues or slow searches, you may wish to set `enableIcons` to false. This changes the search results design so icons are in line with the title, it also disables the downloading of any Notion custom icons that you come across whilst searching.

## Download:
https://github.com/wrjlewis/notion-search-alfred-workflow/releases/latest/download/Notion.Search.alfredworkflow

## Forum topics:
https://www.alfredforum.com/topic/14451-notionso-instant-search-workflow/
https://www.reddit.com/r/NotionSo/comments/f58u1y/notionso_instant_search_workflow_for_alfred/
