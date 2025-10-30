# Configuração do Projeto AdvisorIA Elite

## Pré-requisitos

- Node.js 18+ e npm
- Python 3.11+ com pip
- PostgreSQL (para produção) ou usar in-memory storage para desenvolvimento

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# Database Configuration (opcional para desenvolvimento)
DATABASE_URL=postgresql://user:password@localhost:5432/advisoria_db

# API Keys - Obrigatórias
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
PERPLEXITY_API_KEY=sua_chave_perplexity_aqui

# Server Configuration
PORT=5000
NODE_ENV=development
```

### Como obter as API Keys:

1. **Anthropic (Claude)**: https://console.anthropic.com/
2. **Perplexity**: https://www.perplexity.ai/settings/api

## Instalação

### 1. Dependências Node.js
```bash
npm install
```

### 2. Dependências Python
```bash
pip3 install fastapi uvicorn anthropic httpx pillow pydantic python-dotenv requests crewai crewai-tools asyncpg
```

Ou usando o arquivo de configuração:
```bash
cd python_backend
pip3 install -r requirements.txt
```

### 3. Configuração do Banco de Dados (Opcional)

Se você tiver PostgreSQL instalado:
```bash
npm run db:push
```

**Nota**: O backend Python usa armazenamento em memória por padrão para desenvolvimento, então o banco de dados não é obrigatório para começar.

## Execução

### Modo Desenvolvimento (Recomendado)

Inicie o servidor principal que gerencia ambos Node.js e Python:
```bash
npm run dev
```

Isso irá:
- Iniciar o servidor Node.js/Express na porta 5000
- Iniciar automaticamente o backend Python na porta 5001
- Configurar hot-reload para ambos

### Modo Manual (dois terminais)

**Terminal 1 - Backend Python:**
```bash
cd python_backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

**Terminal 2 - Servidor Node.js:**
```bash
npm run dev
```

## Acessar a Aplicação

Abra o navegador em: http://localhost:5000

## Resolução de Problemas

### Erro: "DATABASE_URL not found"
- O banco de dados é opcional para desenvolvimento
- Configure a variável `.env` ou ignore se estiver usando storage em memória

### Erro: "Module not found" (Python)
- Certifique-se de que todas as dependências Python foram instaladas
- Verifique se está usando Python 3.11+

### Erro: "Port 5000 already in use"
- Altere a porta no `.env`: `PORT=5001`
- Ou mate o processo que está usando a porta 5000

### Erro: "ANTHROPIC_API_KEY required"
- Você precisa de uma chave válida da Anthropic para usar os experts IA
- Obtenha em: https://console.anthropic.com/

## Estrutura do Projeto

```
AdvisorIAElite/
├── client/              # Frontend React + TypeScript
├── server/              # Backend Node.js/Express
├── python_backend/      # Backend Python/FastAPI (IA)
├── shared/              # Schemas compartilhados
└── attached_assets/     # Imagens e avatares
```

## Próximos Passos

1. Configure as variáveis de ambiente no arquivo `.env`
2. Execute `npm run dev` para iniciar
3. Acesse http://localhost:5000
4. Explore os experts de marketing e teste o chat!

## Suporte

Para mais informações, consulte a documentação completa ou abra uma issue no repositório.

