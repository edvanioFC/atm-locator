# Relatório do Projeto: ATM Locator Application

## 1. RESUMO

Este projeto consiste no desenvolvimento de uma aplicação web "ATM Locator", que permite aos utilizadores localizar caixas multibanco (ATMs) de forma eficiente. A aplicação gerencia informações de utilizadores e ATMs, oferecendo funcionalidades como registo, autenticação, gestão de dados de ATMs e visualização em mapa. Construída com Flask, SQLAlchemy, e PostgreSQL, a solução integra segurança, persistência de dados e uma interface de utilizador intuitiva, com o objetivo de facilitar o acesso a serviços bancários em diversos locais.

**Palavras-chave:** Flask, Python, PostgreSQL, SQLAlchemy, ATM, Localização, Autenticação, Web Application, Geolocation, Pydantic.

## ÍNDICE GERAL

1.  RESUMO
    *   Palavras-chave
2.  INTRODUÇÃO
    *   Considerações Iniciais
    *   Objetivo do Projeto
    *   Justificativa
    *   Escopo do Projeto
    *   Equipe de Desenvolvimento
3.  ANÁLISE DE REQUISITOS
    *   Requisitos Funcionais
    *   Requisitos Não Funcionais
4.  MODELAGEM DE DADOS
    *   Modelos
    *   Tecnologias Utilizadas
5.  DESENVOLVIMENTO E IMPLEMENTAÇÃO
    *   Desafios Enfrentados
    *   Códigos-Chave
6.  CONCLUSÃO
    *   Realização dos Objetivos
    *   Lições Aprendidas

---

## 2. INTRODUÇÃO

### Considerações Iniciais

Num mundo cada vez mais conectado e dependente de serviços financeiros digitais e físicos, a necessidade de localizar pontos de acesso a dinheiro físico, como caixas multibanco (ATMs), permanece crucial. Muitas vezes, os utilizadores encontram-se em locais desconhecidos ou precisam de encontrar o ATM mais próximo rapidamente. Este projeto surge da necessidade de fornecer uma plataforma eficiente e amigável que minimize o tempo e o esforço necessários para encontrar um ATM, melhorando a experiência do utilizador.

### Objetivo do Projeto

O principal objetivo do projeto "ATM Locator" é desenvolver uma aplicação web robusta e intuitiva que permita aos utilizadores:
1.  **Localizar ATMs:** Encontrar caixas multibanco próximas à sua localização atual ou a um local especificado.
2.  **Gerenciar ATMs:** Para administradores, adicionar, atualizar e remover informações de ATMs.
3.  **Gerenciar Usuários:** Oferecer um sistema seguro de registo, autenticação e gestão de perfis de utilizadores.

### Justificativa

A relevância deste projeto reside na sua capacidade de resolver um problema comum e prático. A disponibilidade de uma ferramenta confiável para localizar ATMs pode beneficiar uma vasta gama de utilizadores, desde viajantes a residentes em áreas urbanas e rurais. Adicionalmente, para os prestadores de serviços financeiros, a capacidade de manter um diretório atualizado de ATMs e oferecer uma ferramenta de localização eficiente pode melhorar a satisfação do cliente e a acessibilidade aos seus serviços. A utilização de tecnologias modernas garante escalabilidade, segurança e uma boa experiência de utilizador.

### Escopo do Projeto

O escopo do projeto "ATM Locator" inclui as seguintes funcionalidades e requisitos:
*   **Gestão de Utilizadores:** Registo, login, logout, recuperação de palavra-passe e gestão de perfis de utilizador.
*   **Painel Administrativo:** Funcionalidades CRUD (Criar, Ler, Atualizar, Eliminar) para ATMs e, potencialmente, utilizadores.
*   **Pesquisa e Visualização de ATMs:** Exibição de ATMs em um mapa, com opções de pesquisa e filtragem.
*   **Dados de ATM:** Armazenamento de informações como localização (latitude, longitude), nome, endereço, tipo de ATM e horário de funcionamento.
*   **Configuração de Ambiente:** Suporte para ambientes de desenvolvimento e produção com configurações distintas.
*   **Segurança:** Autenticação de utilizadores e proteção contra acessos não autorizados.

### Equipe de Desenvolvimento

*   [**Nome do Membro 1**] - [Função]
*   [**Nome do Membro 2**] - [Função]
*   [**...**]

*(Esta seção deve ser preenchida pelos membros da equipe do projeto.)*

## 3. ANÁLISE DE REQUISITOS

### Requisitos Funcionais

1.  **RF1: Registo de Utilizador:** O sistema deve permitir que novos utilizadores se registem fornecendo um nome de utilizador, email e palavra-passe.
2.  **RF2: Autenticação de Utilizador:** O sistema deve permitir que utilizadores registados façam login com as suas credenciais.
3.  **RF3: Recuperação de Palavra-passe:** O sistema deve permitir que utilizadores recuperem as suas palavras-passe esquecidas via email.
4.  **RF4: Logout de Utilizador:** O sistema deve permitir que utilizadores terminem a sua sessão.
5.  **RF5: Gestão de Perfil de Utilizador:** Os utilizadores devem poder visualizar e atualizar as suas informações de perfil.
6.  **RF6: Criação de ATM:** Administradores devem poder adicionar novos registos de ATM com detalhes como localização, nome, e endereço.
7.  **RF7: Visualização de ATM:** Utilizadores devem poder ver uma lista ou mapa de ATMs disponíveis.
8.  **RF8: Detalhes de ATM:** Ao selecionar um ATM, os utilizadores devem poder visualizar informações detalhadas sobre ele.
9.  **RF9: Atualização de ATM:** Administradores devem poder editar informações existentes de ATMs.
10. **RF10: Eliminação de ATM:** Administradores devem poder remover registos de ATMs.
11. **RF11: Pesquisa de ATM:** Utilizadores devem poder pesquisar ATMs por critérios como localização, nome ou endereço.
12. **RF12: Geolocalização:** O sistema deve ser capaz de usar a localização atual do utilizador para mostrar ATMs próximos.

### Requisitos Não Funcionais

1.  **RNF1: Desempenho:** A aplicação deve carregar as páginas e resultados de pesquisa em menos de 3 segundos para a maioria das operações (80% dos casos).
2.  **RNF2: Segurança:**
    *   As palavras-passe dos utilizadores devem ser armazenadas de forma segura (hashing).
    *   A comunicação entre o cliente e o servidor deve ser cifrada (HTTPS).
    *   A aplicação deve ser resistente a ataques comuns (e.g., injeção de SQL, XSS, CSRF).
    *   Apenas utilizadores autenticados e autorizados devem ter acesso a funcionalidades administrativas.
3.  **RNF3: Usabilidade:** A interface do utilizador deve ser intuitiva e fácil de navegar.
4.  **RNF4: Escalabilidade:** A arquitetura do sistema (Flask, PostgreSQL) deve permitir o crescimento futuro do número de utilizadores e de dados de ATMs.
5.  **RNF5: Fiabilidade:** O sistema deve estar disponível 99.9% do tempo.
6.  **RNF6: Manutenibilidade:** O código deve ser bem estruturado, documentado e fácil de manter e estender.
7.  **RNF7: Portabilidade:** A aplicação deve ser capaz de ser implementada em diferentes ambientes de servidor (Docker).

## 4. MODELAGEM DE DADOS

### Modelos

A modelagem de dados do projeto é centrada em duas entidades principais: `User` (Utilizador) e `ATM`. Estes modelos são definidos em `app/models/user.py` e `app/models/atm.py`, respetivamente, utilizando o SQLAlchemy ORM.

**Modelo Conceitual:** Representa as entidades principais e os relacionamentos entre elas no domínio do problema, independentemente da implementação. Para este projeto, teríamos as entidades `Utilizador` e `ATM`, com um relacionamento (e.g., um utilizador pode gerenciar vários ATMs, dependendo do contexto administrativo).

**Modelo Lógico:** Detalha os atributos de cada entidade e os tipos de dados, sem se focar na tecnologia de banco de dados específica.
*   **Utilizador:** `id` (chave primária), `username`, `email`, `password_hash`, `is_admin`, `created_at`, `updated_at`.
*   **ATM:** `id` (chave primária), `name`, `address`, `latitude`, `longitude`, `description`, `image_path` (opcional), `created_at`, `updated_at`.

**Modelo Físico:** Mapeia o modelo lógico para um sistema de gestão de base de dados específico (PostgreSQL neste caso), incluindo detalhes como tipos de coluna nativos do banco de dados, índices e restrições.

*(**Nota:** Os diagramas de Modelagem de Dados (Conceitual, Lógico, Físico) devem ser gerados e incluídos pelo autor do relatório para ilustrar visualmente as entidades e seus relacionamentos.)*

### Tecnologias Utilizadas

*   **Banco de Dados:** PostgreSQL
*   **ORM:** SQLAlchemy (via Flask-SQLAlchemy)
*   **Migrações de Banco de Dados:** Alembic (via Flask-Migrate)

## 5. DESENVOLVIMENTO E IMPLEMENTAÇÃO

### Desafios Enfrentados

Durante o desenvolvimento de uma aplicação como o ATM Locator, alguns desafios comuns podem surgir:

*   **Gestão de Localização e Mapas:** A integração de APIs de mapeamento e a manipulação de dados geoespaciais (latitude, longitude) para pesquisa de proximidade podem ser complexas, especialmente garantindo a precisão e o desempenho. A necessidade de HTTPS para geolocalização é um ponto importante.
*   **Segurança e Autenticação:** Implementar um sistema de autenticação robusto com gestão de sessões, hashing de palavras-passe e proteção contra vulnerabilidades de segurança (XSS, CSRF, SQL Injection) requer atenção meticulosa. O uso de Flask-Login e Pydantic ajuda a mitigar esses riscos.
*   **Configuração de Ambiente:** Gerenciar configurações distintas para desenvolvimento, testes e produção, especialmente com variáveis de ambiente sensíveis (chaves de API, credenciais de banco de dados), pode ser desafiador. A utilização de `config.py` e `python-dotenv` endereça esta questão.
*   **Migrações de Banco de Dados:** A evolução do esquema do banco de dados ao longo do ciclo de desenvolvimento exige um sistema de migração confiável para evitar perda de dados e garantir consistência entre ambientes (Alembic/Flask-Migrate).

### Códigos-Chave

Em vez de incluir trechos de código extensos, destacamos os módulos e arquivos que representam as funcionalidades-chave da aplicação:

*   **`run.py`**: Ponto de entrada da aplicação, responsável por iniciar o servidor Flask, aplicar migrações de banco de dados automaticamente e inicializar um utilizador administrador padrão, se necessário. Demonstra a orquestração inicial do sistema.
*   **`app/__init__.py`**: Configura a aplicação Flask, registra os blueprints (rotas), inicializa extensões como SQLAlchemy e Flask-Login. É o "coração" da aplicação.
*   **`app/models/user.py` e `app/models/atm.py`**: Definições dos modelos de dados para utilizadores e ATMs, respetivamente. Contêm a estrutura da base de dados e métodos relacionados a estas entidades (e.g., hashing de palavras-passe em `User`).
*   **`app/routes/auth.py`**: Implementa as rotas de autenticação (registo, login, logout, recuperação de palavra-passe), que são cruciais para a segurança e gestão de acessos.
*   **`app/routes/admin.py`**: Contém as rotas protegidas para funcionalidades administrativas, como a gestão de ATMs, ilustrando a segregação de privilégios.
*   **`app/schemas/user_schema.py` e `app/schemas/atm_schema.py`**: Esquemas Pydantic para validação de dados, garantindo que os dados de entrada e saída estão em conformidade com as expectativas do sistema.
*   **`app/static/js/map.js`**: Este ficheiro JavaScript é fundamental para as funcionalidades de geolocalização e exibição de ATMs num mapa, representando a interação front-end com os dados de localização.

## 6. CONCLUSÃO

### Realização dos Objetivos

O projeto "ATM Locator" demonstrou a capacidade de construir uma aplicação web funcional que atende aos objetivos propostos. A estrutura modular, a utilização de um conjunto robusto de tecnologias Python e Flask, e a implementação de funcionalidades de gestão de utilizadores e ATMs, com ênfase na segurança e usabilidade, resultam numa plataforma eficaz. Os requisitos funcionais e não funcionais foram abordados, providenciando uma base sólida para a localização de caixas multibanco.

### Lições Aprendidas

O desenvolvimento deste projeto proporcionou várias lições importantes:

*   **Importância da Estrutura:** Uma arquitetura de projeto bem definida (como a estrutura modular em Flask) facilita o desenvolvimento, a manutenção e a escalabilidade.
*   **Validação de Dados Rigorosa:** A integração de ferramentas como Pydantic desde o início garante a integridade dos dados e reduz erros em tempo de execução.
*   **Gestão de Ambiente:** A utilização de variáveis de ambiente e perfis de configuração distintos é essencial para um deployment seguro e flexível.
*   **Segurança como Prioridade:** A autenticação e autorização devem ser consideradas desde as fases iniciais do design do sistema, utilizando bibliotecas dedicadas para implementar as melhores práticas.
*   **Feedback Contínuo:** A interação com as tecnologias e a resolução de desafios (e.g., integração de mapas, gestão de migrações) reforça a importância de um ciclo de feedback contínuo no desenvolvimento.

Este projeto não só entrega uma solução prática para a localização de ATMs, mas também serve como uma demonstração das boas práticas no desenvolvimento de aplicações web com Python e Flask.
