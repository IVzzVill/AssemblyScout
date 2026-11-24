"""Contrato serial estable entre la Raspberry Pi y el ESP32.

Cada mensaje ocupa una sola línea JSON UTF-8. La Raspberry envía órdenes de
velocidad y el ESP32 devuelve su telemetría. El contrato puede probarse sin
puerto serial mediante ``transport:=dry_run``.
"""

import json
import math


COMMAND_TYPE = 'cmd_vel'
STATE_TYPE = 'state'


def command_line(linear_mps, angular_radps, sequence):
    """Devuelve una orden de velocidad serializable y validada."""
    values = (linear_mps, angular_radps)
    if not all(math.isfinite(value) for value in values):
        raise ValueError('La velocidad debe ser finita')
    if sequence < 0:
        raise ValueError('La secuencia no puede ser negativa')
    return json.dumps({
        'type': COMMAND_TYPE,
        'linear_mps': round(float(linear_mps), 4),
        'angular_radps': round(float(angular_radps), 4),
        'sequence': int(sequence),
    }, separators=(',', ':')) + '\n'


def parse_state(line):
    """Valida una telemetría de ESP32 y devuelve solamente sus datos útiles."""
    message = json.loads(line)
    if not isinstance(message, dict) or message.get('type') != STATE_TYPE:
        raise ValueError('Mensaje de estado no reconocido')

    result = {'type': STATE_TYPE}
    for key in ('left_ticks', 'right_ticks'):
        if key in message:
            result[key] = int(message[key])
    for key in ('front_m', 'left_m', 'right_m'):
        value = message.get(key)
        if value is None:
            result[key] = None
        elif isinstance(value, (int, float)) and math.isfinite(value) and value >= 0.0:
            result[key] = float(value)
        else:
            raise ValueError(f'Lectura inválida: {key}')
    if 'imu' in message and isinstance(message['imu'], dict):
        result['imu'] = message['imu']
    return result
