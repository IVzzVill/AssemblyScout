import json

import pytest

from assemblyscout_hardware.protocol import command_line, parse_state


def test_command_line_is_one_json_line():
    line = command_line(0.12, -0.3, 7)
    assert line.endswith('\n')
    assert json.loads(line) == {
        'type': 'cmd_vel', 'linear_mps': 0.12,
        'angular_radps': -0.3, 'sequence': 7,
    }


def test_parse_state_keeps_valid_sensor_data():
    state = parse_state(
        '{"type":"state","left_ticks":12,"right_ticks":15,'
        '"front_m":0.4,"left_m":null,"right_m":1.2}'
    )
    assert state['left_ticks'] == 12
    assert state['front_m'] == 0.4
    assert state['left_m'] is None


def test_parse_state_rejects_invalid_distance():
    with pytest.raises(ValueError):
        parse_state('{"type":"state","front_m":-0.1}')
