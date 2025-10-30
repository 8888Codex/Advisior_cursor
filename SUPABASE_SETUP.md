# 🗄️ Configuração do Supabase - Guia Completo

## 📋 Checklist Rápido

- [ ] Criar projeto no Supabase
- [ ] Copiar a Connection String
- [ ] Adicionar DATABASE_URL no .env
- [ ] Executar migrations (npm run db:push)
- [ ] Testar a conexão

---

## 1️⃣ Criar Projeto no Supabase

### Passo a Passo:

1. **Acesse:** https://supabase.com/
2. **Login/Cadastro:** Crie uma conta ou faça login
3. **Novo Projeto:** Clique em "New Project"
4. **Preencha os dados:**
   ```
   Name: advisoria-ia-elite
   Database Password: [CRIE UMA SENHA FORTE - ANOTE!]
   Region: South America (São Paulo) - ou mais próxima
   Pricing Plan: Free
   ```
5. **Crie o projeto:** Clique em "Create new project"
6. **Aguarde:** ~2 minutos para provisionar

---

## 2️⃣ Obter Connection String

1. No painel do Supabase, vá em **Settings** ⚙️ (menu lateral esquerdo)
2. Clique em **Database**
3. Role até **"Connection string"**
4. Selecione a aba **"URI"** (não Transaction, não Session)
5. Copie a string que aparece:

```
postgresql://postgres.xxxxxxxxxxxxx:[YOUR-PASSWORD]@xxxx.pooler.supabase.com:6543/postgres
```

### ⚠️ IMPORTANTE:
Substitua `[YOUR-PASSWORD]` pela senha que você criou no passo 1!

**Exemplo:**
Se sua senha é `MinhaSenha123`, ficaria:
```
postgresql://postgres.abcdef12345:MinhaSenha123@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

---

## 3️⃣ Adicionar no arquivo .env

Abra o arquivo `.env` na raiz do projeto e localize:

```bash
# ===========================================
# BANCO DE DADOS (Opcional para desenvolvimento)
# ===========================================

# DATABASE_URL=postgresql://user:password@localhost:5432/advisoria_db
```

**Descomente e substitua** pela sua connection string do Supabase:

```bash
# ===========================================
# BANCO DE DADOS - SUPABASE
# ===========================================

DATABASE_URL=postgresql://postgres.abcdef:SuaSenha@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

### 💾 Salve o arquivo .env

---

## 4️⃣ Criar Tabelas no Banco

Agora que o `.env` está configurado, execute:

```bash
npm run db:push
```

Este comando irá:
- ✅ Conectar ao Supabase
- ✅ Criar as tabelas: `users`, `experts`, `conversations`, `messages`
- ✅ Configurar os índices e relacionamentos

### ✅ Saída Esperada:

```
Pushing schema changes to database...
✔ Successfully pushed schema to database
```

---

## 5️⃣ Verificar no Supabase (Opcional)

1. Volte ao painel do Supabase
2. Clique em **"Table Editor"** no menu lateral
3. Você deve ver as tabelas criadas:
   - `users`
   - `experts`
   - `conversations`
   - `messages`

---

## 🚀 Iniciar o Projeto

Agora que tudo está configurado:

```bash
npm run dev
```

Acesse: **http://localhost:5000**

---

## 🔍 Verificar Conexão com o Banco

Para testar se a conexão está funcionando:

```bash
node -e "require('dotenv').config(); console.log('DATABASE_URL configurada:', process.env.DATABASE_URL ? '✅ Sim' : '❌ Não')"
```

---

## ❓ Problemas Comuns

### Erro: "connection refused" ou "timeout"
- ✅ Verifique se a senha no DATABASE_URL está correta
- ✅ Confirme se não há caracteres especiais que precisam ser encoded
- ✅ Certifique-se de usar a URI correta (porta 6543 para pooler)

### Erro: "password authentication failed"
- ✅ A senha está correta no DATABASE_URL?
- ✅ Tente resetar a senha no Supabase (Settings > Database > Reset password)

### Erro: "DATABASE_URL not found"
- ✅ O arquivo .env está na raiz do projeto?
- ✅ A linha DATABASE_URL está descomentada (sem #)?
- ✅ Reinicie o terminal após editar o .env

### Caracteres Especiais na Senha
Se sua senha tem caracteres especiais (@, #, %, etc), você precisa encodá-los:

```
@ = %40
# = %23
$ = %24
% = %25
& = %26
```

**Exemplo:**
- Senha: `Minha#Senha@123`
- Encoded: `Minha%23Senha%40123`

---

## 💡 Dicas

1. **Plano Gratuito Supabase:**
   - 500 MB de armazenamento
   - 2 GB de transferência/mês
   - Suficiente para desenvolvimento e pequenos projetos

2. **Backup:**
   - Supabase faz backups automáticos diários
   - Acesse em: Database > Backups

3. **Segurança:**
   - ❌ Nunca faça commit do arquivo .env
   - ✅ Use senhas fortes
   - ✅ Ative 2FA na sua conta Supabase

---

## 📚 Links Úteis

- **Supabase Dashboard:** https://app.supabase.com/
- **Documentação:** https://supabase.com/docs
- **Drizzle ORM Docs:** https://orm.drizzle.team/

---

## ✅ Checklist Final

Antes de iniciar o projeto, confirme:

- [ ] ✅ ANTHROPIC_API_KEY configurada no .env
- [ ] ✅ PERPLEXITY_API_KEY configurada no .env
- [ ] ✅ DATABASE_URL do Supabase configurada no .env
- [ ] ✅ Executei `npm run db:push` com sucesso
- [ ] ✅ Tabelas criadas no Supabase

Se todos os itens estiverem ✅, execute:

```bash
npm run dev
```

**Pronto! Seu projeto está rodando!** 🎉

