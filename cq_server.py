from flask import Flask, request
from cadquery import cqgi,exporters
import json

#
# a really basic server
# that runs jobs and stores the results
#

app = Flask(__name__)
DATA_HOME="/home/cq/data"
JOB_INDEX="/home/cq/data/job-index.json"

#create a job
#optionally return the result using ?format=<format>&wait=secs
@app.route('/build', method=['POST'])
def post_job():
    job_data = request.get_json()

#fetch the output of a job
@app.route('/build/<int:job_id>')
def get_job():

#get the output for a single object
@app.route('/build/<int:job_id>/objects/<int:obj_id>')
def get_object():



if __name__ == '__main__':
    app.run(host=0.0.0.0,port=8080,debug=True)
