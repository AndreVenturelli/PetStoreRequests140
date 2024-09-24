# LIBS
import pytest
import json
import requests # framework que testa API's

from utils.utils import ler_csv


# 2- classe


pet_id = 450107701
pet_name = "Killua"
pet_category_id = 1
pet_category_name = "cat"
pet_tag_id = 1
pet_tag_name = "vacinado"



url='https://petstore.swagger.io/v2/pet'
headers={'Content-Type':'application/json'}


#2.2 funções/ métodos

def test_post_pet():
    #configura

    pet=open('./fixtures/json/pet1.json') #abre o arquivo json
    data=json.loads(pet.read())           #ler o conteudo e carrega como json em uma variavel data
    #resultado esperado estão nos atributos acima das funções


    response = requests.post(
        url= url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    #valida
    response_body = response.json()                         #cria uma variavel e carrega a resposta em formato json


    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] ==pet_name
    assert response_body['category' ]['name'] ==pet_category_name
    assert response_body['tags'][0]['name'] ==pet_tag_name

def test_get_pet():
     #configura
        #dado de entrada e saida / resultado esperado estão na seção antes das funções


        #executa
        response = requests.get(
            url=f'{url}/{pet_id}',
            headers=headers
        )


        #valida
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['name'] == pet_name
        assert response_body['category']['id'] == pet_category_id
        assert response_body['tags'][0]['id'] == pet_tag_id
        assert response_body['status'] == 'available'


def test_put_pet():
      #configura
      
    pet = open('./fixtures/json/pet2.json')
    data = json.loads(pet.read())

      #executa
    response = requests.put(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
      )


      #valida
    response_body = response.json()
    
    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] ==pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['category' ]['name'] ==pet_category_name
    assert response_body['tags'][0]['id'] == pet_tag_id
    assert response_body['tags'][0]['name'] ==pet_tag_name
    assert response_body['status'] == 'sold'


def test_delet_pet():
     #configura
     



     #executa
     response = requests.delete(
          url=f'{url}/{pet_id}',
          headers=headers,
          timeout=5
     )

     #valida
     response_body = response.json()

     assert response.status_code ==200
     assert response_body['code'] == 200
     assert response_body['type'] == 'unknown'
     assert response_body['message'] == str(pet_id)
      

@pytest.mark.parametrize('pet_id,category_id,category_name,pet_name,tags,status',
                         ler_csv('./fixtures/csv/pets.csv'))

def test_post_pet_dinamico(pet_id,category_id,category_name,pet_name,tags,status):
     
     pet = {}
     pet['id'] = int (pet_id)
     pet['category'] = {}
     pet['category']['id'] = int(category_id)
     pet['category']['name'] = category_name
     pet['name'] = pet_name
     pet['photoUrls'] = []
     pet['photoUrls'].append('')
     pet['tags'] = []

     tags = tags.split(';')
     for tag in tags:
          tag = tag.split('-')
          tag_formatada = {}
          tag_formatada['id'] = int(tag[0])
          tag_formatada['name'] = (tag[1])
          pet['tags'].append(tag_formatada)

     pet['status'] = status

     pet = json.dumps(obj=pet, indent=4)
     print('\n' + pet)



     response = requests.post(
          url=url,
          headers=headers,
          data=pet,
          timeout=5
      )

     response_body = response.json()
     assert response.status_code == 200
     assert response_body['id'] == int(pet_id)
     assert response_body['name'] == pet_name
     assert response_body['status'] == status

     