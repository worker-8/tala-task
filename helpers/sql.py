def create_fields_values_params(data: dict) -> tuple:
    fields = ",".join(data.keys())
    values = ",".join(["?" for _ in data.values()])
    params = list(data.values())
    return (fields, values, params)