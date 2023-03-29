openJosh
=================
Official API of the LCS

Introduction
----------

We are a team of elite devs dedicated to bringing you an open-source LoL data API.

Endpoints
----------

We currently offer **three** endpoints.
All endpoints are **CASE SENSITIVE**!

- /api/get_player/<name>
- /api/get_team/<team>
- /api/teams_by_region/<region> [DISABLED]

Examples
----------
  
```bash
  pip install requests
```
```python
import requests

# returns a dictionary with player attributes
requests.get('www.domain.com/api/get_player/Broken_Blade')

# returns a dictionary with team attributes
requests.get('www.domain.com/api/get_team/GGS')
```
