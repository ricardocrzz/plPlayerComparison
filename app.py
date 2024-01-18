from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
from dbConfig import DBCONFIG

app=Flask(__name__)

#configure mysql
db=mysql.connector.connect(**DBCONFIG)
cursor=db.cursor()

#shortcut for interacting with db
def executeQuery(query, params=None):
    cursor.execute(query, params)
    db.commit()

#getting all data from db
def fetchData():
    #theres two dbs rn, get all data and combine it into one string to output
    cursor.execute('select * from players')
    players=cursor.fetchall()

    cursor.execute('select * from wages')
    wages=cursor.fetchall()

    return [(player, wage) for player in players for wage in wages if player[0] == wage[0]]

@app.route('/compare')
def compare():
    totalData=fetchData()

    return render_template('compare.html', data=totalData)


@app.route('/addPlayer', methods=['POST', 'GET'])
def addPlayer():
    if request.method == 'POST':
        playerId = request.form['playerId']
        name = request.form['name']
        teamId = request.form['teamId']
        nation = request.form['nation']
        fieldPos = request.form['fieldPos']
        age = request.form['age']

        #query
        query = 'insert into players (playerId, name, teamId, nation, fieldPos, age) values (%s, %s, %s, %s, %s, %s)'
        params = (player_id, name, team_id, nation, field_pos, age)
        execute_query(query, params)

        return redirect('/')
    else:
        return render_template('addPlayer.html')

@app.route('/addWage', methods=['POST', 'GET'])
def addWage():
    if request.method == 'POST':
        playerId = request.form['playerId']
        annual = request.form['annual']
        transfer = request.form['transfer']
        joined = request.form['joined']

        #query
        query = 'insert into wages (playerId, annual, transfer, joined) values (%s, %s, %s, %s)'
        params = (playerId, annual, transfer, joined)
        execute_query(query, params)

        return redirect('/')
    else:
        return render_template('addPlayer.html')


@app.route('/')
def index():

    totalData=fetchData()

    return render_template('index.html', data=totalData)

if __name__ == '__main__':
    app.run(debug=True)