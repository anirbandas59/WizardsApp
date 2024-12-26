# Automated Trading Application

## Overview

This project is an automated trading application designed for the **Zerodha Kite** platform. The application provides functionalities for:

- Automated login and session management.
- Buying and selling stocks based on predefined strategies.
- Stock screening and order generation.
- Risk management to minimize losses.

## Features

- **Auto-login**: Securely log in to the Zerodha platform with support for reconnection.
- **Stock Screening**: Implement strategies to identify stocks for trading.
- **Order Management**: Generate buy/sell orders based on strategy outputs.
- **Risk Management**: Set stop-loss and target prices to limit risk.
- **Real-Time Data**: Fetch live market data using WebSocket connections.
- **Environment Variables**: Securely store sensitive credentials in a `.env` file.

## Prerequisites

1. **Python** (Version 3.9 or higher recommended)
2. **Anaconda** (for environment management, optional but recommended)
3. Zerodha Kite Developer API access
   - [Zerodha Kite Connect API](https://kite.trade/)

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Set Up the Python Environment

```bash
conda create --name trading_env python=3.11
conda activate trading_env
conda install numpy pandas matplotlib sqlalchemy
conda install -c conda-forge kiteconnect websocket-client pyotp
```

### Step 3: Configure Environment Variables

1. Create a `.env` file in the project directory.
2. Add the following variables:

```text
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
ACCESS_TOKEN=your_access_token_here
USERNAME=your_Zerodha_username
PASSWORD=your_Zerodha_password
```

### Step 4: Run the Application

1. Launch the application:

```bash
python main.py
```

2. Monitor logs for real-time updates and trading decisions.

## Project Structure

```text
.
├── main.py                # Entry point for the application
├── strategies/            # Contains trading strategies
├── risk_management.py     # Implements risk management logic
├── data_fetcher.py        # Fetches market data via WebSocket
├── order_manager.py       # Handles order creation and execution
├── .env                   # Environment variables (ignored by Git)
├── requirements.txt       # Dependencies for the project
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Usage

- Update `strategies/` folder with custom trading logic.
- Adjust risk parameters in `risk_management.py`.
- Use `data_fetcher.py` to experiment with live data analysis.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the [GPL-3.0 License](LICENSE).

## Acknowledgements

- [Zerodha Kite Connect API Documentation](https://kite.trade/docs/)
