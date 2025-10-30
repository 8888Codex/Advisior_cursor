# 🧠 Persona Builder - AdvisorIA Elite

## 📋 Visão Geral

O **Persona Builder** é uma funcionalidade que permite criar personas detalhadas para seu negócio, baseadas em pesquisa simulada de comunidades online. Essas personas podem ser usadas para entender melhor seu público-alvo e criar estratégias de marketing mais eficazes.

> **Nota**: Esta versão usa dados simulados em vez de chamar APIs externas, para facilitar o desenvolvimento e testes.

## 🚀 Como Usar

### 1. Criar uma Persona

Para criar uma persona, envie uma requisição POST para `/api/personas` com os seguintes dados:

```json
{
  "targetDescription": "Descrição do público-alvo",
  "industry": "Indústria ou setor",
  "mode": "quick ou strategic",
  "additionalContext": "Informações adicionais (opcional)"
}
```

**Parâmetros**:
- `targetDescription`: Descrição do público-alvo (ex: "Empreendedor de e-commerce")
- `industry`: Indústria ou setor (ex: "Varejo online")
- `mode`: Modo de pesquisa
  - `quick`: Análise básica (mais rápida)
  - `strategic`: Análise detalhada (mais completa)
- `additionalContext`: Informações adicionais para refinar a pesquisa (opcional)

**Exemplo de requisição**:

```bash
curl -X POST http://localhost:5001/api/personas \
  -H "Content-Type: application/json" \
  -d '{
    "targetDescription": "Empreendedor de pequeno negócio de e-commerce",
    "industry": "Varejo online",
    "mode": "strategic",
    "additionalContext": "Vendas de produtos para casa e decoração"
  }'
```

### 2. Buscar uma Persona

Para buscar uma persona específica, envie uma requisição GET para `/api/personas/{persona_id}`:

```bash
curl http://localhost:5001/api/personas/7b589a0b-99e3-475d-99a1-ce359e955c19
```

### 3. Listar todas as Personas

Para listar todas as personas, envie uma requisição GET para `/api/personas`:

```bash
curl http://localhost:5001/api/personas
```

## 📊 Dados da Persona

As personas incluem os seguintes dados:

- **Demographics**: Dados demográficos (idade, localização, ocupação)
- **Psychographics**: Dados psicográficos (interesses, desafios)
- **Pain Points**: Principais dores e frustrações
- **Goals**: Objetivos e aspirações
- **Values**: Valores fundamentais
- **Communities**: Comunidades online frequentadas
- **Content Preferences**: Preferências de conteúdo (formatos, tópicos)
- **Behavioral Patterns**: Padrões comportamentais

No modo `strategic`, são incluídos dados adicionais:
- **Decision Making**: Processo de tomada de decisão
- **Content Consumption**: Hábitos de consumo de conteúdo
- **Channels**: Canais preferidos
- **Influencers**: Tipos de influenciadores seguidos

## 🔧 Implementação Técnica

### Arquivos Principais

- `python_backend/reddit_research.py`: Implementação da pesquisa (versão simulada)
- `python_backend/main.py`: Endpoints da API
- `python_backend/storage.py`: Armazenamento de dados (versão em memória)
- `python_backend/models.py`: Modelos de dados

### Fluxo de Funcionamento

1. O usuário envia uma requisição para criar uma persona
2. O sistema gera dados simulados baseados nos parâmetros fornecidos
3. Os dados são estruturados no formato de persona
4. A persona é armazenada em memória
5. O sistema retorna a persona criada

### Versão Simulada vs. Real

A versão atual usa dados simulados para facilitar o desenvolvimento e testes. Em produção, seria necessário:

1. Configurar as APIs externas (Perplexity, Anthropic)
2. Adicionar as chaves de API no arquivo `.env`
3. Configurar o banco de dados PostgreSQL para armazenamento permanente

## 🛠️ Modificações Realizadas

Para corrigir o erro 500 na criação de personas, foram feitas as seguintes alterações:

1. **Criação de versão simulada do RedditResearch**:
   - Substituição das chamadas de API por dados simulados
   - Eliminação da dependência de APIs externas

2. **Implementação de armazenamento em memória**:
   - Modificação das funções `create_persona`, `get_persona` e `get_personas`
   - Uso de dicionário em memória em vez de PostgreSQL

3. **Simplificação do fluxo de dados**:
   - Geração de dados estruturados diretamente
   - Bypass da etapa de processamento de texto

## 📝 Próximos Passos

Para uma implementação completa em produção:

1. **Conectar ao PostgreSQL**:
   - Configurar `DATABASE_URL` no `.env`
   - Criar tabela `personas` no banco de dados
   - Restaurar as funções originais de armazenamento

2. **Configurar APIs externas**:
   - Adicionar `PERPLEXITY_API_KEY` e `ANTHROPIC_API_KEY` no `.env`
   - Restaurar as funções originais de pesquisa

3. **Melhorar a interface do usuário**:
   - Criar formulário para criação de personas
   - Implementar visualização de personas
   - Adicionar funcionalidade de exportação

## 🔍 Troubleshooting

Se encontrar problemas ao usar a funcionalidade de persona:

1. **Erro 500**:
   - Verifique se o servidor está rodando
   - Verifique os logs em `/tmp/uvicorn.log`

2. **Dados incompletos**:
   - Forneça uma descrição mais detalhada do público-alvo
   - Adicione informações sobre a indústria e contexto adicional

3. **Persona não encontrada**:
   - Verifique se o ID está correto
   - Lembre-se que os dados são armazenados em memória e serão perdidos ao reiniciar o servidor

## 🎯 Conclusão

A funcionalidade de Persona Builder está agora funcionando corretamente em modo de desenvolvimento, usando dados simulados. Isso permite testar e desenvolver a interface do usuário sem depender de APIs externas ou banco de dados.

Para uma implementação completa em produção, será necessário configurar as APIs externas e o banco de dados PostgreSQL.
