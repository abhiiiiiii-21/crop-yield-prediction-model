import logging

from src.model_pipeline import train_and_evaluate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        data_path = "data/crop_yield.csv"

        logger.info("Starting model training...")

        model_name, metrics = train_and_evaluate(data_path)

        logger.info(f"✅ Model trained successfully: {model_name}")
        logger.info(f"Metrics: {metrics}")

    except Exception as e:
        logger.exception(f"❌ Training failed: {e}")


if __name__ == "__main__":
    main()