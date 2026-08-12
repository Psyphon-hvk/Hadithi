from whitenoise.storage import CompressedManifestStaticFilesStorage


class SilentFileManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False