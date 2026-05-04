# Arquitetura e Decisões Técnicas - AlertaDoador

Este documento descreve as escolhas técnicas, padrões arquiteturais e práticas de desenvolvimento adotadas no projeto **AlertaDoador**.

## 1. Visão Geral
O projeto é dividido em duas aplicações principais (Frontend e Backend) que se comunicam via API REST. A infraestrutura e o ambiente de desenvolvimento são orquestrados utilizando Docker e Docker Compose.

---

## 2. Backend

O backend foi construído visando alta performance, tipagem forte e manutenção facilitada, adotando princípios de **Domain-Driven Design (DDD)** e **Arquitetura em Camadas**.

### 2.1. Tecnologias
- **Linguagem:** Python 3
- **Framework Web:** FastAPI (alta performance, assíncrono e tipado)
- **Servidor:** Uvicorn
- **ORM:** SQLAlchemy (mapeamento objeto-relacional)
- **Banco de Dados:** PostgreSQL (via `psycopg2-binary`)
- **Validação de Dados:** Pydantic

### 2.2. Arquitetura em Camadas e Padrões (DDD)
A estrutura do backend reflete uma separação clara de responsabilidades:
- **Models / Entities (`src/models/`):** Representam os objetos de domínio e o esquema do banco de dados.
- **DTOs (`src/dtos/`):** Modelos Pydantic usados para validação de entrada e saída, isolando as entidades internas da API pública.
- **Repositories (`src/repositories/`):** Camada de abstração para operações de banco de dados (Repository Pattern). Permite que a regra de negócio não conheça detalhes de implementação do ORM.
- **Services (`src/services/`):** Contém as regras de negócio centrais. Os serviços orquestram chamadas aos repositórios e outros serviços.
- **Controllers / Routers (`src/controllers/`):** Lidam exclusivamente com as requisições HTTP, injetam dependências e repassam o fluxo para a camada de Service.

### 2.3. Práticas de Desenvolvimento e TDD
- **Testes Automatizados (TDD):** Uso intensivo do `pytest` para testes unitários, de integração e E2E (`tests/test_donor_repository.py`, `test_notification_flow.py`, etc.). A estrutura permite testar a lógica isoladamente através de injeção de dependências ou mockando repositórios.
- **Linting e Formatação:** O projeto utiliza o **Ruff** (um linter e formatter extremamente rápido para Python) para garantir a padronização do código. Também utiliza `mypy` para checagem estática de tipos.

---

## 3. Frontend

O frontend é uma Single Page Application (SPA) reativa e moderna, focada em usabilidade e design responsivo.

### 3.1. Tecnologias
- **Linguagem:** JavaScript / JSX
- **Biblioteca Principal:** React 18
- **Roteamento:** React Router DOM v7
- **Estilização:** Tailwind CSS v3 (utilizado em conjunto com PostCSS para classes utilitárias e prototipação rápida)
- **Ícones:** `lucide-react`

### 3.2. Estrutura e Práticas
- **Componentização:** A interface é dividida em componentes reutilizáveis (como `DonorForm`, `DonorList`, `AlertHistory`, `StockLevels`, etc.), mantendo a lógica de UI encapsulada.
- **Test-Driven Development (TDD):** A suíte de testes utiliza as ferramentas nativas do ecossistema React (Jest e React Testing Library). Foram implementados testes automatizados para validar a renderização correta de componentes e o fluxo de dados (`__tests__/DonorsPage.test.jsx`, `AlertHistory.test.jsx`).

---

## 4. Infraestrutura, Docker e CI/CD

### 4.1. Docker e Docker Compose
Tanto o frontend quanto o backend são conteinerizados.
- **Dockerfiles:** Existem `Dockerfiles` dedicados na raiz de cada serviço (`backend/Dockerfile` e `frontend/Dockerfile`), garantindo isolamento de dependências e paridade entre o ambiente de desenvolvimento e produção.
- **Docker Compose:** Na raiz do repositório, um arquivo `docker-compose.yml` orquestra a subida de todos os serviços simultaneamente (Frontend, Backend e Banco de Dados PostgreSQL), simplificando o setup para novos desenvolvedores.

### 4.2. Integração Contínua (CI) com GitHub Actions
O projeto possui pipelines de CI configuradas através do **GitHub Actions** (`.github/workflows/lint.yml`).
- **Verificações Automáticas:** A cada Pull Request, a pipeline é acionada para rodar automaticamente o **Ruff Linter** e o **Ruff Formatter**.
- **Benefício:** Isso garante que nenhum código fora dos padrões de qualidade ou com erros de sintaxe seja integrado à branch principal, mantendo o código limpo e seguindo as melhores práticas da comunidade.
