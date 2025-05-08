# alternativateatral
Scraping del sitio web de Alternativa Teatral

## Instalación
Las dependencias del script están listadas en el archivo `requirements.txt`. Se recomienda instalar utilizando un environment de Conda:

```bash
$ conda env create -f environment.yml
$ conda activate alternativa
```

## Uso
```bash
$ python src/scrape.py <URL> -o <ARCHIVO_DE_SALIDA>
```

**Ejemplo:**
```bash
$ python src/scrape.py https://www.alternativateatral.com/opiniones65140-sex-vivi-tu-experiencia
```

Los resultados se guardan en formato [JSONL](https://jsonlines.org/).

```json
{"date": "25/04/2025 17:08", "author": "Patricia", "rating": "5", "text": "Excelente! Súper recomendable, un espectáculo diferente!"}
```

## Limitaciones
- Sospecho que el sitio AlternativaTeatral tiene un límite de 999 páginas por obra. A 7 comentarios por página representaría un límite de 6988 reseñas.
- Si bien el sitio permite puntuar una obra en múltiplos de 1/2 estrella, el script sólo captura la parte entera de dicho puntaje.
