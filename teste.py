from flask import Flask, render_template, request, redirect, url_for, session
import templates.Server as Server

app = Flask(__name__)#ISSO AQUI INICIA O FLASK#
app.secret_key = 'pedrao'
#Criando a 1 pag#

    #route -> rota dentro da pag q isso mostra
    #funcao -> oq vai mostrar no site

@app.route("/", methods =["GET", "POST"]) #isso define a roa como a homepage
def login():
    varteste = session.get('varteste', None)


    if request.method == "POST":
        email = request.form.get("email")
        session["email"] = email
        senha = request.form.get("senha")
        login = ("""
        SELECT senha FROM users WHERE usermail = '{}'
        """).format(email)

        conlogin = ("""
        SELECT usermail FROM users WHERE usermail = '{}'
        """).format(email)

        connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")
        exc = Server.read_query(connection, login)
        readmail = Server.read_query(connection, conlogin)

        exc = str(exc)
        senha  = ("[('{}',)]".format(senha))
        senha = str(senha)

        if readmail != []:
            if exc == senha or senha == exc:
                readperm = ("""
                SELECT perm FROM users WHERE usermail = '{}'
                """).format(email)

                perm = Server.read_query(connection, readperm)

                perm = str(perm)

                readnome = ("""
                SELECT name FROM users WHERE usermail = '{}'
                """).format(email)
                name = Server.read_query(connection, readnome)
                name = str(name)[:-4][3:]
                session['name'] = name
                print(readperm)
                if perm == "[(2,)]":
                    session['varteste'] = "dono"
                if perm == "[(1,)]":
                    session['varteste'] = "med"
                if perm == "[(0,)]":
                    session['varteste'] = "pac"
                cara = session['varteste']
                print(cara)


                return ("""<script>
                window.location.assign("/homepage")
                </script>
                """).format(cara, perm)
            else:
                return ("""<script>
                alert('A senha inserida esta incorreta');
                window.location.assign("/")
                </script>
                """)
        else:
            return ("""<script>
                alert('O email inserido está incorreto');
                window.location.assign("/")
                </script>
                """).format(readmail)
            
    return render_template("login.html")




@app.route("/cadastro", methods =["GET", "POST"])
def cadastro():
    varteste = session.get('varteste', None)
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        consenha = request.form.get("consenha")
        username = request.form.get("username")
        sexo = request.form.get("sexo")
        tel = request.form.get("telefone")
        nasc = request.form.get("data_nascimento")
        print(sexo)
        print("aqui"+email+"aqui")
        readdata = """
        SELECT usermail FROM users
        """

        connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")
        read = Server.read_query(connection, readdata)

        teste = """
        (SELECT * FROM users WHERE usermail = '{}')
        UNION
        (SELECT * FROM users WHERE name = '{}')
        """.format(email, username)

        exec2 = Server.read_query(connection, teste)

        if (email == '' or senha == '' or sexo == '---' or username == ''):
            return ("""<script>
                alert('Por favor Preencha todos os campos corretamente corretamente');
                window.location.assign("/cadastro")
                </script>""")
        else:
            
            if exec2 == []:
                if consenha == senha:
                    
                    caduser = ("""
                    INSERT INTO users (Iduser, usermail, name, senha, Sexo, nasc, tel, perm) VALUES
                    (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '0')
                    """).format(email, username, senha, sexo, nasc, tel)
                    create = ("""
                    CREATE TABLE `{}` (
                    id_evento int NOT NULL AUTO_INCREMENT,
                    nome_evento VARCHAR(50) NOT NULL,
                    detalhe_evento VARCHAR(255),
                    data_evento DATE NOT NULL,
                    hora_evento varchar(8) NOT NULL,
                    med VARCHAR(45) NOT NULL,
                    PRIMARY KEY (id_evento))
                    """).format(email)
                    

                    exec = Server.execute_query(connection, caduser)
                    exec1 = Server.execute_query(connection, create)
                    return ("""<script>
                    alert('Conta cadastrada com sucesso')
                    window.location.assign("/")
                    </script>
                    """)

                else:
                    return ("""<script>
                    alert('As senha inseridas não coincidem');
                    window.location.assign("/cadastro")
                    </script>
                    """)
            else:
                return ("""<script>
                alert('Email ou Nome ja cadastrados');
                window.location.assign("/cadastro")
                </script>
                """)
        

    return render_template("cadastro.html")



@app.route("/homepage", methods =["GET", "POST"])
def home():
    varteste = session.get('varteste', None)
    session['varpralogin'] = varteste
    email = session.get('email', None)
    name = session.get('name', None)

    connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")
    readsexo = ("""
    SELECT Sexo FROM users WHERE usermail = '{}' 
    """).format(email)
    sexo = Server.read_query(connection, readsexo)
    sexo = str(sexo)
    if sexo == "[('M',)]" or sexo == "[('O',)]" :
        sexo = ""
    else:
        sexo = "a"

    c = 0
    if varteste == "pac":
        if request.method == "POST":
            data = request.form.get("datahoje")
            data_ano = data[:-6]
            data_mes = data[:-3][5:]
            data_dia = data[8:]
            data_br = (data_dia+"/"+data_mes)
            connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")

            readsexo = ("""
            SELECT Sexo FROM users WHERE usermail = '{}'
            """).format(email)

            sexo = Server.read_query(connection, readsexo)
            sexo = str(sexo)
            if sexo == "[('M',)]" or sexo == "[('M',)]" :
                sexo = ""
            else:
                sexo = "a"



            readnome = ("""
            SELECT nome_evento FROM `{}` WHERE data_evento = '{}'
            """).format(email, data)

            readmed = ("""
            SELECT med FROM `{}` WHERE data_evento = '{}'
            """).format(email, data)

            readobs = ("""
            SELECT detalhe_evento FROM `{}` WHERE data_evento = '{}'
            """).format(email, data)

            readhora = ("""
            SELECT hora_evento FROM `{}` WHERE data_evento = '{}'
            """).format(email, data)

            nome_evento = Server.read_query(connection, readnome)
            #nome_evento = str(nome_evento)[:-4][3:]

            medico = Server.read_query(connection, readmed)
            #medico = str(medico)[:-4][3:]

            obs = Server.read_query(connection, readobs)
            #obs = str(obs)[:-4][3:]

            hora = Server.read_query(connection, readhora)

            divs_evento = []
            c = int(c)
            c = 0
            calc = 90
            display = []
            height = 0
            tamanho = len(nome_evento)
            for nome in nome_evento:
                c = c
                if c == 0:
                    nome_div = str(nome_evento[c])[:-3][2:]
                    med_div = str(medico[c])[:-3][2:]
                    obs_div = str(obs[c])[:-3][2:]
                    hora_div = str(hora[c])[:-3][2:]
                    temp = ("""
                    <div class="l1">
                        <p>Consulta: {}</p>
                        <p>Horario: {}</p>
                        <p>Medico: {}</p>
                        <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                    </div>
                    """).format(nome_div, hora_div, med_div, c, c, obs_div)
                    divs_evento.append(temp)
                    c = c+1
                elif c == 1:
                    nome_div = str(nome_evento[c])[:-3][2:]
                    med_div = str(medico[c])[:-3][2:]
                    obs_div = str(obs[c])[:-3][2:]
                    hora_div = str(hora[c])[:-3][2:]
                    temp = ("""
                    <div class="l2">
                        <p>Consulta: {}</p>
                        <p>Horario: {}</p>
                        <p>Medico: {}</p>
                        <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                    </div>
                    """).format(nome_div, hora_div, med_div, c, c, obs_div)
                    divs_evento.append(temp)
                    c = c+1
                elif c >= 2 and c <9:
                    nome_div = str(nome_evento[c])[:-3][2:]
                    med_div = str(medico[c])[:-3][2:]
                    hora_div = str(hora[c])[:-3][2:]
                    obs_div = str(obs[c])[:-3][2:]
                    temp = ("""
                    <div class="l3">
                        <p>Consulta: {}</p>
                        <p>Horario: {}</p>
                        <p>Medico: {}</p>
                        <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                    </div>
                    """).format(nome_div, hora_div, med_div, c, c, obs_div)
                    divs_evento.append(temp)
                    c = c+1
                    height = 100
                elif c >=9 and c != tamanho-1:
                    nome_div = str(nome_evento[c])[:-3][2:]
                    med_div = str(medico[c])[:-3][2:]
                    hora_div = str(hora[c])[:-3][2:]
                    obs_div = str(obs[c])[:-3][2:]


                    temp = ("""
                    
                    <div class="lfinal" style=" background-color: none;">
                    
                        <p>Consulta: {}</p>
                        <p>Horario: {}</p>
                        <p>Medico: {}</p>
                        <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                    </div>
                    
                    """).format(nome_div, hora_div, med_div, c, c, obs_div)
                    divs_evento.append(temp)
                    c = c+1

                    linha = ("""
                    <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                    """).format(calc)
                    calc = calc+10
                    display.append(linha)
                    height = height+100
                elif c >=9 and c == tamanho-1:
                    nome_div = str(nome_evento[c])[:-3][2:]
                    med_div = str(medico[c])[:-3][2:]
                    hora_div = str(hora[c])[:-3][2:]
                    obs_div = str(obs[c])[:-3][2:]


                    temp = ("""
                    
                    <div class="lfinal espac" style="margin-top: 24px; background-color: none; ">
                    
                        <p>Consulta: {}</p>
                        <p>Horario: {}</p>
                        <p>Medico: {}</p>
                        <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                        <p style="display: none;"  id="tamanho">{}</p>
                    </div>
                    
                    """).format(nome_div, hora_div, med_div, c, c, obs_div, tamanho)
                    divs_evento.append(temp)
                    c = c+1

                    linha = ("""
                    <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                    """).format(calc)
                    calc = calc+10
                    display.append(linha)
                    

            c = 0
            org_evento = ""
            for evento in divs_evento:
                org_evento = org_evento+str(divs_evento[c])
                c = c+1

            # ordem format: sexo, username, dia, nome_evento, medico, obs
            block = "block"
            none = "none"
            filler = ""
            if data_br == None:
                data_br = ""
            return render_template("index.html").format(height, sexo, name, data_br, org_evento, display)
            #return render_template("index.html").format(sexo, name, block, org_evento, filler, none, filler)
        none = "none"
        filler = ""
        return  render_template("index.html").format(filler, sexo, name, filler, filler, filler) #teste isso de none e block
    if varteste == "med":
        #
        #PREPARAÇÃO PARA A DIV DE MEDICO
        #
        

        data_br = ''
        org_evento =''
        if request.method == "POST":
            data = request.form.get('datahoje')
            if data != None:
                data = request.form.get("datahoje")
                data_ano = data[:-6]
                data_mes = data[:-3][5:]
                data_dia = data[8:]
                data_br = (data_dia+"/"+data_mes)
                connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")

                readsexo = ("""
                SELECT Sexo FROM users WHERE usermail = '{}'
                """).format(email)

                sexo = Server.read_query(connection, readsexo)
                sexo = str(sexo)
                if sexo == "[('M',)]" or sexo == "[('M',)]" :
                    sexo = ""
                else:
                    sexo = "a"



                readnome = ("""
                SELECT nome_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)

                readmed = ("""
                SELECT med FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)

                readobs = ("""
                SELECT detalhe_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)

                readpac = ("""
                SELECT paciente FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)

                readhora = ("""
                SELECT hora_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)

                nome_evento = Server.read_query(connection, readnome)
                #nome_evento = str(nome_evento)[:-4][3:]

                medico = Server.read_query(connection, readmed)
                #medico = str(medico)[:-4][3:]

                paciente = Server.read_query(connection, readpac)

                obs = Server.read_query(connection, readobs)
                #obs = str(obs)[:-4][3:]

                hora = Server.read_query(connection, readhora)

                divs_evento = []
                c = int(c)
                c = 0
                calc = 90
                display = []
                height = 0
                tamanho = len(nome_evento)
                for nome in nome_evento:
                    c = c
                    med= str(medico[c])
                    if med != "('',)":
                        if c == 0:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = (medico[c])
                            obs_div = str(obs[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            temp = ("""
                            <div class="l1">
                                <p>Consulta: {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                            </div>
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1
                        elif c == 1:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(medico[c])
                            obs_div = str(obs[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            temp = ("""
                            <div class="l2">
                                <p>Consulta: {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                            </div>
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1
                        elif c >= 2 and c <9:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(medico[c])    
                            hora_div = str(hora[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]
                            temp = ("""
                            <div class="l3">
                                <p>Consulta: {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                            </div>
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1
                            height = 100
                        elif c >=9 and c != tamanho-1:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(medico[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]


                            temp = ("""
                            
                            <div class="lfinal" style=" background-color: none;">
                            
                                <p>Consulta: {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                            </div>
                            
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1

                            linha = ("""
                            <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                            """).format(calc)
                            calc = calc+10
                            display.append(linha)
                            height = height+100
                        elif c >=9 and c == tamanho-1:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(medico[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]


                            temp = ("""
                            
                            <div class="lfinal espac" style="margin-top: 24px; background-color: none; ">
                            
                                <p>Consulta: {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                                <p style="display: none;"  id="tamanho">{}</p>
                            </div>
                            
                            """).format(nome_div, hora_div, med_div, c, c, obs_div, tamanho)
                            divs_evento.append(temp)
                            c = c+1

                            linha = ("""
                            <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                            """).format(calc)
                            calc = calc+10
                            display.append(linha)
                    else:
                        # ? parte de caso a consulta seja de um med
                        if c == 0:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(paciente[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            temp = ("""
                            <div class="l1">
                                <p>Hoje você tem {}</p>
                                <p>Horario: {}</p>
                                <p>Paciente: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                            </div>
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1
                        elif c == 1:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(paciente[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            temp = ("""
                            <div class="l2">
                                <p>Hoje você tem {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                            </div>
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1
                        elif c >= 2 and c <9:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(paciente[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]
                            temp = ("""
                            <div class="l3">
                                <p>Hoje você tem {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                            </div>
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1
                            height = 100
                        elif c >=9 and c != tamanho-1:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(paciente[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]


                            temp = ("""
                            
                            <div class="lfinal" style=" background-color: none;">
                            
                                <p>Hoje você tem {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                            </div>
                            
                            """).format(nome_div, hora_div, med_div, c, c, obs_div)
                            divs_evento.append(temp)
                            c = c+1

                            linha = ("""
                            <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                            """).format(calc)
                            calc = calc+10
                            display.append(linha)
                            height = height+100
                        elif c >=9 and c == tamanho-1:
                            nome_div = str(nome_evento[c])[:-3][2:]
                            med_div = str(paciente[c])[:-3][2:]
                            hora_div = str(hora[c])[:-3][2:]
                            obs_div = str(obs[c])[:-3][2:]


                            temp = ("""
                            
                            <div class="lfinal espac" style="margin-top: 24px; background-color: none; ">
                            
                                <p>Hoje você tem {}</p>
                                <p>Horario: {}</p>
                                <p>Medico: {}</p>
                                <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                                <p style="display: none;"  id="tamanho">{}</p>
                            </div>
                            
                            """).format(nome_div, hora_div, med_div, c, c, obs_div, tamanho)
                            divs_evento.append(temp)
                            c = c+1

                            linha = ("""
                            <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                            """).format(calc)
                            display.append(linha)
                            calc = calc+10
                        

                c = 0
                org_evento = ""
                for evento in divs_evento:
                    org_evento = org_evento+str(divs_evento[c])
                    c = c+1

                # ordem format: sexo, username, dia, nome_evento, medico, obs
                block = "block"
                none = "none"
                filler = ""
                if data_br == None:
                    data_br = ""
                return render_template("index.html").format(height, sexo, name, data_br, org_evento, display)
            #return render_template("index.html").format(sexo, name, block, org_evento, filler, none, filler)
                #
                #COD PARA CASO O FORM DE DIA SEJA PUXADO
                #
                # data = request.form.get("datahoje")
                # data_ano = data[:-6]
                # data_mes = data[:-3][5:]
                # data_dia = data[8:]
                # data_br = (data_dia+"/"+data_mes)
                # connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")

                # readsexo = ("""
                # SELECT Sexo FROM users WHERE usermail = '{}'
                # """).format(email)

                # sexo = Server.read_query(connection, readsexo)
                # sexo = str(sexo)
                # if sexo == "[('M',)]" or sexo == "[('M',)]" :
                #     sexo = ""
                # else:
                #     sexo = "a"



                # readnome = ("""
                # SELECT nome_evento FROM `{}` WHERE data_evento = '{}'
                # """).format(email, data)

                # readmed = ("""
                # SELECT med FROM `{}` WHERE data_evento = '{}'
                # """).format(email, data)

                # readobs = ("""
                # SELECT detalhe_evento FROM `{}` WHERE data_evento = '{}'
                # """).format(email, data)

                # readhora = ("""
                # SELECT hora_evento FROM `{}` WHERE data_evento = '{}'
                # """).format(email, data)
                # readpaciente = ("""
                # SELECT paciente FROM `{}` WHERE data_evento = '{}'
                # """).format(email, data)

                # paciente = Server.read_query(connection, readpaciente)

                # nome_evento = Server.read_query(connection, readnome)
                # #nome_evento = str(nome_evento)[:-4][3:]

                # medico = Server.read_query(connection, readmed)
                # #medico = str(medico)[:-4][3:]

                # obs = Server.read_query(connection, readobs)
                # #obs = str(obs)[:-4][3:]

                # hora = Server.read_query(connection, readhora)

                # divs_evento = []
                # c = int(c)
                # c = 0
                # calc = 74.9
                # display = []
                # height = 0
                # linha = []
                # tamanho = len(nome_evento)
                # for nome in nome_evento:
                #     if medico[c] == "(None,)":
                #         c = c
                #         #
                #         #
                #         #COD AQUI
                #         #
                #         #
                #         if c == 0:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             med_div = str(medico[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             temp = ("""
                #             <div class="l1">
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Medico: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                #             </div>
                #             """).format(nome_div, hora_div, med_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1
                #         elif c == 1:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             med_div = str(medico[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             temp = ("""
                #             <div class="l2">
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Medico: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                #             </div>
                #             """).format(nome_div, hora_div, med_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1
                #         elif c >= 2 and c <9:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             med_div = str(medico[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]
                #             temp = ("""
                #             <div class="l3">
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Medico: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                #             </div>
                #             """).format(nome_div, hora_div, med_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1
                #             height = 100
                #         elif c >=9 and c != tamanho-1:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             med_div = str(medico[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]


                #             temp = ("""
                            
                #             <div class="lfinal" style=" background-color: none;">
                            
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Medico: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                #             </div>
                            
                #             """).format(nome_div, hora_div, med_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1

                #             linha = ("""
                #             <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                #             """).format(calc)
                #             calc = calc+10
                #             display.append(linha)
                #             height = height+100
                #         elif c >=9 and c == tamanho-1:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             med_div = str(medico[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]


                #             temp = ("""
                            
                #             <div class="lfinal espac" style="margin-top: 24px; background-color: none; ">
                            
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Medico: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                #                 <p style="display: none;"  id="tamanho">{}</p>
                #             </div>
                            
                #             """).format(nome_div, hora_div, med_div, c, c, obs_div, tamanho)
                #             divs_evento.append(temp)
                #             c = c+1

                #             linha = ("""
                #             <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                #             """).format(calc)
                #             calc = calc+10
                #             display.append(linha)
                                
                #     else:
                #         if c == 0:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             pac_div = str(paciente[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             temp = ("""
                #             <div class="l1">
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Paciente: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                #             </div>
                #             """).format(nome_div, hora_div, pac_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1
                #         elif c == 1:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             pac_div = str(paciente[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             temp = ("""
                #             <div class="l2">
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Paciente: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                #             </div>
                #             """).format(nome_div, hora_div, pac_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1
                #         elif c >= 2 and c <9:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             pac_div = str(paciente[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]
                #             temp = ("""
                #             <div class="l3">
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Paciente: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam" >{}</textarea></div></p>
                #             </div>
                #             """).format(nome_div, hora_div, pac_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1
                #             height = 100
                #         elif c >=9 and c != tamanho-1:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             pac_div = str(paciente[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]


                #             temp = ("""
                            
                #             <div class="lfinal" style=" background-color: none;">
                            
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Paciente: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                #             </div>
                            
                #             """).format(nome_div, hora_div, pac_div, c, c, obs_div)
                #             divs_evento.append(temp)
                #             c = c+1

                #             linha = ("""
                #             <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                #             """).format(calc)
                #             calc = calc+10
                #             display.append(linha)
                #             height = height+100
                #         elif c >=9 and c == tamanho-1:
                #             nome_div = str(nome_evento[c])[:-3][2:]
                #             pac_div = str(paciente[c])[:-3][2:]
                #             hora_div = str(hora[c])[:-3][2:]
                #             obs_div = str(obs[c])[:-3][2:]


                #             temp = ("""
                            
                #             <div class="lfinal espac" style="margin-top: 24px; background-color: none; ">
                            
                #                 <p>Consulta: {}</p>
                #                 <p>Horario: {}</p>
                #                 <p>Paciente: {}</p>
                #                 <p class="obs" id="{}" onclick="clickcel(this.id)">Obs: <div class="obsdiv" id="teste{}"><textarea disabled class="obstam">{}</textarea></div></p>
                #                 <p style="display: none;"  id="tamanho">{}</p>
                #             </div>
                            
                #             """).format(nome_div, hora_div, pac_div, c, c, obs_div, tamanho)
                #             divs_evento.append(temp)
                #             c = c+1

                #             linha = ("""
                #             <div class="linhaf" style="background-color: none; position: ; width: 100%; height: 1px; top: calc({}% + 50px); border: black dotted 2px; border-right: none; border-left: none; border-top: none; border-right: none;"></div>
                #             """).format(calc)
                #             calc = calc+10
                #             display.append(linha)
                        

                # c = 0
                # org_evento = ""
                # for evento in divs_evento:
                #     org_evento = org_evento+str(divs_evento[c])
                #     c = c+1

                # # ordem format: sexo, username, dia, nome_evento, medico, obs
                # block = "block"
                # none = "none"
                # filler = ""
                # if data_br == None:
                #     data_br = ""
                # return render_template("index_medico.html").format(height, sexo, name, data_br, org_evento, linha)

                #return aqui
        filler = ""
        none= "none"
        block = ""
        return render_template("index_medico.html").format(filler, sexo, name, data_br, filler, filler)
    if varteste == "dono":
        mednames = ("""
        SELECT usermail FROM users WHERE perm = '0'
        """)
        read = Server.read_query(connection, mednames)
        c = 0
        c = int(c)
        select_med = "a"
        for emails in read:
            c = c
            med = str(read[c])[:-3][2:]
            org_med = ("""
            <option value="{}">{}</option>
            """).format(med, med)
            select_med = select_med+org_med
            c = c+1
        usernames = ("""
        SELECT usermail FROM users WHERE perm = '1'
        """)
        read = Server.read_query(connection, usernames)
        c = 0
        c = int(c)
        select_user = ""
        for emails in read:
            c = c
            med = str(read[c])[:-3][2:]
            org_med = ("""
            <option value="{}">{}</option>
            """).format(med, med)
            select_user = select_user+org_med
            c = c+1
        if request.method == "POST":
            teste = request.form.get('inputmed')
            if teste == "AIterar":
                usertomed = request.form.get('med')
                if usertomed == None:
                    return ("""<script>
                    alert('Por favor selecione algum usuario');
                    window.location.assign("/homepage")
                    </script>
                    """)
                process1 = ("""
                ALTER TABLE `{}` ADD `paciente` VARCHAR(45) NULL AFTER `med`;
                """).format(usertomed)

                process2 = ("""
                ALTER TABLE `{}` CHANGE `med` `med` VARCHAR(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NULL;
                """).format(usertomed)

                process3 = ("""
                UPDATE users SET perm = 1 WHERE usermail = '{}';
                """).format(usertomed)

                exc1 = Server.execute_query(connection, process1)
                exc2 = Server.execute_query(connection, process2)
                exc3 = Server.execute_query(connection, process3)
                return ("""<script>
                    alert('O usuario {} agora é medico');
                    window.location.assign("/homepage")
                    </script>
                    """).format(usertomed)
            else:
                medtouser = request.form.get('user')
                if medtouser == None:
                    return ("""<script>
                    alert('Por favor selecione algum usuario');
                    window.location.assign("/homepage")
                    </script>
                    """)
                prcess1 = ("""
                ALTER TABLE `{}` DROP `paciente`;
                """).format(medtouser)

                prcess2 = ("""
                ALTER TABLE `{}` CHANGE `med` `med` VARCHAR(45) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL;
                """).format(medtouser)

                prcess3 = ("""
                UPDATE users SET perm = 0 WHERE usermail = '{}';
                """).format(medtouser)

                prcess4 = ("""
                DELETE FROM `{}` WHERE med IS NULL
                """).format(medtouser)

                exc1 = Server.execute_query(connection, prcess1)
                exc2 = Server.execute_query(connection, prcess2)
                exc3 = Server.execute_query(connection, prcess3)
                exc4 = Server.execute_query(connection, prcess4)
                return( """<script>
                    alert('O usuario {} não é mais medico');
                    window.location.assign("/homepage")
                    </script>
                    """).format(medtouser)

        return render_template("index_dono.html").format(select_user, select_med)
    else:
        return ("""<script>
                alert('por favor efetue o login {}');
                window.location.assign("/")
                </script>
                """).format(varteste)

@app.route("/logout")
def logout():
    session['varteste'] = ""
    return ("""<script>
    window.location.assign("/")
    </script>
    """)

@app.route("/delete", methods =["GET", "POST"])
def delete():
    connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")
    email = session.get('email', None)
    varteste = session.get('varteste', None)
    if varteste == "pac":
        if request.method == "POST":
            data = session.get('data', None)
            submit = request.form.get('submit')
            if submit == "0K":
                valor = request.form.get('desmarcar')
                readnome = ("""
                SELECT nome_evento FROM `{}` WHERE id_evento = '{}'
                """).format(email, valor)
                readhora = ("""
                SELECT hora_evento FROM `{}` WHERE id_evento = '{}'
                """).format(email, valor)
                hora_consulta = Server.read_query(connection, readhora)
                nome_consulta = Server.read_query(connection, readnome)
                hora_consulta = str(hora_consulta)[:-4][3:]
                nome_consulta = str(nome_consulta)[:-4][3:]
                nome_consulta = nome_consulta+" às "+hora_consulta

                readmedico = ("""
                SELECT med FROM `{}` WHERE id_evento = '{}'
                """).format(email, valor)

                read_med = Server.read_query(connection, readmedico)
                med = str(read_med)

                if med == "[(None,)]":
                    #cod para caso a pessoa desmarcando a consulta seja um medico
                    readnome_pac = ("""
                    SELECT paciente FROM `{}` WHERE id_evento = '{}'
                    """).format(email, valor)

                    nome_pac = Server.read_query(connection, readnome_pac)
                    nome_pac = str(nome_pac)[:-4][3:]

                    reademailpac = ("""
                    SELECT usermail FROM users WHERE name = '{}'
                    """).format(nome_pac)

                    emailpac = Server.read_query(connection, reademailpac)
                    emailpac = str(emailpac)[:-4][3:]
                    
                    readmed = ("""
                    SELECT name FROM users WHERE usermail = '{}'
                    """).format(email)
                    nomemed = Server.read_query(connection, readmed)
                    nomemed = str(nomemed)[:-4][3:]

                    id_evento_pac = ("""
                    SELECT id_evento FROM `{}` WHERE (data_evento, hora_evento, med) = ('{}', '{}', '{}')
                    """).format(emailpac, data, hora_consulta, nomemed)
                    id_pac = Server.read_query(connection, id_evento_pac)
                    id_pac = str(id_pac)[:-3][2:]

                    delete_evento = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(emailpac, id_pac)

                    delete_eventoself = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(email, valor)

                    delete = Server.execute_query(connection, delete_evento)
                    delete1 = Server.execute_query(connection, delete_eventoself)
                    d = "med"

                else:
                    #cod para caso a pessoa desmarcando a consulta seja um paciente
                    med = str(med)[:-4][3:]
                    reademailmed = ("""
                    SELECT usermail FROM users WHERE name = '{}'
                    """).format(med)
                    emailmed = Server.read_query(connection, reademailmed)
                    emailmed = str(emailmed)[:-4][3:]

                    readnomepac = ("""
                    SELECT name FROM users WHERE usermail = '{}'
                    """).format(email)
                    nomepac = Server.read_query(connection, readnomepac)
                    nomepac = str(nomepac)[:-4][3:]

                    id_evento_med = ("""
                    SELECT id_evento FROM `{}` WHERE (data_evento, hora_evento, paciente) = ('{}', '{}', '{}')
                    """).format(emailmed, data, hora_consulta, nomepac)

                    id_med = Server.read_query(connection, id_evento_med)
                    id_med = str(id_med)[:-3][2:] 
                    
                    delete_evento = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(emailmed, id_med)

                    delete_eventoself = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(email, valor)
                    
                    delete = Server.execute_query(connection, delete_evento)
                    delete1 = Server.execute_query(connection, delete_eventoself)
                    d = "pac"
                data = session.get('data', None)
                #return(id_med)
                return("""<script>
                alert('Consulta desmarcada');
                window.location.assign("/delete")
                </script>
                """)
            else:
                data = request.form.get('data')
                data = str(data)
                session['data'] = data
                read = ("""
                SELECT nome_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)
                readh = ("""
                SELECT hora_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)
                readd = ("""
                SELECT id_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)
                read_id = Server.read_query(connection, readd)
                read_horas = Server.read_query(connection, readh)
                read_eventos = Server.read_query(connection, read)
                c = 0
                c = int(c)
                select_evento = ""
                for evento in read_eventos: 
                    id_evento = str(read_id[c])[:-2][1:] 
                    hora_evento = str(read_horas[c])[:-3][2:]
                    nome_evento = str(read_eventos[c])[:-3][2:]
                    div_evento = ("""
                    <option value="{}">{} às {}</option>
                    """).format(id_evento, nome_evento, hora_evento)
                    select_evento = select_evento + div_evento
                    c = c+1
                if select_evento == "":
                    filler = "disabled"
                else:
                    filler = ""
                
                return render_template("consultas_pac.html").format(filler, select_evento)
        disabled = "disabled"
        filler = ""
        return render_template("consultas_pac.html").format(disabled, filler)
    if varteste == "med":

        #! COLOCAR PARTE DOS PACIENTES AQUI
        readpac = ("""
        SELECT name FROM users WHERE usermail <> '{}'
        """).format(email)
        readpermpac =  ("""
        SELECT perm FROM users WHERE usermail <> '{}'
        """).format(email)
        readsexopac = ("""
        SELECT sexo FROM users WHERE usermail <> '{}'
        """).format(email)
        nomes_pac = Server.read_query(connection, readpac)
        perms_pac = Server.read_query(connection, readpermpac)
        sexos_pac = Server.read_query(connection, readsexopac)
        c = 0
        c = int(c)
        select_pac = ""
        for nome in nomes_pac:
            perm_pac = str(perms_pac[c])[:-2][1:]
            sexotemp_pac = str(sexos_pac[c])
            if sexotemp_pac == "('F',)":
                sexo_pac = "a"
            else:
                sexo_pac = ""
            if perm_pac == "1":
                nome_pac = str(nomes_pac[c])[:-3][2:]
                org_select = ("""
                <option value="{}"> Doutor{} {}</option>
                """).format(nome_pac, sexo_pac, nome_pac)
                select_pac = select_pac + org_select
                c = c+1
            else:                
                nome_pac = str(nomes_pac[c])[:-3][2:]
                org_select = ("""
                <option value="{}">{}</option>
                """).format(nome_pac, nome_pac)
                select_pac = select_pac + org_select
                c = c+1
        ############################!
        if request.method == "POST":
            data = session.get('data', None)
            submit = request.form.get('submit')
            submitdel = request.form.get('submitdel')

            if submitdel == "0K":
                connection = Server.create_db_connection("sql10.freesqldatabase.com", "sql10522353", "DAi1mTDqMz", "sql10522353")
                readsexo = ("""
                SELECT Sexo FROM users WHERE usermail = '{}' 
                """).format(email)
                sexo = Server.read_query(connection, readsexo)
                sexo = str(sexo)
                if sexo == "[('M',)]" or sexo == "[('O',)]" :
                    sexo = ""
                else:
                    sexo = "a"
                email = session.get('email', None)
                name = session.get('name', None)
                ###################################! TESTE TESTE
                paciente = request.form.get('paciente')
                data_evento = request.form.get('data_evento')
                nome_evento = request.form.get('nome_evento')
                obs_evento = request.form.get('detalhe_evento')
                hora_evento = request.form.get('hora_evento')

                femailpac = ("""
                SELECT usermail FROM users WHERE name = '{}'
                """).format(paciente)
                emailpac = Server.read_query(connection, femailpac)
                emailpac = str(emailpac)[:-4][3:]

                getperm = ("""
                SELECT perm FROM users WHERE name = '{}'
                """).format(paciente)
                permpac = Server.read_query(connection, getperm)
                permpac = str(permpac)[:-3][2:]
                if permpac == "0" or permpac == "2":
                    cadevento = ("""
                    INSERT INTO `{}` VALUES (NULL, '{}', '{}', '{}', '{}', '{}')
                    """).format(emailpac, nome_evento, obs_evento, data_evento, hora_evento, name)
                if permpac == "1":
                    cadevento = ("""
                    INSERT INTO `{}` VALUES (NULL, '{}', '{}', '{}', '{}', '{}', NULL)
                    """).format(emailpac, nome_evento, obs_evento, data_evento, hora_evento, name)


                exc = Server.execute_query(connection, cadevento)

                nome_evento = str(nome_evento)
                paciente = str(paciente)
                nome_eventomed = "Consulta: "+nome_evento
                cadeventomed = ("""
                INSERT INTO `{}` VALUES (NULL, '{}', '{}', '{}', '{}', NULL, '{}')
                """).format(email, nome_eventomed, obs_evento, data_evento, hora_evento, paciente)

                exc = Server.execute_query(connection, cadeventomed)



                
                return("""<script>
                alert('Consulta cadastrada com sucesso, doutor{} {}');
                window.location.assign("/homepage")
                </script>
                """).format(sexo, name)

            if submit == "0K":
                valor = request.form.get('desmarcar')
                readnome = ("""
                SELECT nome_evento FROM `{}` WHERE id_evento = '{}'
                """).format(email, valor)
                readhora = ("""
                SELECT hora_evento FROM `{}` WHERE id_evento = '{}'
                """).format(email, valor)
                hora_consulta = Server.read_query(connection, readhora)
                nome_consulta = Server.read_query(connection, readnome)
                hora_consulta = str(hora_consulta)[:-4][3:]
                nome_consulta = str(nome_consulta)[:-4][3:]
                nome_consulta = nome_consulta+" às "+hora_consulta

                readmedico = ("""
                SELECT med FROM `{}` WHERE id_evento = '{}'
                """).format(email, valor)

                read_med = Server.read_query(connection, readmedico)
                med = str(read_med)

                if med == "[(None,)]":
                    #cod para caso a pessoa desmarcando a consulta seja um medico
                    readnome_pac = ("""
                    SELECT paciente FROM `{}` WHERE id_evento = '{}'
                    """).format(email, valor)

                    nome_pac = Server.read_query(connection, readnome_pac)
                    nome_pac = str(nome_pac)[:-4][3:]

                    reademailpac = ("""
                    SELECT usermail FROM users WHERE name = '{}'
                    """).format(nome_pac)

                    emailpac = Server.read_query(connection, reademailpac)
                    emailpac = str(emailpac)[:-4][3:]
                    
                    readmed = ("""
                    SELECT name FROM users WHERE usermail = '{}'
                    """).format(email)
                    nomemed = Server.read_query(connection, readmed)
                    nomemed = str(nomemed)[:-4][3:]

                    id_evento_pac = ("""
                    SELECT id_evento FROM `{}` WHERE (data_evento, hora_evento, med) = ('{}', '{}', '{}')
                    """).format(emailpac, data, hora_consulta, nomemed)
                    id_pac = Server.read_query(connection, id_evento_pac)
                    id_pac = str(id_pac)[:-3][2:]

                    delete_evento = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(emailpac, id_pac)

                    delete_eventoself = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(email, valor)

                    delete = Server.execute_query(connection, delete_evento)
                    delete1 = Server.execute_query(connection, delete_eventoself)
                    d = "med"

                else:
                    #cod para caso a pessoa desmarcando a consulta seja um paciente
                    med = str(med)[:-4][3:]
                    reademailmed = ("""
                    SELECT usermail FROM users WHERE name = '{}'
                    """).format(med)
                    emailmed = Server.read_query(connection, reademailmed)
                    emailmed = str(emailmed)[:-4][3:]

                    readnomepac = ("""
                    SELECT name FROM users WHERE usermail = '{}'
                    """).format(email)
                    nomepac = Server.read_query(connection, readnomepac)
                    nomepac = str(nomepac)[:-4][3:]

                    id_evento_med = ("""
                    SELECT id_evento FROM `{}` WHERE (data_evento, hora_evento, paciente) = ('{}', '{}', '{}')
                    """).format(emailmed, data, hora_consulta, nomepac)

                    id_med = Server.read_query(connection, id_evento_med)
                    id_med = str(id_med)[:-3][2:] 
                    
                    delete_evento = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(emailmed, id_med)

                    delete_eventoself = ("""
                    DELETE FROM `{}` WHERE id_evento = '{}'
                    """).format(email, valor)
                    
                    delete = Server.execute_query(connection, delete_evento)
                    delete1 = Server.execute_query(connection, delete_eventoself)
                    d = "pac"
                data = session.get('data', None)
                #return(id_med)
                return("""<script>
                alert('Consulta desmarcada');
                window.location.assign("/delete")
                </script>
                """)
            else:
                data = request.form.get('data')
                data = str(data)
                session['data'] = data
                read = ("""
                SELECT nome_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)
                readh = ("""
                SELECT hora_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)
                readd = ("""
                SELECT id_evento FROM `{}` WHERE data_evento = '{}'
                """).format(email, data)
                read_id = Server.read_query(connection, readd)
                read_horas = Server.read_query(connection, readh)
                read_eventos = Server.read_query(connection, read)
                c = 0
                c = int(c)
                select_evento = ""
                for evento in read_eventos: 
                    id_evento = str(read_id[c])[:-2][1:] 
                    hora_evento = str(read_horas[c])[:-3][2:]
                    nome_evento = str(read_eventos[c])[:-3][2:]
                    div_evento = ("""
                    <option value="{}">{} às {}</option>
                    """).format(id_evento, nome_evento, hora_evento)
                    select_evento = select_evento + div_evento
                    c = c+1
                if select_evento == "":
                    filler = "disabled"
                else:
                    filler = ""
                
                return render_template("consultas.html").format(filler, select_evento)
        disabled = "disabled"
        filler = ""
        return render_template("consultas.html").format(select_pac,disabled, filler)
    else:
        return ("""<script>
        alert('por favor efetue o login {}');
        window.location.assign("/")
        </script>
        """).format(varteste)

    

#Rodando o site#

#só vai rodar o site se ele for iniciado diretamente por esse cod
if __name__ == "__main__":
    app.run(debug=True)#isso at o site automaticamente#