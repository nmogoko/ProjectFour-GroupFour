import enum


class SerializerMixin:
    # def serialize(self):
    #     return {column_name.name: getattr(self, column_name.name)for column_name in self.__table__.columns}
    def serialize(self):
        serialized_data = {}
        for column_name in self.__table__.columns:
            value = getattr(self, column_name.name)
            # Check if the value is an instance of an Enum
            if isinstance(value, enum.Enum):
                # Get the value of the enum
                serialized_data[column_name.name] = value.value
            else:
                # Otherwise, use the value as is
                serialized_data[column_name.name] = value
        return serialized_data
