class Subject:
    """TODO"""

    def __init__(
        self,
        schema_type: str = None,
        subject: str = None,
        registry_id: int = 0,
        version: int = 0,
        schema: dict = None):

        self.schema_type = schema_type
        self.subject = subject
        self.registry_id = registry_id
        self.version = version
        self.schema = schema or {}

    def __str__(self):
        return f"type={self.schema_type}, subject={self.subject}, id={self.registry_id}, " \
               f"version={self.version}  => {str(self.schema)}"
