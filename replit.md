# WMS - Sistema de Gerenciamento de Armazém

## Visão Geral
Sistema completo de WMS (Warehouse Management System) desenvolvido com Python Flask no backend e Bootstrap 5 no frontend. O sistema oferece autenticação segura, painel administrativo e relatórios com visualizações gráficas.

## Funcionalidades Principais

### 1. Autenticação e Segurança
- Sistema de login com validação de usuário e senha
- Senhas armazenadas com hash seguro (Werkzeug)
- Gerenciamento de sessões com Flask-Login
- Controle de permissões por cargo (admin/user)

### 2. Dashboard
- Visão geral com estatísticas do sistema
- Cards informativos com métricas principais
- Lista de atividades recentes
- Alertas do sistema

### 3. Painel Administrativo
- Gerenciamento completo de usuários
- Criar, editar e excluir usuários
- Controle de cargos (Administrador/Usuário)
- Listagem com informações detalhadas

### 4. Relatórios
- Gráficos interativos com Chart.js
- Estatísticas de usuários
- Movimentações de estoque (últimos 7 dias)
- Estoque por categoria
- Tabela de atividades recentes

## Estrutura do Projeto

```
.
├── app.py                      # Aplicação Flask principal
├── models.py                   # Modelos do banco de dados (SQLAlchemy)
├── routes/                     # Módulos de rotas
│   ├── __init__.py            # Blueprints e importações
│   ├── auth.py                # Rotas de autenticação
│   ├── admin.py               # Rotas administrativas
│   └── reports.py             # Rotas de relatórios
├── templates/                  # Templates HTML
│   ├── base.html              # Template base
│   ├── login.html             # Página de login
│   ├── dashboard.html         # Dashboard principal
│   ├── admin.html             # Painel de usuários
│   ├── edit_user.html         # Edição de usuário
│   └── reports.html           # Página de relatórios
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   └── js/
│       ├── main.js            # JavaScript principal
│       └── reports.js         # Gráficos e relatórios
└── database.db                # Banco de dados SQLite
```

## Tecnologias Utilizadas

### Backend
- **Python 3.11**: Linguagem de programação
- **Flask**: Framework web
- **Flask-Login**: Gerenciamento de sessões
- **Flask-SQLAlchemy**: ORM para banco de dados
- **Werkzeug**: Hashing de senhas
- **SQLite**: Banco de dados

### Frontend
- **Bootstrap 5**: Framework CSS responsivo
- **Bootstrap Icons**: Ícones
- **Chart.js**: Biblioteca de gráficos
- **JavaScript**: Interatividade

## Credenciais Padrão

O sistema cria automaticamente dois usuários ao inicializar:

**Administrador:**
- Usuário: `admin`
- Senha: `admin123`
- Permissões: Acesso total ao sistema

**Usuário Comum:**
- Usuário: `user`
- Senha: `user123`
- Permissões: Acesso limitado (sem painel administrativo)

## Rotas Principais

### Autenticação
- `GET /` - Redireciona para login ou dashboard
- `GET/POST /login` - Página de login
- `GET /logout` - Logout do sistema
- `GET /dashboard` - Dashboard principal (requer login)

### Administração
- `GET /admin` - Listar usuários (apenas admin)
- `POST /admin/add_user` - Criar novo usuário
- `GET/POST /admin/edit_user/<id>` - Editar usuário
- `POST /admin/delete_user/<id>` - Excluir usuário
- `POST /admin/toggle_status/<id>` - Ativar/desativar usuário

### Relatórios
- `GET /reports` - Página de relatórios
- `GET /reports/api/user_stats` - API de estatísticas de usuários
- `GET /reports/api/stock_movements` - API de movimentações
- `GET /reports/api/stock_by_category` - API de estoque por categoria
- `GET /reports/api/recent_activities` - API de atividades recentes

## Modelos de Dados

### User
- `id`: Integer (Primary Key)
- `username`: String (80) - Único
- `email`: String (120) - Único
- `password_hash`: String (255)
- `name`: String (100)
- `role`: String (50) - 'admin' ou 'user'
- `created_at`: DateTime
- `is_active`: Boolean

## Recursos de Design

### Interface
- Design responsivo para desktop e mobile
- Sidebar de navegação fixa
- Navbar superior com informações do usuário
- Cards informativos com ícones
- Tabelas com hover effect
- Modals para formulários
- Alertas com auto-dismiss

### Cores e Temas
- Primária: Azul (#007bff)
- Sucesso: Verde (#28a745)
- Perigo: Vermelho (#dc3545)
- Aviso: Amarelo (#ffc107)
- Info: Azul claro (#17a2b8)

## Segurança Implementada

1. **Hashing de Senhas**: Todas as senhas são armazenadas com hash usando Werkzeug
2. **Proteção de Rotas**: Decorator `@login_required` protege rotas autenticadas
3. **Controle de Permissões**: Decorator `@admin_required` restringe acesso administrativo
4. **Secret Key**: Usado para assinar cookies de sessão
5. **Validação de Formulários**: Validação básica nos formulários

## Como Executar

O sistema já está configurado e rodando. O workflow "WMS Flask App" executa:

```bash
python app.py
```

O servidor inicia automaticamente em `http://0.0.0.0:5000`

## Próximas Funcionalidades (Fase 2)

- Gestão completa de estoque (produtos, categorias)
- Sistema de entrada e saída de mercadorias
- Código de barras e scanning
- Inventário com contagem cíclica
- Relatórios avançados com exportação PDF/Excel
- Sistema de notificações
- Auditoria de ações
- Dashboard com mais métricas

## Observações Importantes

- O banco de dados SQLite é criado automaticamente na primeira execução
- Os dados simulados nos relatórios são gerados aleatoriamente para demonstração
- O sistema usa Flask em modo debug - não recomendado para produção
- Para produção, use um servidor WSGI como Gunicorn ou uWSGI

## Data de Criação
01 de Novembro de 2024

## Status
✅ Sistema completo e funcional
✅ Todas as funcionalidades implementadas
✅ Interface responsiva
✅ Segurança implementada
