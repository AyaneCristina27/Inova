import unicodedata
from storages.backends.s3 import S3Storage


class SupabaseStorage(S3Storage):
    def get_valid_name(self, name):
        name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
        return super().get_valid_name(name)