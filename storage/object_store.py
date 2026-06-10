from pathlib import Path


class ObjectStore:
    """Filesystem-backed object store adapter for local dev/tests.

    Object keys are MinIO/S3-compatible strings; bytes are persisted under `.object_store/`.
    """

    def __init__(self, root: str = '.object_store'):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    async def put(self, object_key: str, data: bytes) -> str:
        file_path = self.root / object_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(data)
        return object_key
