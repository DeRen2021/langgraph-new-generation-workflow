# News Agent System

## Project Overview

The News Agent System is an automated news generation and management platform that uses artificial intelligence to collect information from the internet and produce high-quality news articles. The system utilizes the LangGraph workflow engine to coordinate various components, achieving full automation from topic search to content generation, image creation, and cloud storage.

## System Architecture

The system consists of the following main components:

### Core Modules
- **Web Search Module**: Searches internet resources based on topic keywords
- **Content Parsing Module**: Extracts valuable news content from web pages
- **Content Generation Module**: Generates high-quality news articles using GPT models
- **Image Generation Module**: Creates news images using DALL-E
- **Cloud Storage Module**: Stores images and articles in AWS cloud services

### Technology Stack
- **Python 3.10+**: Core programming language
- **LangGraph**: Workflow orchestration engine
- **OpenAI API**: Provides GPT and DALL-E model services
- **AWS DynamoDB**: Article content storage
- **AWS S3**: Image storage
- **aiohttp/trafilatura**: Asynchronous network requests and content extraction

## Installation Guide

### Prerequisites
- Python 3.10 or higher
- Valid OpenAI API key
- Valid AWS account and configuration

### Installation Steps

1. Clone the repository:
```bash
git clone [repository URL]
cd news_agent
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -e .
```

4. Configure environment variables:
Create a `.env` file and add the following content:
```
OPENAI_API_KEY=your_OpenAI_key
AWS_ACCESS_KEY_ID=your_AWS_access_key
AWS_SECRET_ACCESS_KEY=your_AWS_secret_key
AWS_REGION=your_AWS_region
AWS_BUCKET_NAME=your_S3_bucket_name
DYNAMODB_TABLE_NAME=your_DynamoDB_table_name
```

## Usage

### Processing a Single Topic News

```python
from node.lg_graph import chain

# Call the workflow with a specific topic
result = chain.invoke({"topic": "iphone 16e"})
```

### Viewing Generated News

Generated news articles will be stored in DynamoDB, and images will be stored in S3.

### Notes

- Ensure all workflow nodes are correctly configured
- Monitor API usage to avoid exceeding limits
- For long texts, you may need to adjust the merging strategy to avoid exceeding model limits

## Project Structure

```
news_agent/
├── config/           # Configuration files
├── node/             # LangGraph nodes and workflow definitions
│   ├── lg_node.py    # Function node implementation
│   ├── lg_graph.py   # Workflow graph definition
│   └── lg_state.py   # State definition
├── utils/            # Utility functions
│   ├── web_search.py # Web search functionality
│   ├── web_parse.py  # Web page parsing functionality
│   ├── pic_generator.py # Image generation functionality
│   ├── s3_api.py     # S3 storage interface
│   └── dynamodb_api.py # DynamoDB interface
├── .env              # Environment variable configuration
└── README.md         # Project documentation
```

## Troubleshooting

### Common Issues

1. **API Call Errors**
   - Check if the API key is valid
   - Confirm if you have reached the API usage quota

2. **Workflow Execution Errors**
   - Check if the state is passed correctly
   - Ensure that dependencies between nodes are correctly configured

3. **JSON Parsing Errors**
   - Reduce input content length
   - Add retry logic

4. **KeyError**
   - Check if the state dictionary contains the expected keys
   - Add default values or conditional checks

## Extended Features

1. **Support for More Topics**: Extend the system to support diverse news topics
2. **Improved Image Generation**: Use more sophisticated image generation prompts
3. **Add Frontend Interface**: Add a user interface to the system
4. **Content Recommendations**: Recommend news based on user interests
5. **Historical Tracking**: Track the development of specific topics over time

## Contribution Guidelines

Contributions in the form of issues and improvement suggestions are welcome. Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Submit changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 