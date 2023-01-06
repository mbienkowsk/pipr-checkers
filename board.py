from field import Field


class Board:
    def __init__(self) -> None:
        #   optional parameter for a specific setting of the pieces?
        self._fields = None
        self._setup_fields()

    def get_field_by_location(location, self):
        for field in self.fields:
            if field.location == location:
                return field
        return None

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, new_fields):
        self._fields = new_fields

    def _setup_fields(self):
        self.fields = [[] for i in range(8)]
        for k in range(8):
            if k % 2 == 0:
                for i in range(8):
                    if i % 2 == 0:
                        self.fields[k].append(Field('white', i, k))
                    else:
                        self.fields[k].append(Field('black', i, k))
            else:
                for i in range(8):
                    if i % 2 == 1:
                        self.fields[k].append(Field('white', i, k))
                    else:
                        self.fields[k].append(Field('black', i, k))

    def __str__(self) -> str:
        #   to delete later, for testing purposes
        result = ''
        for row in self.fields:
            for field in row:
                result += str(field)
            result += '\n'
        return result



