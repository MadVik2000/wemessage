# WeMessage

A scalable, real-time messaging platform that enables open group communications with distributed system architecture.

## Core Components

- Kafka for message streaming and event processing
- Redis for caching and real-time features
- Elasticsearch for message search and indexing
- Django for web backend
- Python 3.11+ runtime

## Features

- Open group messaging
- Real-time message delivery
- Text message support (with plans for media attachments)
- Scalable architecture for high throughput
- Distributed message processing

## Setup Instructions

### Prerequisites

- Python 3.11 or above
- Docker & Docker Compose
- PosgreSQL
- Git

### Quick Start

**Note:** All the commands below must be run from the base directory of the repository.

1. Clone the repository:
    ```bash
    git clone https://github.com/MadVik2000/wemessage
    ```

2. Set up Python virtual environment:

    - For Unix/macOS:
        ```bash
        python3 -m venv env
        ```
    - For Windows:
        ```bash
        python -m venv env
        ```

3. Activate virtual environment:

    - For Unix/macOS:
        ```bash
        source env/bin/activate
        ```
    - For Windows:
        ```bash
        env\Scripts\activate
        ```

4. Install dependencies:
    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```

5. Initialize pre-commit hooks:
    ```bash
    pre-commit install
    ```

6. Create env file
    ```bash
    cp .env.example .env
    ```

    > **Note** Do not forget to populate env values.

7. Copy commit message checker script to git folder:
    ```bash
    cp commit-msg .git/hooks/commit-msg
    ```

9. Start server
    - For development server
        ```bash
        python manage.py runserver 0.0.0.0:8000
        ```

    - For production ready server
        ```bash
        gunicorn --bind 0.0.0.0:8000 wemessage.wsgi
        ```

        > **Note**: Static files won't be served through gunicorn. Admin interface won't be usable.

10. Start Kafka consumer
    ```bash
    python manage.py start_message_consumer
    ```

### Docker Container

> **Info**: No need to setup any environment or dependencies. Just need .env
- Spin up Docker containers:
    ```bash
    docker-compose up -d
    ```

### Update local environment with GitHub

- Fetch Latest Info from remote
    ```bash
    git fetch -p
    ```

- Remove all local branch non-existent on GitHub (Merged)
    ```bash
    git branch -a --merged | grep -v '\*' | grep -v 'remotes' | xargs git branch -D
    ```
    > **Note**: This command only removed branches that have been merged to current branch

- Remove all local branch non-existent on GitHub (All)
    ```bash
    git branch -vv | grep 'origin/.*: gone]' | awk '{print $1}' | xargs git branch -D
    ```
    > **Note**: Be careful when using this command, as it permanently delete local branches without prompting for confirmation


