from pathlib import Path
import keras
import tensorflowjs as tfjs


def export(
    model_path: str = "models/model_lts.keras", export_path: str = "models/export/lts"
):
    model = keras.saving.load_model(Path(model_path))

    tfjs.converters.save_keras_model(model, Path(export_path))


if __name__ == "__main__":
    export(model_path="models/model_5886.keras", export_path="models/export/5886")
