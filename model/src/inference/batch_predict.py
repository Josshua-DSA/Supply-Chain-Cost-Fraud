"""Batch inference helpers."""


def batch_predict(model, frame):
    return model.predict(frame)
