import pandas as pd
#import datetime
# import pygsheets

url='http://www.portaltransparencia.gov.br/despesas/empenho/16009100001'
links = []
resp = []
gestão = input('INSIRA A GESTÃO PARA ANALISAR ( 0 ou 7 ) >>>  ')
dados = pd.read_csv('planilhao_ug_16{}091.csv'.format(gestão), sep= '\t', thousands='.', decimal=',')
for texto, teste in dados.iterrows():

    links.append(url+teste['NE'])

    pac = ['PAC/CITEX', 'PAC/DPI', 'DPI']
    ac_defesa = ['AC DEFESA', 'ACDEFESA']
    fa = ['ALMOX', 'ALMO', 'ALMX', 'GARAGEM', 'VIATURA', 'MECANICA', 'VEICULO', 'VEICULOS', 'ECT', 'CORREIOS',
          'CORREIO', 'ENERGIA', 'ELETRICA', 'ILUMINAÇÃO', 'ILUMINACAO', 'FA', 'DPC', 'AJUDA DE CUSTOS', 'BAGAGEM',
          'TELEGRAFOS', 'TIM S A', 'COMPANHIA DE SANEAMENTO AMBIENTAL DO DISTRITO FEDERAL',
          'VOETUR TURISMO E REPRESENTACOES LTDA',
          'FORTALEZA SERVICOS EMPRESARIAIS EIRELI']
    dci = ['CONTRATOS', 'CONTRATO', 'DCI', 'BRASIL DIGITAL TELECOMUNICACOES LTDA']
    dgsi = ['NIVA TECNOLOGIA DA INFORMACAO LTDA']
    salc = ['EMPRESA BRASIL DE COMUNICACAO S,A', 'EMPRESA BRASIL DE COMUNICACAO S.A']
    cta = ['ORACLE DO BRASIL SISTEMAS LTDA', 'GFS SOFTWARE E CONSULTORIA LIMITADA']
    for texto, teste in dados.iterrows():
        if any(x in teste['OBS'][:10] for x in ac_defesa):
            resp.append('AC DEFESA')
            continue
        if 'CTA' in teste['OBS'][:10]:
            resp.append('7ºCTA')
            continue
        if 'CDS' in teste['OBS'][:10]:
            resp.append('CDS')
            continue
        if 'CITEX' in teste['OBS'][:10]:
            # if any(x in teste['NOME_FAV'] for x in fa):
            #     resp.append('FA')
            #     continue
            # if any(x in teste['NOME_FAV'] for x in dgsi):
            #     resp.append('DGSI')
            #     continue
            # if any(x in teste['NOME_FAV'] for x in salc):
            #     resp.append('SALC')
            #     continue
            # if any(x in teste['NOME_FAV'] for x in dci):
            #     resp.append('DCI')
            #     continue
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
        # if any(x in teste['NOME_FAV'] for x in dci):
        #     resp.append('DCI')
        #     continue
        # if any(x in teste['NOME_FAV'] for x in cta):
        #     resp.append('7ºCTA')
        #     continue
        else:
            resp.append('--')
            print(teste['NE'])
            continue


dados.insert(15,'LINK_NE', links)
dados.insert(14,'RESP', resp)
# dados.insert(19, 'TEMPO', 0)
# dados.insert(26, 'APAG', 0)
for index, data in dados.iterrows():
    liquidado = data['LIQUIDADO']
    pago = data['PAGO']
    a_pag = liquidado - pago
    if liquidado > pago:
        dados['APAG'][index] = a_pag

print(dados.axes)
dados.set_index('UG', inplace=True)
final_aliq = dados.query('A_LIQUIDAR > 0')
final_aliq.applymap(str).replace(r'\.',',',regex=True)
final_aliq = final_aliq.to_csv('planilhao_ug_16{}091_ALIQ.csv'.format(gestão))
final_apag = dados.query('APAG > 0')
final_apag = final_apag.applymap(str).replace(r'\.',',',regex=True)
final_apag.to_csv('planilhao_ug_16{}091_A_PAG.csv'.format(gestão))
dados = dados.rename(columns={'EMISSAO': 'EMISSÃO', 'ALIQ':'A_LIQUIDAR', 'APAG': 'A_PAGAR'})
final_aliq = dados[['NE', 'EMISSÃO','PI', 'ND', 'OBS', 'RESP', 'A_LIQUIDAR']].query('A_LIQUIDAR > 0')
final_aliq = final_aliq.applymap(str).replace(r'\.',',',regex=True)
final_aliq.to_csv('CONSOLIDADO/16{}061_2021_ALIQ.csv'.format(gestão))

dados = dados.applymap(str).replace(r'\.',',',regex=True)
dados.to_csv('final_dummer.csv')
# gc = pygsheets.authorize(service_file='virtual-cubist-249800-c29651c665cb.json')
# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1x7OAj6hvUR-slnQR7to7pFZ_Ce9R4k1reHwjDVOZvFs/edit#gid=1659425859')
# wks = sh[0]
# wks.clear(start='A2')
# wks.set_dataframe(dados, 'A1')