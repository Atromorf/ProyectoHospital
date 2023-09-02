from asyncio.windows_events import NULL
from contextlib import nullcontext
from distutils.command.config import config
from distutils.log import info
from multiprocessing import connection
from xml.sax.handler import EntityResolver
from click import option
from colorama import Cursor
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, request
from email.policy import default
from flask_mysqldb import MySQL
import jinja2
import pdfkit
import fpdf
import reportlab.pdfgen.canvas
from arrow import utcnow, get
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white
from reportlab.pdfgen import canvas

# inicializar variable para usar flask
app = Flask(__name__)

#configuracion de conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdmedicos'
mysql = MySQL(app)
app.secret_key = 'mysecretkey'

admedico = 0
idmedico = 0
idpaciente = 0

#zona de routing
@app.route('/')
def index():
    global idmedico, admedico
    idmedico = 0
    admedico = 0
    return render_template('index.html')

#zona de routing
@app.route('/login', methods=['GET', 'POST'])
def login():
    #iniciar sesion
   if request.method == 'POST':
        #obtener los datos del formulario
        rfc = request.form['txtRFC']
        password = request.form['txtPassword']
        #comprobar que los datos son correctos
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM medicos WHERE RFC = %s AND Password = %s", [rfc, password])
        
        if result > 0:
            #datos correctos
            cur.execute("SELECT Rol FROM medicos WHERE RFC = %s AND Password = %s", [rfc, password])
            rol = cur.fetchone()
            rol = int(rol[0])
            cur.execute("SELECT ID_Medico FROM medicos WHERE RFC = %s AND Password = %s", [rfc, password])
            idmedico = cur.fetchone()
            global admedico
            admedico = int(idmedico[0])
            if rol == 1:
                flash('Bienvenido al sistema Administrador')
                return redirect(url_for('expedientesA'))
            else:
                flash('Bienvenido al sistema Medico')
                return redirect(url_for('expedientes'))
        else:
            #datos incorrectos
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('index'))

#expedientes de paciente 
@app.route('/expedientes', methods=['GET', 'POST'])
def expedientes():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texpedientes WHERE Medico = %s', [admedico])
    consulta = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('expedientes.html', Medics = consulta)

#expedientes de medico
@app.route('/expedi')
def expedi():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM medicos')
    consul = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('expedientesM.html', Medico = consul)

#datos personales de paciente
@app.route('/Dpersonal')
def Dpersonal():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texploracion WHERE Medico = %s', [admedico])
    consultar = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('Dpersonales.html', Medicose = consultar)

#datos personales de pacientes receta
@app.route('/DpersonalR')
def DpersonalR():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texploracion WHERE Medico = %s', [admedico])
    consultar = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('recetaag.html', Medicose = consultar)

#datos personales de pacientes receta admin
@app.route('/DpersonalRA')
def DpersonalRA():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texploracion WHERE Medico = %s', [admedico])
    consultar = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('recetaagA.html', Medicoses = consultar)

@app.route('/DpersonalA')
def DpersonalA():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texploracion WHERE Medico = %s', [admedico])
    consultar = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('DpersonalesA.html', Medicose = consultar)


@app.route('/Dpersonales')
def Dpersonales():
    
    return render_template('Dpersonales.html')

@app.route('/Buscar')
def Buscar():
    
    return render_template('Buscar.html')

@app.route('/expedientesA')
def expedientesA():
    
    return render_template('expedientesA.html')

@app.route('/agreg')
def agre():
    
    return render_template('agregarP.html')

@app.route('/agregm')
def agrem():
    
    return render_template('agregarM.html')

@app.route('/regres')
def regres():
    
    return render_template('index.html')

@app.route('/recetaag')
def recetaag():
    
    return render_template('recetaag.html')

@app.route('/regresm')
def regresm():
    
    return render_template('DpersonalesA.html')

@app.route('/recag')
def recag():
    
    return render_template('recetaag.html')

@app.route('/regresma')
def regresma():
    
    return render_template('expedientesAa.html')


@app.route('/expedientesAa')
def expedientesAa():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texpedientes WHERE Medico = %s', [admedico])
    consulta = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('expedientesAa.html', Medics = consulta)

@app.route('/Busca' , methods=['GET', 'POST'])
def Busca():
    buscar = request.form['txtBusquedaP']
    buscaf = request.form['txtBusquedaF']
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texpedientes WHERE Paciente=%s OR Fecha_Nacimiento=%s', [buscar, buscaf])
    consulta = cursos.fetchall()
    
    return render_template('Buscar.html', Busca = consulta)

@app.route('/BuscaAP' , methods=['GET', 'POST'])
def BuscaAP():
    busca = request.form['txtBusquedaAP']
    buscf = request.form['txtBusquedaAF']
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texpedientes WHERE Paciente=%s OR Fecha_Nacimiento=%s', [busca, buscf])
    consulta = cursos.fetchall()
    print (consulta)
    
    return render_template('BuscarA.html', Buscar = consulta)

@app.route('/BuscaD' , methods=['GET', 'POST'])
def BuscaD():
    busc = request.form['txtBusquedaD']
    busf = request.form['txtBusquedaDF']
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texploracion WHERE Paciente=%s OR Fecha=%s', [busc, busf])
    consulta = cursos.fetchall()
    print (consulta)
    
    return render_template('BuscarD.html', Buscose = consulta)

@app.route('/BuscaDA' , methods=['GET', 'POST'])
def BuscaDA():
    busc = request.form['txtBusquedaDA']
    busf = request.form['txtBusquedaDAF']
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM texploracion WHERE Paciente=%s OR Fecha=%s', [busc, busf])
    consulta = cursos.fetchall()
    print (consulta)
    
    return render_template('BuscarDA.html', Sear = consulta)

@app.route('/BuscaR' , methods=['GET', 'POST'])
def BuscaR():
    buscarr = request.form['txtBusquedaR']
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM tdiagnostico WHERE Paciente=%s', [buscarr])
    consulta = cursos.fetchall()
    print (consulta)
    
    return render_template('BuscarR.html', Search = consulta)

@app.route('/Buscarra' , methods=['GET', 'POST'])
def Buscarra():
    buscarra = request.form['txtBusquedaRA']
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM tdiagnostico WHERE Paciente=%s', [buscarra])
    consulta = cursos.fetchall()
    print (consulta)
    
    return render_template('Buscarra.html', Sirc = consulta)

@app.route('/receta')
def receta():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM tdiagnostico WHERE Medico = %s', [admedico])
    consulta = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('receta.html', Estudi = consulta)

@app.route('/recetaA')
def recetaA():
    global idpaciente
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT * FROM tdiagnostico WHERE Medico = %s', [admedico])
    consulta = cursos.fetchall()
    idpaciente = [0][0]
    
    return render_template('recetaA.html', Estudio = consulta)

@app.route('/agregarC', methods=['POST'])
def agregarC():

    vnombre = request.form['txtpaciente']
    vdx = request.form['txtdx']
    vsintomas = request.form['txtsintomas']
    vestudio = request.form['txtestudio']
    ctratamiento = request.form['txttratamiento']
    vmedico = request.form['txtmedico']


    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO tdiagnostico(Paciente,Dx,Sintomas,Estudio,Tratamiento,Medico) VALUES(%s,%s,%s,%s,%s,%s)",(vnombre,vdx,vsintomas,vestudio,ctratamiento,vmedico))
    mysql.connection.commit()
        
    flash('Paciente agregado correctamente')
       
    return redirect(url_for('receta'))

@app.route('/agregarP', methods=['POST'])
def agregarP():

    vnombre = request.form['txtnombre']
    vfechan = request.form['txtfechan']
    venfermedades = request.form['txtenfermedades']
    valergias = request.form['txtalergias']
    vantecedentes = request.form['txtantecedentes']
    vmedico = request.form['txtmedico']
    vfechad = request.form['txtfechad']
    valtura = request.form['txtaltura']
    vpeso = request.form['txtpeso']
    vtemperatura = request.form['txttemperatura']
    vlatidos = request.form['txtlatidos']
    voxigeno = request.form['txtoxigeno']
    vdx = request.form['txtdx']
    vsintomas = request.form['txtsintomas']
    vestudio = request.form['txtestudio']
    ctratamiento = request.form['txttratamiento']

       
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO texpedientes(Paciente,Fecha_Nacimiento,Enfermedades,Alergias,Antecedentes,Medico) VALUES(%s,%s,%s,%s,%s,%s)",(vnombre,vfechan,venfermedades,valergias,vantecedentes,vmedico))
    mysql.connection.commit()
    
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO texploracion(Paciente,Fecha,Fecha_Nacimiento,Altura,Peso,Temperatura,Latidos_x_M,Sat_Oxi_Gluc,Medico) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(vnombre,vfechad,vfechan,valtura,vpeso,vtemperatura,vlatidos,voxigeno,vmedico))
    mysql.connection.commit()
    
    cur=mysql.connection.cursor()
    cur.execute("INSERT INTO tdiagnostico(Paciente,Dx,Sintomas,Estudio,Tratamiento,Medico) VALUES(%s,%s,%s,%s,%s,%s)",(vnombre,vdx,vsintomas,vestudio,ctratamiento,vmedico))
    mysql.connection.commit()
        
    flash('Paciente agregado correctamente')
       
    return redirect(url_for('expedientes'))
  
@app.route('/agregarM', methods=['POST'])
def agregarM():

        vnombrem = request.form['txtnombrem']
        vrfc = request.form['txtrfc']
        vcedula = request.form['txtcedula']
        vrol = request.form['txtrol']
        vpass = request.form['txtpassword']
        vcorre = request.form['txtcorreo']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO medicos(Nombre,RFC,Cedula,Rol,Password,Correo) VALUES(%s,%s,%s,%s,%s,%s)",(vnombrem,vrfc,vcedula,vrol,vpass,vcorre))
        mysql.connection.commit()
        
        flash('Medico agregado correctamente')
        return redirect(url_for('expedi'))
    
@app.route('/eliminarP/<string:id>')
def eliminarP(id):
    
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM texpedientes WHERE ID_Paciente={0}".format(id))
    mysql.connection.commit()
    
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM texploracion WHERE ID_Exploracion={0}".format(id))
    mysql.connection.commit()
    
    flash('Paciente eliminado de la base de datos')
    return redirect(url_for('expedientes'))

@app.route('/eliminarR/<string:id>')
def eliminarR(id):
    
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM tdiagnostico WHERE ID_Diagnostico={0}".format(id))
    mysql.connection.commit()
    
    flash('Receta eliminada de la base de datos')
    return redirect(url_for('expedientesM'))

@app.route('/eliminarM/<string:id>')
def eliminarM(id):
    
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM medicos WHERE ID_Medico={0}".format(id))
    mysql.connection.commit()
    
    flash('Doctor eliminado de la base de datos')
    return redirect(url_for('expedi'))

@app.route('/editarP/<string:id>', methods=['POST','GET'])
def get_paciente(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM texpedientes WHERE ID_Paciente = {0}'.format(id))
    data=cur.fetchall()
    
    return render_template('edit.html', medic = data[0])
    

@app.route('/updateP/<string:id>', methods=['POST'])
def update_paciente(id):
    if request.method == 'POST':
        vnombre = request.form['txtnombre']
        vfechan = request.form['txtfechan']
        venfermedades = request.form['txtenfermedades']
        valergias = request.form['txtalergias']
        vantecedentes = request.form['txtantecedentes']
        vmedico = request.form['txtmedico']
        
       
        cur=mysql.connection.cursor()
        cur.execute("UPDATE texpedientes SET Paciente=%s, Fecha_Nacimiento=%s, Enfermedades=%s, Alergias=%s, Antecedentes=%s, Medico=%s WHERE ID_Paciente=%s",(vnombre,vfechan,venfermedades,valergias,vantecedentes,vmedico,id))
        cur.execute("UPDATE texploracion SET Paciente=%s, Fecha_Nacimiento=%s WHERE ID_Exploracion=%s",(vnombre,vfechan,id))
        cur.execute("UPDATE tdiagnostico SET Paciente=%s WHERE ID_Diagnostico=%s",(vnombre,id))
        mysql.connection.commit()
        
        flash('Paciente actualizado')
        
        return redirect(url_for('expedientes'))
    
@app.route('/editarD/<string:id>', methods=['POST','GET'])
def get_datos(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM texploracion WHERE ID_Exploracion = {0}'.format(id))
    data=cur.fetchall()
    
    return render_template('editD.html', med = data[0])

@app.route('/updateD/<string:id>', methods=['POST'])
def update_datos(id):
    if request.method == 'POST':
        vfechad = request.form['txtfechad']
        valtura = request.form['txtaltura']
        vpeso = request.form['txtpeso']
        vtemperatura = request.form['txttemperatura']
        vlatidos = request.form['txtlatidos']
        voxigeno = request.form['txtoxigeno']
        
       
        cur=mysql.connection.cursor()
        cur.execute("UPDATE texploracion SET Fecha=%s, Altura=%s, Peso=%s, Temperatura=%s, Latidos_x_M=%s, Sat_Oxi_Gluc WHERE ID_Exploracion=%s",(vfechad,valtura,vpeso,vtemperatura,vlatidos,voxigeno,id))
        mysql.connection.commit()
        
        
        flash('Paciente actualizado')
        
        return redirect(url_for('Dpersonales'))
    
@app.route('/editarM/<string:id>', methods=['POST','GET'])
def get_medico(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM medicos WHERE ID_Medico = {0}'.format(id))
    data=cur.fetchall()
    return render_template('editM.html', medi = data[0])
    

@app.route('/updateM/<string:id>', methods=['POST'])
def update_medico(id):
    if request.method == 'POST':
        vnombrem = request.form['txtnombrem']
        vrfc = request.form['txtrfc']
        vcedula = request.form['txtcedula']
        vrol = request.form['txtrol']
        vcorre = request.form['txtcorreo']
       
        cur=mysql.connection.cursor()
        cur.execute("UPDATE medicos SET Nombre=%s, RFC=%s, Cedula=%s, Rol=%s, Correo=%s WHERE ID_Medico=%s",(vnombrem,vrfc,vcedula,vrol,vcorre,id))
        mysql.connection.commit()
        
        flash('Medico actualizado')
        
        return redirect(url_for('expedi'))

@app.route('/imp/<string:id>', methods=['POST','GET'])
def imp(id):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch
    w, h = A4
    global admedico
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT Nombre FROM medicos WHERE ID_Medico = %s', [admedico])
    medic = cursos.fetchall()
    medico = medic[0][0]
    cursos = mysql.connection.cursor()
    cursos.execute('SELECT Paciente,Dx,Sintomas,Estudio,Tratamiento,Medico FROM tdiagnostico WHERE ID_Diagnostico = %s', [id])
    pacientes = cursos.fetchall()
    paciente = pacientes[0][0]
    dx = pacientes[0][1]
    sint = pacientes[0][2]
    est = pacientes[0][3]
    trat = pacientes[0][4]
    c = canvas.Canvas("Paciente.pdf", pagesize=A4)
    c.drawString(30, h - 50, "Datos del Paciente: ")
    x = 120
    y = h - 45
    c.drawString(30, h - 100, "Paciente: " + paciente)
    c.drawString(30, h - 250, "Diagnostico: " + dx)
    c.drawString(30, h - 300, "Sintomas: " + sint)
    c.drawString(30, h - 350, "Estudio: " + est)
    c.drawString(30, h - 400, "Tratamiento: " + trat)
    c.drawString(30, h - 450, "Medico: " + medico)
    c.showPage()
    c.save()
    flash('Documento creado')
    return redirect(url_for('receta')) 

@app.route('/medi')
def medi():
    #sql para ver medicos
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM medicos')
    medicos = cur.fetchall()
    return render_template('medicos.html', medicos = medicos)

# arrancamos servidor
if __name__ == '__main__' :
    app.run(port = 3000, debug = True)