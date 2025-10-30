# 📦 Análise de Bundle e Performance

## Estatísticas Gerais

- **Total de Dependências**: 69 packages
- **Componentes Radix UI**: 27 componentes
- **Bibliotecas de Animação**: Framer Motion
- **Estado Global**: React Query (@tanstack/react-query)
- **Roteamento**: Wouter (leve!)

## Bibliotecas Pesadas Identificadas

### 🔴 CRÍTICO (Impact Alto)
1. **Framer Motion** (~60KB gzipped)
   - Usado em TODAS as páginas (AnimatedPage)
   - Animações complexas em múltiplos componentes
   - **Recomendação**: Considerar alternativas mais leves ou lazy load

2. **React Markdown** + remark-gfm (~40KB)
   - Usado apenas no ChatMessage
   - Pode ser lazy loaded

3. **27 Componentes Radix UI** (~150KB+ total)
   - Muitos podem não estar sendo usados
   - **Recomendação**: Tree-shaking audit

### 🟡 MÉDIO (Otimizável)
4. **Lucide Icons**
   - Import de ~30-40 ícones diferentes
   - **Recomendação**: Usar tree-shaking automático (já suportado)

5. **@tanstack/react-query** (~40KB)
   - Essencial, mas bem otimizado
   - ✅ Uso correto

### 🟢 BAIXO (OK)
6. **Wouter** (~2KB) - Excelente escolha vs React Router
7. **TailwindCSS** - Build-time, não afeta bundle
8. **Zod** - ~10KB, essencial para validação

## Problemas de Performance Identificados

### 1. Sem Code Splitting
```typescript
// App.tsx importa TODAS as páginas
import Home from './pages/Home';
import Landing from './pages/Landing';
import Experts from './pages/Experts';
import Chat from './pages/Chat';
// ... 11 páginas importadas estaticamente
```

**Impacto**: Bundle inicial inclui código de TODAS as páginas
**Solução**:
```typescript
// Lazy loading
const Home = lazy(() => import('./pages/Home'));
const Experts = lazy(() => import('./pages/Experts'));
```

### 2. AnimatedPage em Todas as Páginas
- Framer Motion carregado obrigatoriamente
- Animações complexas em cada transição
- **Sugestão**: Simplificar animações ou tornar opcional

### 3. React Query Cache
- Cache padrão: 5 minutos
- Experts são estáticos mas refetcham
- **Sugestão**: Aumentar staleTime para dados estáticos

```typescript
// Experts query
{
  queryKey: ["/api/experts"],
  staleTime: Infinity, // Experts não mudam frequentemente
}
```

### 4. Múltiplas Queries Paralelas
- Algumas páginas fazem 3-4 queries simultâneas
- Sem prefetch ou parallel batching
- **Sugestão**: Implementar prefetch em navegação

## Recomendações por Prioridade

### 🔴 ALTA PRIORIDADE
1. **Implementar Code Splitting** (Impacto: -40% bundle inicial)
   ```typescript
   const pages = {
     Home: lazy(() => import('./pages/Home')),
     Experts: lazy(() => import('./pages/Experts')),
     // ...
   };
   ```

2. **Lazy Load React Markdown** (Impacto: -40KB)
   ```typescript
   const ReactMarkdown = lazy(() => import('react-markdown'));
   ```

3. **Audit Radix Components** (Impacto: -20-30KB)
   - Remover componentes não usados
   - Verificar tree-shaking

### 🟡 MÉDIA PRIORIDADE
4. **Otimizar Framer Motion**
   - Reduzir complexidade de animações
   - Considerar CSS animations para casos simples

5. **Implementar Prefetching**
   - Prefetch de experts ao hover
   - Prefetch de chat ao clicar

6. **Otimizar React Query**
   - Aumentar staleTime para dados estáticos
   - Implementar cache persistence

### 🟢 BAIXA PRIORIDADE
7. **Comprimir Assets**
   - Otimizar imagens de avatares
   - Usar WebP quando disponível

8. **Service Worker**
   - Cache de assets estáticos
   - Offline support básico

## Estimativa de Impacto

| Otimização | Bundle Size Redução | Tempo Implementação |
|------------|---------------------|---------------------|
| Code Splitting | -200KB (~40%) | 2-3 horas |
| Lazy ReactMarkdown | -40KB | 30 min |
| Radix Audit | -20-30KB | 1-2 horas |
| Framer Simplification | -20KB | 3-4 horas |
| React Query Opt | Melhor caching | 1 hora |

**Total Potencial**: ~290KB redução (50-60% do bundle inicial)

## Bundle Size Estimado

**Atual (sem build de produção)**:
- Estimado: ~500-600KB (gzipped)
- First Load: ~400-500KB

**Com Otimizações**:
- Estimado: ~250-350KB (gzipped)
- First Load: ~200-250KB
- Subsequent: <100KB por página

## Conclusão

O projeto tem um bundle razoável para um app moderno, mas há oportunidades significativas de otimização:

✅ **Pontos Positivos**:
- Wouter (roteador leve)
- TailwindCSS (build-time)
- React Query (estado eficiente)

⚠️ **Pontos de Melhoria**:
- Code splitting ausente
- Framer Motion pesado
- Múltiplos componentes Radix (verificar uso)

**Recomendação**: Implementar code splitting URGENTE para reduzir ~40% do bundle inicial.
