# alternativateatral
Scraping del sitio web de Alternativa Teatral

## Uso

### Binario para Linux
Descargar el binario de la sección [Releases](https://github.com/epassaro/alternativateatral/releases) y ejecutar:

```bash
./scrape <URL> -o <ARCHIVO_DE_SALIDA>
```

Ejemplo:
```bash
$ ./scrape https://www.alternativateatral.com/opiniones65140-sex-vivi-tu-experiencia
```

Los resultados se guardan en formato [JSONL](https://jsonlines.org/).

```json
{"date": "25/04/2025 17:08", "author": "Patricia", "rating": "5", "text": "Excelente! Súper recomendable, un espectáculo diferente!"}
```

### Script de Python
Instalar las dependencias de `requirements.txt` y ejecutar:

```bash
$ python src/scrape.py <URL> -o <ARCHIVO_DE_SALIDA>
```

## Desarrollo
Para el desarrollo/empaquetado es crear el _environment_ de Conda:

```bash
$ conda env create -f environment.yml
$ conda activate alternativa
```

## Limitaciones
- Sospecho que el sitio AlternativaTeatral tiene un límite de 999 páginas por obra. A 7 comentarios por página representaría un límite de 6988 reseñas.
- Si bien el sitio permite puntuar una obra en múltiplos de 1/2 estrella, el script sólo captura la parte entera de dicho puntaje.
- Para poder empaquetar el binario se desactivó la verificación de los certificados SSL. Esto tiene algunas implicaciones de seguridad. Una alternativa a esto sería incluir `cacert.pem` al binario mediante PyInstaller.
