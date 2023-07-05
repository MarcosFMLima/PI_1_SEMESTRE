#Marcos Felipe Moreira de Lima

#Conexão com o banco de dados Oracle 
import oracledb

connection = oracledb.connect(
    user="bd240223136",
    password="Olmkc1",
    dsn="172.16.12.14/xe")

print("Conectado ao Banco de dados com sucesso!!!")

cursor = connection.cursor()

#Criação da tabela, caso seja necessário dar um drop manualmente.
'''cursor.execute("""
  CREATE TABLE amostras (
  id integer PRIMARY KEY,
  MP10 varchar(100) NOT NULL,
  "MP2.5" varchar(100) NOT NULL,
  O3 varchar(100) NOT NULL,
  CO varchar(100) NOT NULL,
  NO2 varchar(100) NOT NULL,
  SO2 varchar(100) NOT NULL
)""")
connection.commit()'''

def inserir_amostras():
    print("\n--- Inserir Dados ---")
    try: #Se uma exceção ocorrer dentro do bloco try, o controle é transferido para o bloco except
        id = int(input("ID: "))
        mp10 = float(input("MP10: "))
        mp25 = float(input("MP2.5: "))
        o3 = float(input("O3: "))
        co = float(input("CO: "))
        no2 = float(input("NO2: "))
        so2 = float(input("SO2: "))

        
        if any(value < 0 for value in [id, mp10, mp25, o3, co, no2, so2]):
            print("\nValores negativos são inválidos!")
        else:
            cursor.execute(f"INSERT INTO amostras (id, MP10, \"MP2.5\", O3, CO, NO2, SO2) VALUES ({id}, {mp10}, {mp25}, {o3}, {co}, {no2}, {so2})")
            connection.commit()
            print("\nAmostras inseridas com sucesso!")

    except Exception:
        print("\nErro ao inserir amostras! Campo vazio ou ID existente!!")

def excluir_amostras():
    print("\n--- Excluir Dados ---")
    
    cursor.execute("SELECT id FROM amostras")
    ids = [row[0] for row in cursor.fetchall()] #percorrer toda a linha 0 e mandar dentro dessa variável

    try:
        cursor.execute("SELECT id FROM amostras")
        results = cursor.fetchall()

        print("\nIDs das amostras disponíveis:")
        for result in results:
            print(result[0])

        id = int(input("\nID da amostra a ser excluída: "))

        cursor.execute(f"DELETE FROM amostras WHERE id = {id}")
        connection.commit()

        if id not in ids:
            print("\nNão há amostras com esse valor para excluir.")
            return

        print("\nAmostra excluída com sucesso!")
    except Exception:
        print("\nErro ao excluir a amostra!")

def alterar_amostras():
    print("\n--- Alterar Dados ---")

    try:
        cursor.execute("SELECT id FROM amostras")
        ids = [row[0] for row in cursor.fetchall()]

        if len(ids) == 0:
            print("\nNão há amostras existentes para alterar.")
            return

        cursor.execute("SELECT id FROM amostras")
        results = cursor.fetchall()

        print("\nIDs das amostras disponíveis:")
        for result in results:
            print(result[0])

        id_amostra = int(input("\nEscolha o ID da amostra a ser alterada: "))

        if id_amostra not in ids:
            print("\nID da amostra não encontrado.")
            return

        cursor.execute(f"SELECT MP10, \"MP2.5\", O3, CO, NO2, SO2 FROM amostras WHERE id = {id_amostra}")
        parametros_atuais = cursor.fetchone() #para chamar uma linha apenas de cada parâmetro

        if parametros_atuais is None:
            print("\nOs valores dos parâmetros dessa amostra não foram encontrados.")
            return

        mp10_atual, mp25_atual, o3_atual, co_atual, no2_atual, so2_atual = parametros_atuais

        print(f"\nValores atuais dos parâmetros da amostra ID {id_amostra}:")
        print("MP10:", mp10_atual)
        print("MP2.5:", mp25_atual)
        print("O3:", o3_atual)
        print("CO:", co_atual)
        print("NO2:", no2_atual)
        print("SO2:", so2_atual)

        mp10_novo = float(input("Novo valor de MP10: "))
        mp25_novo = float(input("Novo valor de MP2.5: "))
        o3_novo = float(input("Novo valor de O3: "))
        co_novo = float(input("Novo valor de CO: "))
        no2_novo = float(input("Novo valor de NO2: "))
        so2_novo = float(input("Novo valor de SO2: "))
        
        if any(value < 0 for value in [mp10_novo, mp25_novo, o3_novo, co_novo, no2_novo, so2_novo]):
            print("\nValores negativos são inválidos!")
        else:
            cursor.execute(f"UPDATE amostras SET MP10 = {mp10_novo}, \"MP2.5\" = {mp25_novo}, O3 = {o3_novo}, CO = {co_novo}, NO2 = {no2_novo}, SO2 = {so2_novo} WHERE id = {id_amostra}")
            connection.commit() #salvar todas as alterações feitas no sql 
            print("\nParâmetros da amostra atualizados com sucesso!")

    except Exception:
        print("\nErro ao atualizar amostra! Campo vazio ou valor inválido!")

def classificar_amostras():
    print("\n--- Classificação do Ar ---")
    print("")

    cursor.execute("SELECT MP10, \"MP2.5\", O3, CO, NO2, SO2 FROM amostras")
    results = cursor.fetchall()

    if len(results) == 0:
        print("\nSem amostras pra mostrar classificação!")
        return
    
    #variáveis de soma, iniciando com 0
    mp10_sum = 0
    mp25_sum = 0
    o3_sum = 0
    co_sum = 0
    no2_sum = 0
    so2_sum = 0

    for result in results:
        mp10_sum += float(result[0])
        mp25_sum += float(result[1])
        o3_sum += float(result[2])
        co_sum += float(result[3])
        no2_sum += float(result[4])
        so2_sum += float(result[5])

    #variável das médias calculando o valor já
    mp10_avg = mp10_sum / len(results)
    mp25_avg = mp25_sum / len(results)
    o3_avg = o3_sum / len(results)
    co_avg = co_sum / len(results)
    no2_avg = no2_sum / len(results)
    so2_avg = so2_sum / len(results)

    print("")
    print(f"Média MP10: {mp10_avg:.2f}")  # formatação :.2f (duas casas decimais após a virgula), se eu quisesse 4 casas decimais após a virgula, colocaria :.4f
    print(f"Média MP2.5: {mp25_avg:.2f}")
    print(f"Média O3: {o3_avg:.2f}")
    print(f"Média CO: {co_avg:.2f}")
    print(f"Média NO2: {no2_avg:.2f}")
    print(f"Média SO2: {so2_avg:.2f}")
    print("")

    if mp10_avg <= 50 and mp25_avg <= 25 and o3_avg <= 100 and co_avg <= 9 and no2_avg <= 200 and so2_avg <= 20:
        print("Qualidade do ar boa!")
        print("\nNão há riscos à saúde")
    elif mp10_avg <= 100 and mp25_avg <= 50 and o3_avg <= 130 and co_avg <= 11 and no2_avg <= 240 and so2_avg <= 40:
        print("Qualidade do ar regular!")
        print("\nPessoas de grupos sensíveis (crianças, idosos e \npessoas com doenças respiratórias e cardíacas) podem \napresentar sintomas como tosse seca e cansaço. A população,\nem geral, não é afetada.")
    elif mp10_avg <= 150 and mp25_avg <= 75 and o3_avg <= 160 and co_avg <= 13 and no2_avg <= 320 and so2_avg <= 365:
        print("Qualidade do ar ruim!")
        print("\nToda a população pode apresentar sintomas como \ntosse seca, cansaço, ardor nos olhos, nariz e garganta.\nPessoas de grupos sensíveis (crianças, idosos e pessoas \ncom doenças respiratórias e cardíacas) podem \napresentar efeitos mais sérios na saúde.")
    elif mp10_avg <= 250 and mp25_avg <= 125 and o3_avg <= 200 and co_avg <= 15 and no2_avg <= 1130 and so2_avg <= 800:
        print("Qualidade do ar muito ruim!")
        print("\nToda a população pode apresentar agravamento dos\n sintomas como tosse seca, cansaço, ardor nos olhos,\nnariz e garganta e ainda falta de ar e respiração ofegante.\nEfeitos ainda mais graves à saúde de grupos sensíveis (crianças, \nidosos e pessoas com doenças respiratórias e cardíacas).")
    else:
        print("Qualidade do ar péssima!")
        print("\nToda a população pode apresentar sérios riscos\nde manifestação de doenças respiratórias e cardiovasculares.\nAumento de mortes prematuras em pessoas de grupos sensíveis.")

def exibir_menu():
    while True:
        print("\n=-=-=-=-=-=-=-=- Menu -=-=-=-=-=-=-=-=")
        print("\t1. Inserir amostras")
        print("\t2. Excluir amostras")
        print("\t3. Alterar amostras")
        print("\t4. Classificar amostras")
        print("\t5. Sair")
        print("=-"*19)

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            inserir_amostras()
        elif opcao == "2":
            excluir_amostras()
        elif opcao == "3":
            alterar_amostras()
        elif opcao == "4":
            classificar_amostras()
        elif opcao == "5":
            print("\nPrograma encerrado, obrigado por usar!!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

exibir_menu()
connection.close()
