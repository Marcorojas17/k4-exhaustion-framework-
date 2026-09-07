# Anteproyecto de Tesis - K4 Exhaustion Framework

**Alumno:** Marco Rojas (@Marcorojas17) - Toluca, EdoMex
**Repositorio:** https://github.com/Marcorojas17/k4-exhaustion-framework-
**Demo Live:** https://marcorojas17.github.io/k4-exhaustion-framework-/
**Tema:** Criptoanálisis aplicado a Kryptos K4

## Título propuesto
Desarrollo de un framework de criptoanálisis por exhaustión para el cifrado Kryptos K4 mediante llaves derivadas del Reloj de Berlín y filtrado estadístico.

## Planteamiento del problema
La escultura Kryptos (CIA, 1990) contiene 4 mensajes, 3 resueltos, K4 permanece sin descifrar por 35 años. La pista oficial es BERLINCLOCK. No existe herramienta open-source que sistematice la búsqueda.

## Objetivo General
Desarrollar y validar un framework automatizado que excluya sistemáticamente familias de cifrado para K4 usando 9 assets matriciales (0-8.png) derivados del Reloj de Berlín.

## Objetivos Específicos
1. Implementar parser de imágenes 0-8.png a bits y matrices mod26 (ya hecho: image_parser.py)
2. Implementar generador de assets neon sincronizado base-0 (ya hecho: generate_assets.py)
3. Integrar filtros chi² e Índice de Coincidencia para descartar texto no-inglés
4. Publicar visualizador web neon matrix para reproducibilidad (ya live en Pages)
5. Ejecutar sweep de 14,100+ combinaciones con CI automatizado

## Hipótesis
Es posible reducir el espacio de claves de K4 mediante exhaustión guiada por topología Berlin Clock, descartando >90% de configuraciones con criterios estadísticos.

## Justificación
Aportación original a ciberseguridad y criptografía histórica. Metodología aplicable a otros cifrados sin resolver. Primer laboratorio visual público de K4 en México. Potencial de publicación en arXiv y beca CONAHCYT.

## Metodología
Python + PIL + NumPy + GitHub Actions + GitHub Pages. Validación: parser 9 keys OK, test de bits Berlín 23:51.

## Cronograma (4 meses)
Mes 1: Paper + TESIS.md (hecho)
Mes 2: Sweep completo y logs
Mes 3: Redacción capítulos 1-3
Mes 4: Defensa + publicación

## Financiamiento requerido
Servidor para sweep profundo + dominio + publicación. Abierto a sponsoreo vía GitHub Sponsors.

Firma asesor: ________________________
