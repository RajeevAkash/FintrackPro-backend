# FintrackPro Backend

A complete, production-ready REST API backend for the **FintrackPro** financial management web application. Built with **FastAPI**, **MongoDB Atlas**, **Motor (async)**, **JWT authentication**, **scikit-learn ML**, **ARIMA forecasting**, and **Gemini AI**.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | FastAPI 0.115 |
| Database | MongoDB Atlas |
| Async Driver | Motor 3.6 (async) |
| Authentication | JWT (python-jose) + bcrypt (passlib) |
| ML Classification | scikit-learn — TF-IDF + Naive Bayes / Random Forest |
| Forecasting | ARIMA (statsmodels) |
| AI Tips | Google Gemini 2.0 Flash (google-generativeai) |
| Validation | Pydantic v2 |
| Config | pydantic-settings + python-dotenv |

---

## Prerequisites

- Python 3.10+
- MongoDB Atlas account (free tier is fine)
- Gemini API key (from [Google AI Studio](https://aistudio.google.com/))

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/RajeevAkash/FintrackPro-backend.git
cd FintrackPro-backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` and fill in your values:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/fintrackpro?retryWrites=true&w=majority
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440
GEMINI_API_KEY=your-gemini-api-key
```

### 5. Train the ML model (optional)
See the **ML Model Training** section below.

### 6. Run the development server
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

---

## API Endpoints

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| `POST` | `/api/auth/register` | Register a new user | No |
| `POST` | `/api/auth/login` | Login and get JWT token | No |
| `GET` | `/api/transactions` | List all transactions (with filters & pagination) | Yes |
| `POST` | `/api/transactions` | Create a new transaction | Yes |
| `PUT` | `/api/transactions/{id}` | Update a transaction | Yes |
| `DELETE` | `/api/transactions/{id}` | Delete a transaction | Yes |
| `GET` | `/api/bills` | List all bills | Yes |
| `POST` | `/api/bills` | Create a new bill | Yes |
| `PATCH` | `/api/bills/{id}/pay` | Mark a bill as paid | Yes |
| `GET` | `/api/goals` | List all goals | Yes |
| `POST` | `/api/goals` | Create a new goal | Yes |
| `PATCH` | `/api/goals/{id}/progress` | Update goal progress | Yes |
| `GET` | `/api/analytics/summary` | Monthly income/expense summary | Yes |
| `GET` | `/api/analytics/categories` | Expense breakdown by category (pie chart) | Yes |
| `GET` | `/api/analytics/forecast` | ARIMA spending forecast for current month | Yes |
| `GET` | `/api/analytics/status` | Budget status and risk level | Yes |
| `POST` | `/api/ai/classify` | Classify a transaction category using ML | Yes |
| `GET` | `/api/ai/tips` | Get AI-generated savings tips (Gemini) | Yes |
| `GET` | `/health` | Health check | No |

### Query Parameters for `GET /api/transactions`
| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category name |
| `type` | string | Filter by type: `income` or `expense` |
| `from_date` | date (YYYY-MM-DD) | Start date filter |
| `to_date` | date (YYYY-MM-DD) | End date filter |
| `page` | int (default: 1) | Page number |
| `limit` | int (default: 20) | Items per page (max: 100) |

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MONGO_URI` | Yes | — | MongoDB Atlas connection string |
| `JWT_SECRET` | Yes | — | Secret key for signing JWT tokens |
| `JWT_ALGORITHM` | No | `HS256` | JWT signing algorithm |
| `JWT_EXPIRY_MINUTES` | No | `1440` | Token expiry in minutes (default 24h) |
| `GEMINI_API_KEY` | No | `""` | Google Gemini API key (for AI tips) |

---

## ML Model Training

The transaction category classifier uses **TF-IDF vectorization** + **Multinomial Naive Bayes** or **Random Forest** (whichever performs better on your dataset).

### Steps

1. Prepare your CSV dataset with:
   - A text column: `description`, `transaction_description`, `text`, `title`, or `narration`
   - A `category` column with category labels (e.g., `Food`, `Transport`, `Bills`, etc.)

2. Update the dataset path in `app/ml/train_classifier.py`:
   ```python
   DATASET_PATH = "path/to/your/dataset.csv"
   ```

3. Run the training script:
   ```bash
   python -m app.ml.train_classifier
   ```

4. The trained model is saved to `app/ml/artifacts/transaction_clf.pkl`.

5. The server will automatically load the model on startup. The `/api/ai/classify` endpoint will return a `503` error if the model has not been trained yet.

---

## Project Structure

```
app/
  main.py                    # FastAPI entry point, CORS, lifespan
  core/
    config.py                # Settings from .env
    security.py              # JWT, bcrypt, get_current_user dependency
    database.py              # Motor client, lifespan, get_database()
  api/
    deps.py                  # Common dependencies
    v1/
      router.py              # Aggregates all sub-routers
      auth.py                # /api/auth/*
      transactions.py        # /api/transactions/*
      bills.py               # /api/bills/*
      goals.py               # /api/goals/*
      analytics.py           # /api/analytics/*
      ai.py                  # /api/ai/*
  models/                    # Pydantic request/response schemas
  db/repositories/           # MongoDB query layer
  services/                  # Business logic
  ml/
    train_classifier.py      # ML training script
    artifacts/               # Stores .pkl model (not committed)
  utils/
    dates.py                 # Date helpers
    bson_helpers.py          # ObjectId serialization
```
