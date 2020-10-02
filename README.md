This python script will fetch football matches result from goal.com
Just run this script and score will be shown in the output window.

### A live version of this can be accessed in [Heroku](https://goal-com-api.herokuapp.com/live)
---

### Use it as a REST API
A REST API is configured at `code/api.py`

#### API Endpoints
`/live`  
Get a list of competitions and the live matches happening in these competitions

`/fixtures?date=2020-12-31`  
Get a list of matches by the provided date

`/competitions?competition_type=all`  
Get a list of Competitions.

Supported parameters,   
- `competition_type` (*required*)
  - `all` Get list of ALL competitions grouped by Region/League
  - `popular` Get only the Popular competitions (Top 5 leagues)
