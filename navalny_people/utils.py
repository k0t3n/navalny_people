import os
import uuid


def upload_to(instance, filename):
    """
    Returns path to upload file as @string
    @string: app_name/model_name/4_uuid4_symbols/uuid4.ext
    """
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4(), ext)
    basedir = os.path.join(instance._meta.app_label,
                           instance.__class__.__name__.lower())
    return os.path.join(basedir, filename[:4], filename)
