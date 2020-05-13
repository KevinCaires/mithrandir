# Mithrandir

### Proposta

A API mithrandir foi criada com a intenção de fornecer suporte à criação e manutenção de ordens de serviço para o aplicativo `Startup Me`, aplicativo a ser apresentado para o TCC nas Faculdades Integradas Camões. Nessa API é utilizado os FrameWorks Django e Graphql.

### Compatível com o sistemas
![Linux Badges](https://img.shields.io/badge/OS-Linux-black)

### Linguagem

![Python Badge](https://img.shields.io/badge/Python-3.6.9-black)

### Dependências

As dependencias e pacotes necessários estão contidas no arquivo `dev.txt` dentro do diretório requirements.

### Instalação

| Ambiente Linux |
|----------------|
| 1° - Crie um ambiente virtual destinado ao projeto e acesse o mesmo. |
| 2° - Com o ambiente criado você pode instalar os pacotes com `make install`. |
| 3° - Faça as migrações necessárias com `make migrate`. |
| 4° - Rode o projeto com o comando `make run`. |
| A API estará rodando no localhost porta 6006 e pode ser acessada diretamente do navegador ou então programas como insomnia. As `queries` para consulta e `mutations` para criação e modificação dos objetos está na nossa [wiki](https://github.com/KevinCaires/mithrandir/wiki). |
