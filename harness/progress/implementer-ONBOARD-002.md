# implementer · ONBOARD-002

- **Fecha:** 2026-10-25
- **Veredicto:** ok

Implementado y verificado:
1) research find_papers --query 'LLM multi-agent software development agents' -> success=true, 7 papers únicos (antes 10 con el mismo trabajo repetido por DOI distinto). Fix en agents/tools/research_tool.py: la clave de dedupe es el título normalizado, no el DOI; test nuevo en agents/tests/test_research_tool.py (8 passed).
2) rag index_urls -> 3 URLs indexadas (2511.18467: 7 chunks; 2505.16086: 7; 2407.01489: 8). rag search --file_type url devuelve los papers con trust=externo y warning de contenido externo. Se descartó la URL 2506.05372 (violence detection, irrelevante) reconstruyendo el índice.
3) vault/01_PROYECTO/estado-del-arte.md: 7 fuentes con qué se toma y qué se descarta.
4) bootstrap suggest_agents: 21 términos sin cobertura léxica; revisados uno a uno, todos tienen dueño semántico o no son capacidades (tabla en estado-del-arte.md). Huecos aceptados: 0; no se crea agente especulativo (proporcionalidad del diseño).
5) agents.prompts_sync -> verde tras regenerar el prompt de research.
6) .gitignore: .rag-index/ y graphify-out/ (índices locales, no versionables).
