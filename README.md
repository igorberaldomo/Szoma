esse é o projeto da Szoma de um aplicativo web

a pasta pycache tem o executável

a pasta desenho contem o desenho das relações entre tabelas do banco de dados

a pasta misc/cores/suvinil contém u código javacript que foi usado para gerar o json chamado 'pantone.json', esse código pegou a lista de cores hexadecimal encontrada no 'pantone-colors.json', que foi o json mais próximo de ser util encontrado, para rodar uma biblioteca chamada 'nearest-pantone', infelizmente não teve biblioteca análoga encontrada no python, também contém o leech da suvinil, e a versão em json por grupo de cor

a pasta padrão contem a tabela padrão do banco de dados

a pasta pantone contem  'pantone.json' a versão atual utilizada no código para encontrar o pantone mais pŕoximo em python

a pasta sqlscripts contém scripts que tem que ser digitados no workbench em caso de falha para restaurar as conecções entre tabelas

a pasta suvinil contém o arquivo 'suvinil.json' contendo as cores já processadas pela função fullprocess dentro da pasta utils que é a função que usa a extenção colorthief para pegar a cor do leach em /misc/png cores/.fullcolor que é a combinação detodas as outras cores retiradas as dupicatas, nisso ele vê a cor da suvinil mais procima em suvinil.json e a cor do pantone que estiver dentro do desvio e cadastra elas em um suvinil.jnson na pasta suvinil

a pasta suvinil é para guardar as cores da suvinil sendo usadas atualmente

a pasta utils tem todas as funções para criar os esqueletos da tabelas do sql e restaura-las , contem todas as versões utilizadas para procurar cores, pantones, formatar nomes, escrever jsons, formatar respostas para o front-end

.env contem o acesso ao sql

response.json é escrito com as informações requisitadas pelo método post, para ser lido no método get enviado para o frontend

