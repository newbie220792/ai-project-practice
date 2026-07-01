import pandas as pd
from flask import Flask, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import tempfile
import os
import logging


app = Flask(__name__)

DB_PATH = "/app/faces_db"

logging.basicConfig(
    filename="logs/app.log",  # Log file name
    level=logging.INFO,  # Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

@app.route("/recognize", methods=["POST"])
def recognize():
    if "image" not in request.files:
        return jsonify({"error": "no image"}), 400

    file = request.files["image"]
    img_bytes = file.read()

    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")

    try:
       cv2.imwrite(tmp.name, img)
    except Exception as e:
        tmp.close()
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
        logging.exception("Failed to write temp image: %s", e)
        return jsonify({"error": "failed to write temp image"}), 500

    try:
        result = DeepFace.find(
            img_path=tmp.name,
            db_path=DB_PATH,
            model_name="Facenet",
            detector_backend="retinaface",
            distance_metric="cosine",
            enforce_detection=False
        )

        # result should be a list-like where result[0] is a pandas.DataFrame
        if not result or len(result) == 0:
            logging.info("DeepFace.find returned no results")
            return jsonify({"name": "unknown", "confidence": 0})

        df = result[0]
        # safe-check dataframe
        if getattr(df, "empty", True):
            return jsonify({"name": "unknown", "confidence": 0})

        # ensure expected columns exist
        if "distance" not in df.columns or "identity" not in df.columns:
            logging.error("Unexpected result columns from DeepFace.find: %s", df.columns.tolist())
            return jsonify({"error": "unexpected result from recognition engine"}), 500

        identity = df.iloc[0]
        distance = identity.get("distance", None)
        identity_path = identity.get("identity", None)

        if distance is None or identity_path is None:
            logging.error("Missing distance/identity in result row")
            return jsonify({"error": "malformed recognition result"}), 500

        # normalize path separators and extract folder name (person id)
        person_name = os.path.normpath(identity_path).split(os.path.sep)[-2] if os.path.sep in os.path.normpath(identity_path) else os.path.basename(os.path.normpath(identity_path))

        if distance <= 0.68:
            logging.info("Match (distance=%.4f) -> %s", distance, person_name)
            confidence = float(max(0.0, min(1.0, 1.0 - distance)))
    
            # Verify confidence bounds
            personAttributes = DeepFace.analyze(img_path = tmp.name, 
                                   actions = ['age', 'gender', 'race', 'emotion'])
            
            # convert numpy/pandas types to plain python types so jsonify won't fail
            def _to_serializable(obj) -> object:
                # pandas objects
                try:
                    if isinstance(obj, (pd.DataFrame, pd.Series)):
                        return _to_serializable(obj.to_dict())
                except Exception:
                    pass

                if isinstance(obj, dict):
                    return {k: _to_serializable(v) for k, v in obj.items()}
                if isinstance(obj, (list, tuple)):
                    return [_to_serializable(v) for v in obj]
                # numpy scalars
                if isinstance(obj, np.generic):
                    return obj.item()
                return obj
            
            attrs = _to_serializable(personAttributes)
            return jsonify({"name": person_name, "confidence": confidence, "attributes": attrs})
        else:
            logging.warning("No match found (closest distance=%.4f)", distance)
            return jsonify({"name": "unknown", "confidence": 0})

    except Exception as e:
        logging.exception("Error during recognition: " + str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route("/test", methods=["GET"])
def test():
  return jsonify({"code": "success"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)