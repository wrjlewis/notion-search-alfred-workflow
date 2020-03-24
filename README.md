# notion-search-alfred-workflow
An Alfred workflow to search Notion.so with instant results

Simply type your keyword into Alfred (default: ns) to see instant search results from Notion that mimic the Quick Find function in the Notion webapp. Selecting a search result takes you to that page in Notion in your default web browser.

## Workflow Variables

- `cookie`: Needed for your Notion token. I don't know how long a Notion token lasts but I suspect indefinitely if you use notion regularly.
- `notionSpaceId`: Your organisation identifier. 

## Obtaining your workflow variables

Visit the Notion webapp and use your browser developer tools to see the network requests being made when you type in anything to the quick find search bar.

Here you'll see a request called 'search', check the request headers to copy the `cookie` value and check the request payload to copy your `notionSpaceId`.

https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/cookie.png

https://github.com/wrjlewis/notion-search-alfred-workflow/blob/master/spaceId.png

## Tips

- If you prefer using the Mac app of Notion, just replace `https://www.notion.so` with `notion://www.notion.so/` in the workflow script.

## Download:
https://github.com/wrjlewis/notion-search-alfred-workflow/raw/master/Notion%20Search.alfredworkflow

## Forum topics:
https://www.alfredforum.com/topic/14451-notionso-instant-search-workflow/
https://www.reddit.com/r/NotionSo/comments/f58u1y/notionso_instant_search_workflow_for_alfred/
