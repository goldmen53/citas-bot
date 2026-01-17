# Git Workflow para CITAS Bot

## Estructura de Ramas

```
main (v2.0 release branch)
  ├── develop (integration branch)
  │   ├── feature/modular-architecture (EN DESARROLLO)
  │   ├── feature/telegram-integration
  │   ├── feature/docker-orchestration
  │   ├── feature/proxy-rotation
  │   └── feature/captcha-handling
  │
  └── v1.0-legacy (código original archivado)
```

## Cómo Trabajar

### 1. Crear una nueva feature

```bash
# Desde develop
git checkout develop
git pull origin develop

# Crear rama de feature
git checkout -b feature/nombre-feature

# Hacer cambios...
git add .
git commit -m "Feature: descripción clara"

# Enviar a repositorio
git push origin feature/nombre-feature
```

### 2. Merge a develop

```bash
git checkout develop
git merge --no-ff feature/nombre-feature
git push origin develop
```

### 3. Release a main (v2.0)

```bash
git checkout main
git merge --no-ff develop
git tag -a v2.0 -m "Release v2.0: Modular architecture with Telegram integration"
git push origin main
git push origin v2.0
```

## Convenciones de Commit

Use formato: `Type: Descripción`

- `feat:` - Nueva feature
- `fix:` - Corrección de bug
- `refactor:` - Cambios sin alterar funcionalidad
- `docs:` - Cambios en documentación
- `test:` - Añadir tests
- `chore:` - Tareas mantenimiento

### Ejemplos

```bash
git commit -m "feat: Add modular visa architecture"
git commit -m "fix: Handle captcha blocking issue"
git commit -m "docs: Update README with Docker setup"
git commit -m "refactor: Extract common telegram handlers"
```

## Historial Actual

```
v1.0 (tag)
└── main: Add v1.0 legacy code
    └── Initial commit: Configuration and docs
```

## Próximos Pasos

1. `feature/modular-architecture` - Estructura base
2. `feature/telegram-integration` - Bot de Telegram
3. `feature/docker-orchestration` - Docker & Proxys
4. Merge to develop
5. Release v2.0 a main

## Restaurar v1.0 si es necesario

```bash
# Ver código v1.0
git checkout v1.0

# O desde cualquier rama
git show v1.0:v1.0-legacy/CITA_NIE.py
```
