![image](https://github.com/graylan0/purple-llama/assets/34530588/b4307250-984b-4043-bc1c-8956353557b6)

# Purple Llama Twitch Bot

## Description

Purple Llama is a Twitch bot built with FastAPI, SQLite, and the Llama language model. It listens to Twitch chat commands and generates text based on the prompts it receives. The bot also features rate-limiting, caching, and job hats for different text outputs.

## Features

- Twitch chat integration
- Text generation using the Llama language model
- SQLite database for caching replies
- Rate limiting for API requests
- Caching for generated text
- Job hats for different text outputs

## Prerequisites

- Python 3.8 or higher
- pip
- Twitch Developer Account for API token

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/purple_llama.git
    cd purple_llama
    ```

2. Install the required packages:

    ```bash
    pip install fastapi twitchio playwright llama_cpp cachetools sklearn ratelimit
    ```

3. Create a `config.json` file in the root directory and add your Twitch API token and initial channels:

    ```json
    {
        "TWITCH_TOKEN": "your_twitch_token_here",
        "INITIAL_CHANNELS": ["channel1", "channel2"]
    }
    ```

4. Optionally, you can also create a `job_hat_prompts.json` to customize job hat prompts.

## Usage

### Running the Bot

To run the bot, execute the following command:

```bash
purple_llama run
```

### Twitch Commands

- `!llama <prompt>`: Generates text based on the given prompt.

### API Endpoints

- `POST /generate/`: Generates a story based on the given prompt.

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is open-source and available under GPL2
