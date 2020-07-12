import os
import sqlite3
import datetime
from flask import Flask,render_template,request,redirect,url_for,send_from_directory,session
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SECRET_KEY']=os.urandom(24)
csrf=CSRFProtect(app)


def show_entries(input):
    con = sqlite3.connect('todo.db')
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS message(data_id,msg,date_time)")
    result = con.execute("SELECT * FROM message ORDER BY data_id DESC")
    alert = input
    return render_template('index.html',result=result,alert=alert)



@app.route('/')
def index_show():
    output = show_entries('')
    return output



@app.route('/',methods=['GET','POST'])
def send():
    
    if request.method == 'POST':
        msg = request.form['msg']
        if not msg:
            output = show_entries('WARNING : If you want to create new ToDo,Please enter something')
            return output
        else:
            date_time = datetime.datetime.today()
            data_id = date_time.strftime("%Y%m%dH%M%S")
            con = sqlite3.connect('todo.db')
            c = con.cursor()
            c.execute("INSERT INTO message VALUES (?,?,?)",(data_id,msg,date_time))
            con.commit()
            result = con.execute("SELECT * FROM message ORDER BY data_id DESC")

            return render_template('index.html',result=result)


@app.route('/delete_data',methods=['GET','POST'])
def delete_data():
    if request.method == 'POST':
        data_ids = request.form.get('action')
        if not data_ids:
            output = show_entries('WARNING : If you want to delete some ToDo,you have to select some checkboxes.')
            return output
        else:
            con = sqlite3.connect('todo.db')
            c = con.cursor()
            query = "DELETE FROM message WHERE data_id=?"
            c.execute(query,(data_ids,))
            con.commit()
            result = con.execute("SELECT * FROM message ORDER BY data_id DESC")
    
            return render_template('index.html',result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()
