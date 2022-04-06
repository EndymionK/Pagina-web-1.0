from statistics import correlation
from flask import Flask, url_for
from flask import render_template, request, redirect, flash
from flaskext.mysql import MySQL

app= Flask(__name__)
app.secret_key = "Develoteca"

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema'
mysql.init_app(app)


@app.route('/')
def index():

    sql = "SELECT * FROM `estudiantes`;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    estudiantes=cursor.fetchall()
    print(estudiantes)

    conn.commit()
    return render_template('estudiantes/index.html', estudiantes=estudiantes)

@app.route('/create')
def create():
    
    return render_template('estudiantes/create.html')

@app.route('/store', methods=['POST'])
def storage():

    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _facultad=request.form['txtFacultad']
    

    if _nombre=='' or _correo=='' or _facultad=='':
        flash('Debes llenar todos los datos requeridos')
        return redirect(url_for('create'))

    
    sql = "INSERT INTO `estudiantes` (`id`, `nombre`, `correo`, `facultad`, `faltas`) VALUES (NULL, %s, %s, %s, %s);"
    
    datos=(_nombre,_correo,_facultad)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('estudiantes/index.html')

@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM estudiantes WHERE id=%s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM estudiantes WHERE id=%s", (id))

    estudiantes=cursor.fetchall()
    conn.commit()

    return render_template('estudiantes/edit.html', estudiantes=estudiantes)

@app.route('/update', methods=['POST'])
def update():

    _nombre=request.form['txtNombre']
    _correo=request.form['txtCorreo']
    _facultad=request.form['txtFacultad']
    id=request.form['txtID']

    sql = "UPDATE estudiantes SET nombre= %s, correo=  %s, facultad=  %s WHERE id= %s ;"
    
    datos=(_nombre,_correo,_facultad,id)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')


if __name__=='__main__':
    app.run(debug=True)