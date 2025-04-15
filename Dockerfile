# Image officielle Python
FROM python:3.10

# Installer curl et poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

# Ajouter poetry au PATH
ENV PATH="/root/.local/bin:$PATH"

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de projet
COPY pyproject.toml poetry.lock* ./

# Installer les dépendances sans créer d'environnement virtuel
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copier tout le reste du code
COPY . .

# Exposer le port
EXPOSE 8000

# Commande par défaut (modifiable si tu utilises gunicorn ou autre)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
