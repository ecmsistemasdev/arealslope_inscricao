import streamlit as st
import mysql.connector
import re
from datetime import date, datetime
import smtplib
import email.message

conexao = mysql.connector.connect(
    host='arealslope.mysql.uhserver.com',
    user='ecmsistemas',
    password='@Musica17',
    database='arealslope'
)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


v_nome = ""
v_ncelular = ""
v_email = ""
v_km = ""
v_vlinscricao = ""

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

def calculateAge(birthDate): 
    #dia = int(nascimento[0:2])
    #mes = int(nascimento[3:5])
    #ano = int(nascimento[6:10])

    #birthDate = date(ano, mes, dia)

    data_str = "19/01/2025"
    dataRef = datetime.strptime(data_str, "%d/%m/%Y")

    #today = date.today() 
    age = dataRef.year - birthDate.year - ((dataRef.month, dataRef.day) < (birthDate.month, birthDate.day)) 
  
    return age 


def enviar_email(snome,sfone,skm,semail, svl): 
    try: 
        corpo_email = f"""
        <p>Pré inscrição realizada para a <b>1ª Corrida Areal Slope</b> </p>
        <p>Nome: <b>{snome}</b> </p>
        <p>Telefone: <b>{sfone}</b> </p>
        <p>Percurso: <b>{skm}</b> </p>
        <p>Valor da Inscrição: <b> R$ {svl}</b> </p>
        """
        
        msg = email.message.Message()
        msg['Subject'] = "Inscrição 1ª Corrida Areal Slope - "+ snome
        msg['From'] = 'ecmsistemasdeveloper@gmail.com'
        msg['To'] = "kelioesteves@hotmail.com;"
        msg['Co'] = semail
        password = 'mwxncuvjvmvwvnhp' 
        msg.add_header('Content-Type', 'text/html')
        #msg.attach()
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To'],msg['Co']], msg.as_string().encode('utf-8'))
        s.quit()
        st.write("")
    except Exception as e:
        st.write("")
    #finally:            


def concluido():
    global tela_ativa
    #placeholder.empty()
    #placeholder2 = st.empty()

    #with placeholder2.form("Regulamento"):
    st.success("INSCRIÇÃO REALIZADA COM SUCESSO")
    #st.write(incricao().modalidade)
    #st.write(incricao().idmodalidade)
    #st.write(incricao().kmsolo)
    #st.write("id_atleta ", inscricao().idatleta)



st.set_page_config(page_title="1ª Corrida Areal Slope")
tela_ativa = 0

from PIL import Image
img = Image.open('02.png')
st.image(img)

st.markdown("### 1ª Corrida Areal Slope")


form_inscricao = st.empty()

def inscricao():
    global tela_ativa
    global concluido
    global v_nome, v_ncelular, v_email, v_km, v_vlinscricao

    cpfvalido =False

    def validador(cpf):
        global cpfvalido
        cpfvalido = False
        
        #Retira apenas os dígitos do CPF, ignorando os caracteres especiais
        numeros = [int(digito) for digito in cpf if digito.isdigit()]
        
        quant_digitos = False
        validacao1 = False
        validacao2 = False

        if len(numeros) == 11:
            quant_digitos = True
        
            soma_produtos = sum(a*b for a, b in zip (numeros[0:9], range (10, 1, -1)))
            digito_esperado = (soma_produtos * 10 % 11) % 10
            if numeros[9] == digito_esperado:
                validacao1 = True

            soma_produtos1 = sum(a*b for a, b in zip(numeros [0:10], range (11, 1, -1)))
            digito_esperado1 = (soma_produtos1 *10 % 11) % 10
            if numeros[10] == digito_esperado1:
                validacao2 = True

            if quant_digitos == True and validacao1 == True and validacao2 == True:
                cpfvalido = True
            else:
                cpfvalido = False

        else:
            cpfvalido = False


    with ((form_inscricao.form("Inscricao"))):
        st.markdown("### Formulário de Inscrição")

        input_km = st.radio("Percurso:", ["7km", "14km", "21km"], captions=["R$ 90,00","R$ 100,00","R$ 115,00"], key="00")
        input_email = st.text_input(label="E-mail:", key="01")
        input_nome = st.text_input(label="Primeiro Nome:", placeholder="Insira apenas seu primeiro nome", key="02")
        input_sobrenome = st.text_input(label="Sobrenome:", placeholder="Insira seu sobrenome",key="03")
        c1,c2 = st.columns([1,1])
        with c1:
            input_cpf = st.text_input(label="CPF (99999999999):", placeholder="Somente números", max_chars=11,key="04")
        with c2:
            input_dn = st.date_input(label="Data de Nascimento:",format="DD/MM/YYYY", 
                                     max_value=date(year=2008, month=1, day=1),min_value=date(year=1924, month=1, day=1), value=None, key="05")
        
        f1,f2,f3 = st.columns([1,1,1])
        with f1:
            input_telefone = st.text_input(label="Nº Celular 99 99999-9999:", max_chars=15, key="06")
        with f2:
            input_genero = st.radio("Gênero:", ["Masculino", "Feminino"])
        with f3:
            input_camiseta = st.radio("Camiseta:", ["PP", "P", "M", "G", "GG"])

        st.divider()
        st.write("Ao confirmar a inscrição você está concordando com os termos do regulamento")

        cursor = conexao.cursor()
        comando = f'SELECT ID_ATLETA FROM arealslope.ATLETA WHERE CPF = "{input_cpf}"'
        cursor.execute(comando)
        resultado_cpf = cursor.fetchone()

        cursor2 = conexao.cursor()
        id_ = f'SELECT IFNULL(MAX(ID_ATLETA)+1,1) FROM arealslope.ATLETA'
        cursor2.execute(id_)
        newid = cursor2.fetchone()
        idatleta = newid[0]

        confirma_button = st.form_submit_button("CONFIRMAR INSCRIÇÃO",type="primary", disabled=False)  # not st.session_state.disabled)
                                
        if confirma_button:
            if input_email == '':
                st.warning("Informe o E-mail!", icon="⚠️")
                st.stop()

            if input_cpf == '':
                st.warning("Informe o CPF!", icon="⚠️")
                st.stop()

            ncpf = input_cpf
            crtr2 = "!@#$()*'%:;?<>_\|/ .-,"
            for i in range(0,len(crtr2)):
                ncpf = ncpf.replace(crtr2[i],"")

            #validador(ncpf)

            # verifica numero do CPF
            
            #Retira apenas os dígitos do CPF, ignorando os caracteres especiais
            cpfvalido = False
            numeros = [int(digito) for digito in ncpf if digito.isdigit()]
            
            quant_digitos = False
            validacao1 = False
            validacao2 = False

            if len(numeros) == 11:
                quant_digitos = True
            
                soma_produtos = sum(a*b for a, b in zip (numeros[0:9], range (10, 1, -1)))
                digito_esperado = (soma_produtos * 10 % 11) % 10
                if numeros[9] == digito_esperado:
                    validacao1 = True

                soma_produtos1 = sum(a*b for a, b in zip(numeros [0:10], range (11, 1, -1)))
                digito_esperado1 = (soma_produtos1 *10 % 11) % 10
                if numeros[10] == digito_esperado1:
                    validacao2 = True

                if quant_digitos == True and validacao1 == True and validacao2 == True:
                    cpfvalido = True
                else:
                    cpfvalido = False

            else:
                cpfvalido = False


            if cpfvalido == False:
                st.warning(f"O CPF {ncpf} não é válido!", icon="⚠️")
                st.stop()
            
            if input_km == '':
                st.warning("Informe o Km!", icon="⚠️")
                st.stop()

            if input_nome == '':
                st.warning("Informe o primeiro Nome!", icon="⚠️")
                st.stop()

            if input_sobrenome == '':
                st.warning("Informe o primeiro Nome!", icon="⚠️")
                st.stop()

            if input_dn == '':
                st.warning("Informe sua Data de Nascimento!", icon="⚠️")
                st.stop()

            if input_telefone == '':
                st.warning("Informe o número do Celular!", icon="⚠️")
                st.stop()

            ncelular = input_telefone
            crtr1 = "!@#$()*'%:;?<>_\|/ .-,"
            for i in range(0,len(crtr1)):
                ncelular = ncelular.replace(crtr1[i],"")

            if len(ncelular) is not 11:
                st.warning("Nº do celular inválido")
                st.stop()

            if resultado_cpf is not None:
                st.warning("CPF Já cadastrado!", icon="⚠️")
                st.stop()

            if input_genero == 'Masculino':
                sexo = "M"
            else:
                sexo = "F"

            data = date.today()
            dataf = data.strftime('%d/%m/%Y')
            datanasc = input_dn.strftime('%d/%m/%Y')
            idade = calculateAge(input_dn)
            
            if input_km == "7km":
                idpercurso = 3
                if idade < 60:
                    vl = 90
                else:
                    vl = 45
            elif input_km == "14km":
                idpercurso = 2
                if idade < 60:
                    vl = 100
                else:
                    vl = 50
            elif input_km == "21km":
                idpercurso = 1
                if idade < 60:
                    vl = 115
                else:
                    vl = 57.5

            vl_inscricao = vl

            v_nome = input_nome + ' ' + input_sobrenome
            v_ncelular = ncelular
            v_km = input_km
            v_email = input_email
            v_ano = 2025
            v_vlinscricao = vl_inscricao

            try:
                
                qry_insert = f"""INSERT INTO arealslope.ATLETA (
                                 ID_ATLETA, EMAIL, CPF, NOME, DT_NASCIMENTO, NR_CELULAR, SEXO, CAMISETA, KM, FL_PAGO, 
                                 ATIVO, DT_INSCRICAO, ACEITO_TERMO, VL_PAGO, VL_INSCRICAO, ID_ANO, ID_PERCURSO, IDADE )
                                 VALUES (
                                        {idatleta},"{input_email}","{ncpf}",upper("{input_nome + ' ' + input_sobrenome}"),"{datanasc}","{ncelular}",
                                        "{sexo}","{input_camiseta}","{v_km}",'N','S',"{dataf}",'S',0,{vl_inscricao},{v_ano},{idpercurso},{idade}) """

                cursor = conexao.cursor()
                cursor.execute(qry_insert)
                conexao.commit()
                cursor.close()

            except mysql.connector.Error as error:
                st.warning("Erro no Banco de Daods, tente novamente, se persistir contate o Administrador do Sistema! {}".format(error), icon="⚠️")
                st.stop()

            finally:
                if conexao.is_connected():
                    conexao.close()            
        
            tela_ativa = 2

            form_inscricao.empty()

inscricao()

if tela_ativa == 2:

    valor_incr = "{:,.2f}".format(v_vlinscricao).replace(",", "X").replace(".", ",").replace("X", ".")

    msg = f"""Valor da Inscrição: R$ {valor_incr}"""

    st.success("PRÉ INSCRIÇÃO REALIZADA COM SUCESSO", icon="😀")
    st.warning("ATENÇÃO", icon="⚠️")
    st.warning("A efetivação da sua Inscrição está condicionada ao envio do comprovante de pagamento para o número (69) 99925-9005, ou pelo link a baixo:")
    st.warning("https://wa.me/5569999259005", icon="📱")

    st.warning(msg)
    st.warning("Pix para pagamento: Kelioesteves@hotmail.com")

    enviar_email(v_nome,v_ncelular,v_km, v_email, valor_incr)
 
from PIL import Image
img = Image.open('003.png')
st.image(img)
