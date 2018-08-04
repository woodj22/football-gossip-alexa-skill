# football-gossip-alexa-skill
Scrape the football gossip from BBC sports and present it in Alexa skill JSON.


### What ya need

- serverless framework installed globally (`npm install -g serverless`)

- Docker. This is to build the python packages on a linux distribution ready for the AWS EC2 instance the lambda function will run on.
### Lets get started

#### Start virtualenv

I have included a virtualenv directory with all the python requirements contained within.
To start the environment:

`source venv/bin/activate`

You can then install any python modules within this environment and then add them to the `requirements.txt` so that they can be pased around properly.

#### Install requirements

run `npm install --save serverless-python-requirements`
This installs all the requirements if any changes have been made.


#### Test the code

testing locally:
`serverless invoke local --function gossip -p /mock_requests/get_gossip_request.json`

This will pass the mock json into the events handler of python module. To get the mock json, add a file to the tests folder which contains output of the Alexa skill.


#### Deploy the code

`serverless deploy`
For this to work you must set up the correct AWS user credentials to work with the serverless tool. This user MUST have full admin access to work as it adds to a bucket and deploys the code from their.

