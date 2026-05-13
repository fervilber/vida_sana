# Skill: Git — Control de Versiones del Proyecto

## Estrategia General

El agente distingue entre dos operaciones Git independientes:

| Operación | Cuándo | Automático |
|-----------|--------|------------|
| `git add + commit` | Al terminar cada operación significativa | ✅ Sí |
| `git push` | A petición del usuario, o al cerrar sesión | ❌ No automático |

**El commit local es barato y frecuente. El push a GitHub es bajo demanda.**

Esto evita generar tráfico de red innecesario en cada pequeño cambio, y permite
al usuario revisar los cambios antes de publicarlos en el remoto.

---

## Regla 1 — Commit Local (automático por el agente)

El agente hace `git add + commit` al finalizar cada operación **significativa**:

✅ **Hacer commit** al terminar:
- Procesamiento completo de una fuente (`/raw/` → `/wiki/`)
- Creación o edición de notas en `/wiki/`
- Nuevo diagrama Excalidraw guardado
- Revisión de mantenimiento con cambios efectivos
- Actualización de `index.md` o `log.md`

❌ **NO hacer commit** en pasos intermedios:
- Ediciones parciales de un archivo mientras aún trabaja en él
- Correcciones menores de formato durante una sesión activa
- Cambios de configuración menores en mismo turno que otros cambios

> **Regla práctica:** Si el agente está en medio de una tarea compleja
> (por ejemplo, procesar una fuente que crea 5 notas), hace **un solo commit**
> al terminar toda la tarea, no 5 commits intermedios.

---

## Regla 2 — Push a GitHub (bajo demanda)

El push **solo se ejecuta** en estos casos:

### A) El usuario lo pide explícitamente

Frases que activan el push:
- *«Sube los cambios a GitHub»*
- *«Sincroniza con GitHub»*
- *«Haz push»*
- *«Guarda en remoto»*
- *«Actualiza el repositorio»*

### B) Al cerrar una sesión de trabajo importante

Cuando el usuario indica que ha terminado la sesión, el agente propone el push:
> *«He completado las operaciones. Hay X commits locales pendientes de subir a GitHub.
> ¿Quieres que haga push ahora?»*

### C) Operaciones especialmente relevantes

Solo para cambios estructurales que convenga respaldar inmediatamente:
- Primera fuente procesada del proyecto
- Cambios en `.agentic/` (skills, workflows, templates)
- Cambios en `RULES.md` o `README.md`

En estos casos el agente **pregunta** antes de hacer push, no lo ejecuta sin confirmación.

---

## Convención de Mensajes de Commit

Formato estándar:
```
<tipo>(<ámbito>): <descripción breve en español>
```

### Tipos permitidos

| Tipo | Cuándo usarlo |
|------|---------------|
| `procesa` | Procesamiento de una fuente nueva en /raw/ |
| `wiki` | Creación o actualización de notas en /wiki/ |
| `diagrama` | Nuevo o actualizado diagrama Excalidraw |
| `raw` | Nuevo archivo añadido a /raw/ |
| `mantiene` | Revisión de mantenimiento, arreglo de enlaces |
| `config` | Cambios en .agentic/, scripts/, RULES.md |
| `docs` | Cambios en doc/ o README |

### Ámbito (opcional)
Nombre corto del tema o sección afectada: `fuentes`, `conceptos`, `log`, etc.

### Ejemplos
```bash
git commit -m "procesa(fuentes): añade resumen del video 'Intro a LLMs'"
git commit -m "wiki(conceptos): nueva nota sobre RAG y embedding"
git commit -m "diagrama: arquitectura del sistema LLM Wiki"
git commit -m "mantiene: corrige enlaces rotos y actualiza índice"
git commit -m "config: actualiza skill excalidraw con nuevos anti-patrones"
# Commit de sesión (agrupa varias operaciones menores):
git commit -m "wiki: sesión 2026-04-23 — 3 fuentes, 7 notas, mantenimiento"
```

---

## Procedimiento de Commit Local

```bash
# 1. Verificar qué hay para commitear
git status

# 2. Añadir todos los cambios
git add -A

# 3. Commit con mensaje descriptivo
git commit -m "<tipo>(<ámbito>): <descripción>"
```

Si `git status` dice "nothing to commit" → no hacer nada, informar al usuario.

---

## Procedimiento de Push

```bash
# Ver commits pendientes de push antes de subir
git log --oneline origin/main..HEAD

# Push al remoto
git push origin main
```

> Si la rama activa no es `main`, verificar con `git branch --show-current`.

---

## Manejo de Errores

### "nothing to commit"
→ Sin cambios pendientes. Informar y continuar.

### "rejected" en el push (conflicto con el remoto)
```bash
git pull --rebase origin main
git push origin main
```
Si persiste: NO forzar el push. Decir al usuario:
> *«Hay cambios en GitHub que no están en local. Revisa el conflicto con `git status`.»*

### "not a git repository"
→ Decir al usuario:
> *«El directorio no tiene git inicializado. ¿Ejecuto `git init && git remote add origin <URL>`?»*

### Error de autenticación
→ Decir al usuario:
> *«Git pide credenciales. Configura acceso con `gh auth login` o con clave SSH.»*

---

## Comandos de Referencia

```bash
# Commits pendientes de push
git log --oneline origin/main..HEAD

# Estado del repositorio
git status

# Historial reciente
git log --oneline -10

# Rama activa
git branch --show-current

# Diferencias sin commitear
git diff --stat

# Deshacer último commit (conserva cambios)
git reset --soft HEAD~1

# Remoto configurado
git remote -v

# Traer cambios remotos sin push
git pull --rebase origin main
```
