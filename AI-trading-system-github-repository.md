ai-trading-system/
│
├── .github/
│   ├── workflows/
│   │   ├── build.yml          # CI/CD for testing
│   │   └── deploy.yml         # AWS/GCP deployment
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
│
├── configs/
│   ├── bitget.yaml            # Exchange API credentials
│   ├── risk_params.yaml       # Max drawdown, position sizing
│   └── mifid_template.xml     # Compliance report schema
│
├── core/
│   ├── fpga/                  # Hardware-accelerated components
│   │   ├── hft_kernel.cpp     # Xilinx HLS code
│   │   └── Makefile           # Builds xclbin
│   │
│   ├── ai/
│   │   ├── train.py           # Model training script
│   │   └── predict.py         # Real-time inference
│   │
│   └── execution/
│       ├── bitget_connector.py
│       └── risk_engine.py
│
├── data/
│   ├── sample/                # Test market data
│   │   ├── btc_1m.csv
│   │   └── eurusd_tick.feather
│   └── live/                  # Real-time data storage
│       └── .gitkeep
│
├── models/                    # Pre-trained models
│   ├── lstm_crypto.h5
│   └── xgboost_forex.json
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── Dockerfile                 # Containerization
├── requirements.txt           # Python dependencies
├── README.md                  # Setup instructions
└── .gitignore