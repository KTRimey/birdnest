# birdnest report

## A web application for monitoring recent violators of the Monadikuikka NDZ -- [PROJECT BIRDNEST](https://assignments.reaktor.com/birdnest/)

"A rare and endangered Monadikuikka has been spotted nesting at a local lake.

Unfortunately some enthusiasts have been a little too curious about this elusive bird species, flying their drones very close to the nest for rare photos and bothering the birds in the process."

<p align="center">
    <img src="react-app/public/DALLE.png" alt="DAllE generated image of bird and droid" height="300"/>
</p>

birdnest report includes a Flask server which queries the monitoring equipment of the Monadikuikka nest and the national drone registry, and a React app which displays the information on pilots who have recently violated the NDZ perimeter, including their contact information and closest approach.

The information on violators is persisted for 10 minutes since the drone was last seen the monitoring equipment. For privacy concerns, only pilot information for drones violating the NDZ is queried.

#### You can test birdnest report out for yourself!

###### Installation:

It is a good idea to run birdnest in a virtual environment. Set this up with the required dependencies with the following commands.

`python3 -m venv venv`<br />
`. venv/bin/activate`<br />
`pip install -r requirements.txt`<br />
`npm install` in react-app directory

###### Running:

`python init_db.py` to create the SQLite database and table, you only need to do this once<br />
`python updater.py` to launch updater<br />
`flask run`<br />
`npm start` in react-app directory

To access database, try:
`sqlite3 database.db` and, e.g. `SELECT * FROM drone;`
