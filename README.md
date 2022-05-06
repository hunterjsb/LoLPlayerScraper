openJosh
=================
-------------------------
Official API of the LCS
-------------------------

Introduction
============

We are a team of elite gamers dedicated to bringing you the world's premier LoL data source. The openJosh team has
over 200+ years of collective experience which is why we are able to maintain the world's only open-source pro LOL API.

Endpoints
----------

We currently offer **three** endpoints.
All endpoints are **CASE SENSITIVE**!

- /api/get_player/<name>
- /api/get_team/<team>
- /api/teams_by_region/<region> [DISABLED]

Examples
----------

```python
import requests

# returns a dictionary with player attributes
requests.get('www.domain.com/api/get_player/Broken_Blade')

# returns a dictionary with team attributes
requests.get('www.domain.com/api/get_player/GGS')
```