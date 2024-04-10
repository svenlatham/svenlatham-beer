# svenlatham-beer
Dedicated beer repo

## Why does it exist?
This is an experimental project to test out different ways of serving content,
via GitHub Pages, Jekyll, Docker and other methods.

It's also a way for me to make notes about my favourite Belgian-style beers.

## How does it work?
At the moment I'm using a simple Python web server (Flask) to generate a series of pages.
I then use `wget` to scrape those pages into a static folder. This is
then uploaded to GitHub Pages.
The developer can choose to run the Docker image directly, which serves a local webserver with real-time changes enabled.

## Why not use Jekyll?
I've had a few problems with Jekyll in the past, from seemingly countless vulnerability notifications, to a fairly heavy build process. I'm aiming for a lighter solution.

## Where is it published?
Repo is at https://github.com/svenlatham/svenlatham-beer

Output is at https://beer.svenlatham.com/

Cheers!

