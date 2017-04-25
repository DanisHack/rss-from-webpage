## RSS from Webpage

*A simple script to convert a webpage to an RSS feed.*

### How it works

*RSS from Webpage* uses [requests]() to get the source page, 
[BeautifulSoup4]() to grok the document tree and pull out the items, and 
[feedgen]() to create the feed.

You give it a *feed_settings* object specifying the source URL, the output file 
name, the URL it will be published at, the CSS selector for identifying the 
list of articles, the title and author, etc.

### But why

I like RSS, I get a lot of my news via [Feedly](https://www.feedly.com/) Pro.

But you can't always find an RSS feed for the news you like.
Some recalcitrant news sites only  have one giant feed of every single 
article, and don't provide feeds for individual topics or authors.

That's no good. I don't want the firehose. I can't absorb everything from the 
[Sydney Morning Herald](https://www.smh.com.au/), but I ain't gonna miss 
anything written by 
[Annabel Crabb](https://www.smh.com.au/comment/by/Annabel-Crabb-hvecc) who is
grouse.

So I needed this.

When Yahoo Pipes was a thing, it was my tool of choice to get RSS feeds out of
those pages. A visual authoring tool for the 
technically-competent-but-not-a-coder people like me.
But it disappeared a couple of years back. Thanks, Obama.

I know there are new things to do the job: IFTT, Huginn, simple free 
webpage-to-RSS services.

But I used a couple of free ones that fell over. And I needed an excuse to 
learn to code anyway. And hey, web scraping seems like a common starting 
project. So here goes!

### Lots to do

There is still lots to do.
- Rules for extracting articles are hard coded! So it's one feed only.
  - It assumes an **A** anchor link where the HREF is what you want, and the 
    title is what's between the tags. 
  - And it assumes a **P** paragraph with the description.
  - So...even if you changed the source URL, it probably only works on SMH 
    columnists!
- I should ask an actual  Python programmer to review and give suggestions! It 
  Feels like some stuff is weird.
  - Names are the same in different scopes and in function arguments - is that
  normal or is it better to call the instance this_*name* to avoid confusion? 
  What to put in main(). Is it too procedural. etc.
- There's the long list of TODOs in the source. And I need to move those to 
  GitHub issues or JIRA.
- This name is no good!

### Disclaimer

**My first\* real attempt at cutting proper code!**

Beyond playing with [Udacity CS-101]().

*\*I don't count the horrendous VBScript and Windows batch file shenanigans I 
wrote 15 years ago for server/desktop builds.
I guess it was an attempt at "infrastructure as code", a full build from text
files, source locations and environments injected as variables. But eesh, I 
wouldn't want to read it now.*
