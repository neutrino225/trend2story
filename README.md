# Trend2Story

A web application that transforms trending topics into engaging stories using AI. This project fetches trending topics from various sources (Google News, YouTube, and Google Trends) and generates creative stories based on user-selected themes.

## Features

- **Multiple Trend Sources**: Fetch trending topics from:
  - Google News
  - YouTube
  - Google Trends

- **Customizable Themes**: Generate stories in various themes:
  - Comedy
  - Tragedy
  - Sarcasm
  - Drama
  - Adventure
  - Horror
  - Romance
  - Mystery

- **User-Friendly Interface**: Simple and intuitive web interface built with Gradio
- **gRPC Support**: Efficient communication between services
- **REST API**: FastAPI-based endpoints for external integration

## Tech Stack

### Backend
- **Python 3.9+**: Core programming language
- **FastAPI**: High-performance web framework for building APIs
- **gRPC**: High-performance RPC framework for service communication
- **LangChain**: Framework for developing applications powered by language models
- **Ollama**: Local LLM deployment and management
- **Gradio**: Web interface for ML models

### AI/ML Components
- **LLM**: llama3.2:3b model for story generation
- **LangChain**: Orchestration of LLM operations
- **Ollama**: Local LLM deployment and management

### Data Processing
- **Selenium**: Web scraping
- **GNews**: Google News API integration

### Infrastructure
- **Docker**: Containerization
- **Conda**: Environment management

## Architecture

### System Components
1. **Web Interface (Gradio)**
   - User interaction layer
   - Trend source selection
   - Theme selection
   - Story display

2. **API Layer**
   - FastAPI REST endpoints
   - gRPC services
   - Request/response handling

3. **Data Collection**
   - Trend scraping from multiple sources
   - Data preprocessing and cleaning
   - Trend data storage

4. **Story Generation**
   - LLM integration via Ollama
   - Theme-based story creation
   - Content moderation

5. **Infrastructure**
   - Docker containers
   - Environment management
   - Service orchestration

### Data Flow
1. User selects trend source and theme
2. System fetches trending topics
3. Data is processed and formatted
4. LLM generates story based on trends and theme
5. Story is returned to user interface

## Setup

### Prerequisites
- Python 3.9+
- Conda (recommended for environment management)
- Docker (optional, for containerized deployment)
- Ollama with llama3.2:3b model installed
- Minimum 8GB RAM (16GB recommended)
- 4GB free disk space

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/trend2story.git
cd trend2story
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate nlp_project
```

3. Install Ollama and the required model:
```bash
# Install Ollama (follow instructions from https://ollama.com/)
ollama pull llama3.2:3b
```

## Usage

### Web Interface
1. Start the application:
```bash
python main.py
```

2. Open your web browser and navigate to `http://localhost:8001`

3. Select a trend source and theme, then click "Generate Story" to create your story

### API Usage
The application exposes both REST and gRPC endpoints:

#### REST API (FastAPI)
```bash
# Start the FastAPI server
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

#### gRPC Service
```bash
# Start the gRPC server
python -m app.grpc_server
```

### API Documentation
- REST API: `http://localhost:8000/docs`
- gRPC: See proto files in `app/proto/`

## Model Sources

### LLM Model
- **Model**: llama3.2:3b
- **Source**: Ollama
- **Size**: 3B parameters
- **Features**:
  - Local deployment
  - Fast inference
  - Good story generation capabilities
  - Theme understanding

### Trend Sources
1. **Google News**
   - Real-time news trends
   - Global coverage
   - Multiple categories

2. **YouTube**
   - Video trends
   - Popular content
   - Regional trends

3. **Google Trends**
   - Search trends
   - Interest over time
   - Related queries

## Limitations

### Technical Limitations
- Limited to 3B parameter model (may affect story quality)
- Local deployment requires sufficient hardware
- Rate limits on trend data sources
- Memory constraints for long stories

### Content Limitations
- May generate inappropriate content (requires moderation)
- Limited context window for long trends
- Potential bias in trend sources
- Language limitations (primarily English)

### Performance Considerations
- Story generation time varies (5-30 seconds)
- Trend fetching depends on source API availability
- High memory usage during story generation
- Network latency for trend data

## Project Structure

```
trend2story/
├── app/                    # Application modules
│   ├── scraper.py         # Trend scraping functionality
│   ├── llm.py             # Story generation using LLM
│   ├── api.py             # FastAPI endpoints
│   ├── grpc_server.py     # gRPC server implementation
│   └── proto/             # Protocol buffer definitions
├── main.py                # Main application entry point
├── environment.yml        # Conda environment configuration
├── Dockerfile             # Docker configuration
└── Dockerfile.web         # Web service Docker configuration
```

## Docker Support

The project includes Docker support for easy deployment:

- `Dockerfile`: Main application container
- `Dockerfile.web`: Web service container

To build and run with Docker:
```bash
docker build -t trend2story .
docker run -p 8001:8001 trend2story
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Gradio for the web interface
- FastAPI for the REST API framework
- gRPC for efficient service communication
- LangChain for LLM orchestration
- Ollama for local LLM deployment
- Various data sources for trend information
- llama3.2:3b model for story generation 