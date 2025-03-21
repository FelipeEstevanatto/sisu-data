import requests
import shutil
import csv
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}

# instituicoes_url = 'https://sisu-api.apps.mec.gov.br/api/v1/oferta/instituicoes' # 2020
# instituicoes_url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicoes' # 2021, 2022, 2023
instituicoes_url = 'https://sisu-api.sisu.mec.gov.br/api/v1/oferta/instituicoes' # 2024, 2025

year = '2025'
# They changed the endpoint for 2025 and I didn't bother to reverse engineer it lol
# or maybe it's just not available anymore

def write_to_file(directory, filename, filecontent):
    if directory:
        try: os.makedirs(directory)
        except: pass
    else:
        directory = ''

    with open(os.path.join(directory, filename), 'wb') as f:
        filecontent.raw.decode_content = True
        shutil.copyfileobj(filecontent.raw, f)

directory = os.path.abspath(os.path.join('..', '..', 'data', year, 'listagem_alunos_aprovados_csv'))

response = requests.get(instituicoes_url, headers=headers).json()
instituicoes = [r['co_ies'] for r in response]

# base_url = 'https://sisu.mec.gov.br/static/listagem-alunos-aprovados-portal/' # 2024
base_url = 'https://sisu.mec.gov.br/static/pdf/282/portal/chamada_regular/'

base_filename = 'listagem-alunos-aprovados-ies-{}-{}.csv'
for i, instituicao in enumerate(instituicoes):
        termo_adesao_url = instituicoes_url.replace('instituicoes', r'instituicao/{}').format(instituicao)
        response = requests.get(termo_adesao_url, headers=headers).json()

        termo_adesao = response['0']['co_termo_adesao']

        filename = base_filename.format(instituicao, termo_adesao)

        # url = base_url + filename # 2024
        url = base_url + instituicao + '/' + filename
        file = requests.get(url, headers=headers, stream=True)
        if file.status_code != 200:
            print(f'[{i+1:>4}/{len(instituicoes)}] [ERROR {file.status_code}] {filename}')
        else:
            write_to_file(directory, filename, file)
            print(f'[{i+1:>4}/{len(instituicoes)}] Saved to \'{os.path.abspath(filename)}\'')