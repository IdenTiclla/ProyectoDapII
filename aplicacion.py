from bottle import get, post, request, route, run, redirect, template, response,static_file
import random

p = {'sesion':[],'nombre':[],'puntajeGeneral':[],"puntajeRonda":[],"dados":[]}

dados = []
ptj = [0]

dado= [0]
turno = [1]

posts = []

insc = [False]



##
@route("/static/<filename>")
def server_static(filename):
    return static_file(filename,root="./css")

@route("/files/<filename>")
def server_filees(filename):
    return static_file(filename,root="./files")

@route("/dados")
def dados():
    return template("dados.html")



##






@route("/")
def index():
    return template("inicio.html")


@route("/control")
def control():
    return template("control.html")


@route("/abrir")
def abrir():
    insc[0] = True
    return template("abrir.html")

@route("/cerrar")
def cerrar():
    insc[0] = False
    return template("cerrar.html")


@route('/inscribir', ["GET","POST"])
def inscribir():
    if request.method == "GET":
        return template("inscribir.html")
    elif request.method == "POST":
        if insc[0]:
            part = request.forms.get('participante')
            if part:
                s = int(random.random() * 1000000)
                p['sesion'].append(s)
                p['nombre'].append(part)
                p["dados"].append([])
                p['puntajeGeneral'].append(0)
                p['puntajeRonda'].append(0)
                setSesion(s)
                print(p)

                #return redirect('/turno')
                return template("success.html")
            else:
                return redirect('/inscribir')
        else:
            return  template("fallo.html")

@route("/salir")
def salir():
    return template("salir.html")



@route('/jugar')
def jugar():
    s = getSesion()
    if s != -1 and s in p['sesion']:
        pos = p['sesion'].index(s)        
        return template('turno.html',part=p['nombre'][pos])
    else:
        return redirect('/inscribir')


@route('/ajax', method='post')
def ajax():
    s = getSesion()
    if s != -1 and s in p['sesion']:
        pos = p['sesion'].index(s)
        if pos == turno[0]:
            return "si es tu turno <a href='/postear'>Juega!</a>"
        else:
            return 'no es tu turno'
        
         
#agregado
@route('/resumen')
def res():

    participantes = p["nombre"]
    puntajeRonda = p['puntajeRonda']
    puntajeGeneral = p["puntajeGeneral"] 
    dados = p["dados"]

    ##
    dado1 = 1
    dado2 = 2
    dado3 = 3
    dado4 = 4
    dado5 = 5
    dado6 = 6


    ##
    return template('resumen.html',dado1=dado1,dado2=dado2,dado3=dado3,dado4=dado4,dado5=dado5,dado6=dado6,n=len(p["nombre"]),participantes=participantes,dados=dados,puntajeRonda=puntajeRonda,puntajeGeneral=puntajeGeneral)
    

#agregado
@route('/resumen',method="post")
def resp():        
    return redirect('/resumen')










    
@route('/postear',["GET","POST"])
def postear():
    if request.method == "GET":
        s = getSesion()
        if s != -1 and s in p['sesion']:
            pos = p['sesion'].index(s)        
            if pos == turno[0]:
                return template('posting.html', nombre= p['nombre'][pos])
            else:
                return redirect('/inscribir')
    elif request.method == "POST":
        s = getSesion()
        if s != -1 and s in p['sesion']:
            pos = p['sesion'].index(s)        
            if pos == turno[0]:
                post = request.forms.get('post')
                posts.append(post)
                turno[0] += 1
                if not turno[0] < len(p['sesion']):
                    turno[0] = 0

                print(p['nombre'][turno[0]])
                
                return redirect('/jugar')
            else:
                return redirect('/inscribir')


@route("/opcion0")
def opcioncero():
    
    s = getSesion()
    pos = p['sesion'].index(s)
    if s != -1 and s in p['sesion']:
        pos = p['sesion'].index(s)        
        if pos == turno[0]:
            if p["puntajeRonda"][pos] >= 6:
                turno[0] += 1
                p["puntajeGeneral"][pos] += p["puntajeRonda"][pos]
                
                #
                if p["puntajeGeneral"][pos] >= 64:
                    turno[0] = -1
                    return template("ganador.html",ganador = p["nombre"][pos],puntaje = p["puntajeGeneral"][pos])

                

                p["dados"][pos] = [] 
                p["puntajeRonda"][pos] = 0
                if not turno[0] < len(p['sesion']):
                    turno[0] = 0 
            elif  p["puntajeRonda"][pos] < 6:
                return template("nosale.html") 
            
  
            print(p['nombre'][turno[0]])
                
            return redirect('/jugar')

@route("/opcion1")
def opcionuno():
    s = getSesion()
    pos = p["sesion"].index(s)
    if s != -1 and s in p['sesion']:
        pos = p["sesion"].index(s)
        if pos == turno[0]:
            dado[0] = int(random.random() * 6) + 1
            if not dado[0] in p["dados"][pos]:
                p["dados"][pos].append(dado[0])
                p["puntajeRonda"][pos] += dado[0]
                return redirect("/postear")
            elif dado[0] in p["dados"][pos]:
                turno[0] += 1
                if not turno[0] < len(p['sesion']):
                    turno[0] = 0
                p["dados"][pos] = [] 
                p["puntajeRonda"][pos] = 0   
                return template("dadorepetido.html",dado = str(dado[0]))

        if len(p["dados"][pos]) >=6:
            return template("ganaste.html")
            


# manejo de sesiones.
def getSesion():
    cookie = request.get_cookie("sesion")
    if not cookie:
        return -1
    return int(cookie)

def setSesion(valor):
    response.set_cookie("sesion", str(valor))    





if __name__ == '__main__':
    run(port = 8080,debug=True,reloader=True, server='waitress')
