
class Board:
    def __init__(self) -> None:
        #   optional parameter for a specific setting of the pieces?
        self._fields = None  # do implementacji
        pass

    def get_field_by_location(location: tuple(int), self):
        for field in self.fields:
            if field.location == location:
                return field
        return None

    @property
    def fields(self):
        return self._fields
