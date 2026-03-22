import logging
import os

logger = logging.getLogger(__name__)

_model = None

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "artifacts", "transaction_clf.pkl")


def _load_model():
    global _model
    try:
        import joblib
        model_path = os.path.abspath(_MODEL_PATH)
        if os.path.exists(model_path):
            _model = joblib.load(model_path)
            logger.info("ML classifier model loaded successfully.")
        else:
            logger.warning(
                "ML model not found at %s. Run `python -m app.ml.train_classifier` to train it.",
                model_path,
            )
    except Exception as e:
        logger.error("Failed to load ML model: %s", e)
        _model = None


_load_model()


def predict_category(title: str, description: str) -> str:
    from fastapi import HTTPException, status

    if _model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model not trained yet. Run `python -m app.ml.train_classifier` first.",
        )
    text = f"{title} {description or ''}".strip().lower()
    prediction = _model.predict([text])
    return str(prediction[0])
