# alternativateatral
Web scraper for user reviews on Alternativa Teatral

## Usage

### Binary for Linux
Download the binary from the [Releases](https://github.com/epassaro/alternativateatral/releases) section and run:

```bash
./scrape <URL> -o <OUTPUT_FILE>
```

Example:
```bash
$ ./scrape https://www.alternativateatral.com/opiniones65140-sex-vivi-tu-experiencia
```

The results are saved in [JSONL](https://jsonlines.org/) format.

```json
{"date": "25/04/2025 17:08", "author": "Patricia", "rating": "5", "text": "Excelente! Súper recomendable, un espectáculo diferente!"}
```

### Python Script
Install the dependencies from `requirements.txt` and run:

```bash
$ python src/scrape.py <URL> -o <OUTPUT_FILE>
```

## Development
For development/packaging, create the Conda environment:

```bash
$ conda env create -f environment.yml
$ conda activate alternativa
```

## Limitations
- I suspect the Alternativa Teatral website has a limit of 999 pages per play. At 7 comments per page, this would represent a maximum of 6,988 reviews.
- Although the site allows rating a play in half-star increments, the script only captures the integer part of the rating.
- To enable packaging into a binary, SSL certificate verification was disabled. This has some security implications. An alternative would be to bundle `cacert.pem` alongside the binary.
