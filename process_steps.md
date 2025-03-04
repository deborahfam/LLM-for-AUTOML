## Fase 1: Definición del problema y preparación
- [ x ] Definir qué tipos de problemas de ML debe clasificar el sistema (clasificación, regresión y agrupamiento). 
- [ x ] Reunir datasets públicos (preguntas de Stack Overflow, Kaggle forums) que relacionen texto ambiguo con tareas de ML.
- [ x ] Usar GPT-4 para crear 100-300 ejemplos de preguntas ambiguas y sus etiquetas.
- [ x ] estructurar en formato JSON: {"input": "texto", "metadata": {"tipo_problema": "X", ...}}.
- [ ] Crear un esquema jerárquico (ej: "Problema → Tipo → Métricas → Datos requeridos").

## Fase 2: Diseño del sistema RAG
### Construir base de conocimiento:

- [ ] Recopilar documentos técnicos (ej: scikit-learn docs, artículos de arXiv sobre taxonomías de ML).

- [ ] Convertirlos a texto plano y dividir en chunks de nosecuantos tokens.

- [ ] Configurar vector DB

### Definir estrategia de retrieval:

- [ ] Semántico: Buscar chunks similares a la pregunta del usuario.

- [ ] Basado en keywords: Usar TF-IDF o BM25 para capturar términos clave (ej: "predecir" → regresión) (a lo mejor hacer esto en prompting sea conveniente)

- [ ] Integrar RAG con LLM

## Fase 3: Experimentación inicial
- [ ] Pruebas zero-shot: Evaluar con prompts directos (ej: "Clasifica esta pregunta: '¿Cómo saber si mis datos tienen patrones ocultos?'").

### Implementar RAG básico:

- [ ] Para cada pregunta, recuperar 3-5 chunks relevantes de la DB e inyectarlos como contexto en el prompt del LLM.
- [ ] Metricas de evaluación
- [ ] Análisis de errores: Identificar patrones (ej: confusion entre clasificación multi-clase y etiquetado multi-label).
- [ ] Optimizar retrieval: Probar combinaciones de embeddings + keywords (ej: ponderar 70% semántico + 30% BM25).


## Experimentar???
- Diálogo iterativo: Programar un flujo donde el LLM hace preguntas de clarificación (ej: "¿Tu objetivo es predecir categorías o valores numéricos?").