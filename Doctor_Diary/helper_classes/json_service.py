import datetime
import services.model_entities


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    elif isinstance(obj, services.model_entities.Patient):
        return {
            'number': obj.number,
            'firstname': obj.firstname,
            'lastname': obj.lastname
        }
    elif isinstance(obj, services.model_entities.Appointment):
        return {
            'patient_number': obj.patient_number,
            'date': obj.date,
            'time': obj.time,
            'description': obj.description
        }
    raise TypeError(f"Type {type(obj)} is not serializable")


def json_deserializer(obj):
    if 'date' in obj:
        obj['date'] = datetime.datetime.strptime(obj['date'], '%Y-%m-%d').date()

    if 'time' in obj:
        obj['time'] = datetime.datetime.strptime(obj['time'], '%H:%M:%S').time()

    return obj
