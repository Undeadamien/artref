# artref

artref is a Python tool to search and download image references from online APIs.

## Install / Setup

Install the cli globally using `pipx`

```
pipx ensurepath
pipx install .
```

## Usage

**CLI**

> Check the query syntax in the docs for each source

```
artref wallhaven "guweiz"
artref scryfall "art:magalie"
```

**API**

> Not yet implemented

## Todo

**General:**

- [ ] Implement the API with FastAPI
- [ ] Document the CLI part
- [ ] Add more logging

**Sources:**

- [x] Wallhaven support
- [ ] Scryfall support
  - [ ] Handle the different card layout
- [ ] Unsplash support

## Resources

Scryfall: https://scryfall.com/docs/api  
Unsplash: https://unsplash.com/documentation  
WallHaven: https://wallhaven.cc/help/api
