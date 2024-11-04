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

1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```

2. Set up Python virtual environment:

    - For Unix/macOS:
        ```bash
        python3.11 -m venv env
        ```
    - For Windows:
        ```bash
        env\Scripts\activate
        ```

3. Install dependencies:
    ```bash
    pip install --no-cache-dir -r requirements.txt
    ```

4. Initialize pre-commit hooks:
    ```bash
    pre-commit install
    ```

5. Launch Docker services:
    ```bash
    docker-compose up -d
    ```