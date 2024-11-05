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

6. Copy commit message checker script to git folder:
    ```bash
    cp commit-msg .git/hooks/commit-msg
    ```

6. Launch Docker services:
    ```bash
    docker-compose up -d
    ```