import pandas as pd
import datetime
from lxml import html
import requests
# import pygsheets
def obs_from_portal(NE, url):
    xpath = '/html/body/main/div[2]/section[1]/div[3]/div/span/text()'
    url = url + NE
    r = requests.get(url).content
    tree = html.fromstring(r)
    result = tree.xpath(xpath)[0]
    return result
def resp_df(dados):
    resp = []
    pac = ['PAC/CITEX', 'PAC/DPI', 'DPI']
    ac_defesa = ['AC DEFESA', 'ACDEFESA']
    fa = ['ALMOX', 'ALMO', 'ALMX', 'GARAGEM', 'VIATURA', 'MECANICA', 'VEICULO', 'VEICULOS', 'ECT', 'CORREIOS',
          'CORREIO','ENERGIA', 'ELETRICA', 'ILUMINAÇÃO', 'ILUMINACAO', 'FA', 'DPC', 'AJUDA DE CUSTOS', 'BAGAGEM',
          'TELEGRAFOS', 'TIM S A', 'COMPANHIA DE SANEAMENTO AMBIENTAL DO DISTRITO FEDERAL', 'VOETUR TURISMO E REPRESENTACOES LTDA',
          'FORTALEZA SERVICOS EMPRESARIAIS EIRELI']
    dci = ['CONTRATOS', 'CONTRATO', 'DCI', 'BRASIL DIGITAL TELECOMUNICACOES LTDA']
    dgsi = ['NIVA TECNOLOGIA DA INFORMACAO LTDA']
    salc = ['EMPRESA BRASIL DE COMUNICACAO S,A', 'EMPRESA BRASIL DE COMUNICACAO S.A']
    cta = ['ORACLE DO BRASIL SISTEMAS LTDA', 'GFS SOFTWARE E CONSULTORIA LIMITADA']
    for texto, teste in dados.iterrows():
        if 'CITEX' in teste['OBS'][:10]:
            if any(x in teste['NOME_FAV'] for x in fa):
                resp.append('FA')
                continue
            if any(x in teste['NOME_FAV'] for x in dgsi):
                resp.append('DGSI')
                continue
            if any(x in teste['NOME_FAV'] for x in salc):
                resp.append('SALC')
                continue
            if any(x in teste['NOME_FAV'] for x in dci):
                resp.append('DCI')
                continue
            if any(x in teste['OBS'] for x in pac):
                resp.append('PAC')
                continue
            if 'DGSI' in teste['OBS']:
                resp.append('DGSI')
                continue
            if 'SALC' in teste['OBS']:
                resp.append('SALC')
                continue
            if any(x in teste['OBS'] for x in dci):
                resp.append('DCI')
                continue
            if any(x in teste['OBS'] for x in fa):
                resp.append('FA')
                continue
            else:
                resp.append('CITEX')
                print(teste['NE'])
                continue
        if any(x in teste['NOME_FAV'] for x in dci):
            resp.append('DCI')
            continue
        if any(x in teste['NOME_FAV'] for x in cta):
            resp.append('7ºCTA')
            continue
        if any(x in teste['OBS'] for x in ac_defesa):
            resp.append('AC DEFESA')
            continue
        if 'CTA' in teste['OBS']:
            resp.append('7ºCTA')
            continue
        if 'CDS' in teste['OBS'][:10]:
            resp.append('CDS')
            continue
        else:
            resp.append('--')
            print(teste['NE'])
            continue

    return resp
gestão = input('INSIRA A GESTÃO PARA ANALISAR ( 0 ou 7 ) >>>  ')
xpath = '/html/body/main/div[2]/section[1]/div[3]/div/span/text()'
url='http://www.portaltransparencia.gov.br/despesas/empenho/16{}09100001'.format(gestão)

links = []
obs  = []
dados = pd.read_csv('RPNP/planilhao_ug_16{}091.csv'.format(gestão), sep= '\t', thousands='.', decimal=',')
print('Pegando Dados')
for texto, teste in dados.iterrows():
    ne = teste['NE'][:-2]
    # obs.append(obs_from_portal(ne, url))
    obs.append('nada')
    links.append(url+teste['NE'][:-2])


dados.insert(15,'LINK_NE', links)
# dados.insert(16, 'OBS', obs)
resp = resp_df(dados)
dados.insert(17,'RESP', resp)
dados = dados.rename(columns={'EMISSAO':'DATA'})
dados.insert(19,'TEMPO', 0)
# print(resp)
print(dados.columns)
final_aliq = dados.query('ALIQ > 0')

# final_aliq.to_csv('RPNP/planilhao_ug_16{}091_ALIQ.csv'.format(gestão))
# final_apag = dados.query('APAG > 0')
# final_apag = final_apag.applymap(str).replace(r'\.',',',regex=True)
# final_apag.to_csv('RPNP/planilhao_ug_16{}091_A_PAG.csv'.format(gestão))

dados = dados.rename(columns={'DATA': 'EMISSÃO', 'ALIQ':'A_LIQUIDAR', 'APAG': 'A_PAGAR'})

# final_aliq = dados[['NE', 'EMISSÃO','PI', 'ND', 'OBS', 'RESP', 'A_LIQUIDAR']].query('A_LIQUIDAR > 0')
# final_aliq = final_aliq.applymap(str).replace(r'\.',',',regex=True)
# final_aliq.to_csv('CONSOLIDADO/16{}061_ALIQ.csv'.format(gestão))




# final_apag = dados[['NE', 'EMISSÃO','PI', 'ND', 'OBS', 'RESP', 'A_PAGAR']].query('A_PAGAR > 0')
# final_apag = final_apag.applymap(str).replace(r'\.',',',regex=True)
# final_apag.to_csv('CONSOLIDADO/16{}061_APAG.csv'.format(gestão))


dados = dados.applymap(str).replace(r'\.',',',regex=True)
dados = dados.set_index("UG")
dados.to_csv('saldo_em_RP_16{}.csv'.format(gestão))

# gc = pygsheets.authorize(service_file='virtual-cubist-249800-c29651c665cb.json')
# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/10cSNEIfM9fcv9u_ZGXwOy9ffWrrcgnISIYlp_3wPZxA/edit#gid=0')
# if gestão == 0:
#     wks = sh[0]
#     wks.clear(start='A2')
#     wks.set_dataframe(dados, 'A1')
# else:
#     wks = sh[1]
#     wks.clear(start='A2')
#     wks.set_dataframe(dados, 'A1')