# Evolution API - MCP Bridge

A FastAPI bridge that connects Evolution API with MCP (Model Context Protocol) servers.

## Features

- Receive messages from Evolution API via webhooks
- Process messages through MCP server
- Send responses back via Evolution API
- Conversation session management
- Redis caching for common messages
- Docker containerization
- Code quality tools (Ruff, Black, Pylint, MyPy)
- Comprehensive test coverage with pytest
- GitHub Actions CI/CD

## Development

### Prerequisites

- Python 3.11+
- Docker (optional)
- Redis

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for development
```
Enable the plugin: Run rabbitmq-plugins enable rabbitmq_management on your server.