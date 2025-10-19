# Price Radar 📊

A powerful tool for Amazon product price analysis and competitor tracking, powered by AI.

## Features

- 🔍 **Product Scraping**: Easily fetch product details using ASIN
- 📊 **Competitor Analysis**: Automatically find and analyze competing products
- 🤖 **AI-Powered Insights**: Get intelligent market analysis using LLM
- 📈 **Price Tracking**: Monitor prices across different Amazon domains
- 🌍 **Multi-Region Support**: Works with multiple Amazon marketplaces (US, UK, CA, DE, FR, IT, AE, IN)

## Tech Stack

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python 3.13+
- **Database**: TinyDB (JSON-based)
- **AI/ML**: LangChain + GROQ
- **Data Collection**: Oxylabs Realtime API

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Chiru9604/Price-Radar.git
   cd Price-Radar
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```env
   OXYLABS_USERNAME=your_username
   OXYLABS_PASSWORD=your_password
   GROQ_API_KEY=your_groq_key
   ```

5. Run the application:
   ```bash
   streamlit run main.py
   ```

## Usage

1. Enter the ASIN of the Amazon product you want to analyze
2. Provide the zip/postal code for location-specific pricing
3. Select the Amazon domain (marketplace)
4. Click "Scrape Product" to fetch product details
5. Use "Analyze Competitors" to find competing products
6. Click "Analyze with AI" for detailed market insights

## Project Structure

```
├── main.py              # Streamlit UI and main application
├── src/
│   ├── db.py           # Database operations (TinyDB)
│   ├── llm.py          # AI analysis using LangChain
│   ├── oxylabs_client.py # Product data scraping
│   └── services.py     # Business logic and data processing
├── data.json           # Local database file
└── .env               # Environment variables
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit
- Powered by OpenAI and LangChain
- Data provided by Oxylabs