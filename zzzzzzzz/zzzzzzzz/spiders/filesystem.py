

class FileCsv(object):
    filename = 'travels.csv'

    def __init__(self, *args, **kwargs):

        with open(self.filename, 'w') as f:
            f.write(
                'Fecha de Extracción,Hora de Extracción,Fuente,'
                'Fecha de Salida,Hora de Salida,Marca,Origen,'
                'Destino,Precio Base,Precio Promoción,Categoria,'
                'Tipo de Tramo\n'
            )

    def add_row(self, data):
        text = '{},{},{},{},{},\"{}\",\"{}\",\"{}\",{},{},\"{}\",\"{}\"\n'.format(
            data["date_process"],
            data["time_process"],
            data["id_sitio"],
            data["departure_date"],
            data["departure_time"],
            data["brand"],
            data["origin"],
            data["destination"],
            data["base_price"],
            data["promo_price"],
            data["service_type"],
            data["route_type"],
        )
        with open(self.filename, 'a') as f:
            f.write(text)
