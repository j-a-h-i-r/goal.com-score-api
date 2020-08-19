This python script will fetch football matches result from goal.com
Just run this script and score will be shown in the output window.


### Use it as a REST API
A REST API is configured at `code/api.py`

#### Endpoints
`/live`

Get a list of competitions and the live matches happening in these competitions

`/fixture?date=2020-12-31`

Get a list of matches by the provided date

> A live version of this can be accessed in [Heroku](https://goal-com-api.herokuapp.com)
