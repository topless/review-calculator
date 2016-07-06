## Review Calculator

Arguments for our calculator are provided as a dictionary, `{"domain": "google.com"}`


### Deployed calculation
Endpoint: **[https://ugntdo49t1.execute-api.eu-central-1.amazonaws.com/prod](https://ugntdo49t1.execute-api.eu-central-1.amazonaws.com/prod)**

You can try the calculator by firing a `PUT` request to the
deployed api, the desired domain as parameter.

`curl -H "Content-Type: application/json" -X PUT -d '{"domain": "microsoft.com"}' https://ugntdo49t1.execute-api.eu-central-1.amazonaws.com/prod`


### Local usage
For development purposes we can trigger the script locally.
Invoke the script and pass as string argument the domain you want to calculate
the reviews for.

`python main.py facebook.com`


### Aging algorithm
A very simple weighted mean value is used for our calculations.
We consider the oldest review with weight 1 and we use the difference in days
from it, to calculate the weight of each latest review.

Clarification, it states in the requirements **Only use the 300 first ratings.**
We consider first 300 ratings from first review and on. Still the solution can be adjusted by changing the `MAX_RESULTS` number.


### Observations
- There is an error in the page title for [API developer challenge](http://followthewhiterabbit.trustpilot.com/api/challenge.html), it looks its inherited from the backend challenge.
- It took me 7 minutes and 26 seconds, to memorize the api key, and repeat it 10 times without a mistake.
