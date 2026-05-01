from services.dummy_model import DummyReturnModel


MODEL_REGISTRY = {
    "Dummy Return Model": DummyReturnModel,
}


def get_available_models() -> list[str]:
    """Return available model names."""
    return list(MODEL_REGISTRY.keys())


def get_model_class(model_name: str):
    """Return model class from registry."""
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model: {model_name}")

    return MODEL_REGISTRY[model_name]