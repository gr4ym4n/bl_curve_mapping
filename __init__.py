
import math
import typing
import dataclasses
import uuid
import bpy
import mathutils

#region Data Transfer Objects
###################################################################################################

@dataclasses.dataclass
class BLCMAP_CurvePointDTO:
    location: typing.Tuple[float, float] = (0.0, 0.0)
    handle_type: str = 'AUTO'
    select: bool = False

@dataclasses.dataclass
class BLCMAP_CurveDTO:
    points: typing.Sequence[BLCMAP_CurvePointDTO]
    extend: str = 'HORIZONTAL'

@dataclasses.dataclass
class BLCMAP_KeyframePointDTO:
    interpolation: str = 'BEZIER'
    easing: str = 'AUTO'
    co: typing.Tuple[float, float] = (0.0, 0.0)
    handle_left_type: str = 'FREE'
    handle_right_type: str = 'FREE'
    handle_left: typing.Tuple[float, float] = (0.0, 0.0)
    handle_right: typing.Tuple[float, float] = (0.0, 0.0)

#endregion Data Transfer Objects

#region Presets
###################################################################################################

linear = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((1.0, 1.0), 'VECTOR'),
    ])

sine_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.1, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO'),
    ])

sine_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.9, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO'),
    ])

sine_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.1, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO'),
    ])

quad_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.15, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)   , 'AUTO'),
    ])

quad_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.85, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)   , 'AUTO'),
    ])

quad_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.15, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.85, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)   , 'AUTO'),
    ])

cubic_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.2, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO'),
    ])

cubic_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.8, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO'),
    ])

cubic_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.2, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO'),
    ])

quart_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.25, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)  , 'AUTO'),
    ])

quart_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.75, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)  , 'AUTO'),
    ])

quart_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.25, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.75, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)  , 'AUTO'),
    ])

quint_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.275, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)    , 'AUTO'),
    ])

quint_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.725, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)    , 'AUTO'),
    ])

quint_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.275, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.725, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)    , 'AUTO'),
    ])

falloff_linear = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((1.0, 0.0), 'VECTOR'),
    ])

falloff_sine_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.1, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

falloff_sine_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

falloff_sine_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.1, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

falloff_quad_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.15, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO'),
    ])

falloff_quad_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.85, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO'),
    ])

falloff_quad_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.15, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.85, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO'),
    ])

falloff_cubic_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.2, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

falloff_cubic_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.8, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

falloff_cubic_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.2, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

falloff_quart_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.25, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO'),
    ])

falloff_quart_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.75, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO'),
    ])

falloff_quart_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.25, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.75, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO'),
    ])

falloff_quint_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.275, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO'),
    ])

falloff_quint_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.725, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO'),
    ])

falloff_quint_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.275, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.725, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO'),
    ])

bell_linear = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((0.5, 1.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((1.0, 0.0), 'VECTOR'),
    ])

bell_sine_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.05, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.95, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_sine_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.45, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.55, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_sine_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.05, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.45, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.55, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.95, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_quad_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.075, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.925, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO_CLAMPED'),
    ])

bell_quad_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.425, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.575, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO_CLAMPED'),
    ])

bell_quad_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.075, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.425, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.575, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.925, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO_CLAMPED'),
    ])

bell_cubic_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_cubic_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.4, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    ])

bell_cubic_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.4, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    ])

bell_quart_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.125, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.875, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO_CLAMPED'),
    ])

bell_quart_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.375, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.625, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO_CLAMPED'),
    ])

bell_quart_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.125, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.375, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.625, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.875, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO_CLAMPED'),
    ])

bell_quint_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1375, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8625, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)     , 'AUTO_CLAMPED'),
    ])

bell_quint_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.3625, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6375, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)     , 'AUTO_CLAMPED'),
    ])

bell_quint_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1375, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.3625, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6375, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8625, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)     , 'AUTO_CLAMPED'),
    ])

bell_linear_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((0.5, 1.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((1.0, 1.0), 'VECTOR'),
    ])

bell_sine_in_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.05, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)  , 'AUTO_CLAMPED'),
    ])

bell_sine_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.45, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)  , 'AUTO_CLAMPED'),
    ])

bell_sine_in_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.05, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.45, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)  , 'AUTO_CLAMPED'),
    ])

bell_quad_in_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.075, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)    , 'AUTO_CLAMPED'),
    ])

bell_quad_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.425, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)    , 'AUTO_CLAMPED'),
    ])

bell_quad_in_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.075, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.425, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)    , 'AUTO_CLAMPED'),
    ])

bell_cubic_in_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO_CLAMPED'),
    ])

bell_cubic_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.4, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO_CLAMPED'),
    ])

bell_cubic_in_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.4, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0) , 'AUTO_CLAMPED'),
    ])

bell_quart_in_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.125, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)   , 'AUTO_CLAMPED'),
    ])

bell_quart_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.375, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)   , 'AUTO_CLAMPED'),
    ])

bell_quart_in_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.125, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.375, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)   , 'AUTO_CLAMPED'),
    ])

bell_quint_in_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1375, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)     , 'AUTO_CLAMPED'),
    ])

bell_quint_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.3625, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)     , 'AUTO_CLAMPED'),
    ])

bell_quint_in_out_head = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 0.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.1375, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.3625, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 1.0)     , 'AUTO_CLAMPED'),
    ])

bell_linear_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((0.5, 1.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((1.0, 0.0), 'VECTOR'),
    ])

bell_sine_in_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.95, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_sine_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.55, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_sine_in_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)  , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.55, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.95, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO_CLAMPED'),
    ])

bell_quad_in_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.925, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO_CLAMPED'),
    ])

bell_quad_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.575, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO_CLAMPED'),
    ])

bell_quad_in_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)    , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.575, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.925, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO_CLAMPED'),
    ])

bell_cubic_in_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO_CLAMPED'),
    ])

bell_cubic_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO_CLAMPED'),
    ])

bell_cubic_in_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0) , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO_CLAMPED'),
    ])

bell_quart_in_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.875, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO_CLAMPED'),
    ])

bell_quart_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.625, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO_CLAMPED'),
    ])

bell_quart_in_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)   , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.625, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.875, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO_CLAMPED'),
    ])

bell_quint_in_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8625, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)     , 'AUTO_CLAMPED'),
    ])

bell_quint_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6375, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)     , 'AUTO_CLAMPED'),
    ])

bell_quint_in_out_tail = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.5, 1.0)     , 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.6375, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8625, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)     , 'AUTO_CLAMPED'),
    ])

PRESET_LUT = {
    'SIGMOID': {
        'LINEAR': {
            'EASE_IN'    : linear,
            'EASE_OUT'   : linear,
            'EASE_IN_OUT': linear,
            },
        'SINE': {
            'EASE_IN'    : sine_in,
            'EASE_OUT'   : sine_out,
            'EASE_IN_OUT': sine_in_out,
            },
        'QUAD': {
            'EASE_IN'    : quad_in,
            'EASE_OUT'   : quad_out,
            'EASE_IN_OUT': quad_in_out,
            },
        'CUBIC': {
            'EASE_IN'    : cubic_in,
            'EASE_OUT'   : cubic_out,
            'EASE_IN_OUT': cubic_in_out,
            },
        'QUART': {
            'EASE_IN'    : quart_in,
            'EASE_OUT'   : quart_out,
            'EASE_IN_OUT': quart_in_out,
            },
        'QUINT': {
            'EASE_IN'    : quint_in,
            'EASE_OUT'   : quint_out,
            'EASE_IN_OUT': quint_in_out,
            },
    },
    'FALLOFF': {
        'LINEAR': {
            'EASE_IN'    : falloff_linear,
            'EASE_OUT'   : falloff_linear,
            'EASE_IN_OUT': falloff_linear,
            },
        'SINE': {
            'EASE_IN'    : falloff_sine_in,
            'EASE_OUT'   : falloff_sine_out,
            'EASE_IN_OUT': falloff_sine_in_out,
            },
        'QUAD': {
            'EASE_IN'    : falloff_quad_in,
            'EASE_OUT'   : falloff_quad_out,
            'EASE_IN_OUT': falloff_quad_in_out,
            },
        'CUBIC': {
            'EASE_IN'    : falloff_cubic_in,
            'EASE_OUT'   : falloff_cubic_out,
            'EASE_IN_OUT': falloff_cubic_in_out,
            },
        'QUART': {
            'EASE_IN'    : falloff_quart_in,
            'EASE_OUT'   : falloff_quart_out,
            'EASE_IN_OUT': falloff_quart_in_out,
            },
        'QUINT': {
            'EASE_IN'    : falloff_quint_in,
            'EASE_OUT'   : falloff_quint_out,
            'EASE_IN_OUT': falloff_quint_in_out,
            },
    },
    'BELL': {
        'HEAD': {
            'LINEAR': {
                'EASE_IN'    : bell_linear_head,
                'EASE_OUT'   : bell_linear_head,
                'EASE_IN_OUT': bell_linear_head,
                },
            'SINE': {
                'EASE_IN'    : bell_sine_in_head,
                'EASE_OUT'   : bell_sine_out_head,
                'EASE_IN_OUT': bell_sine_in_out_head,
                },
            'QUAD': {
                'EASE_IN'    : bell_quad_in_head,
                'EASE_OUT'   : bell_quad_out_head,
                'EASE_IN_OUT': bell_quad_in_out_head,
                },
            'CUBIC': {
                'EASE_IN'    : bell_cubic_in_head,
                'EASE_OUT'   : bell_cubic_out_head,
                'EASE_IN_OUT': bell_cubic_in_out_head,
                },
            'QUART': {
                'EASE_IN'    : bell_quart_in_head,
                'EASE_OUT'   : bell_quart_out_head,
                'EASE_IN_OUT': bell_quart_in_out_head,
                },
            'QUINT': {
                'EASE_IN'    : bell_quint_in_head,
                'EASE_OUT'   : bell_quint_out_head,
                'EASE_IN_OUT': bell_quint_in_out_head,
                },
        },
        'TAIL': {
            'LINEAR': {
                'EASE_IN'    : bell_linear_tail,
                'EASE_OUT'   : bell_linear_tail,
                'EASE_IN_OUT': bell_linear_tail,
                },
            'SINE': {
                'EASE_IN'    : bell_sine_in_tail,
                'EASE_OUT'   : bell_sine_out_tail,
                'EASE_IN_OUT': bell_sine_in_out_tail,
                },
            'QUAD': {
                'EASE_IN'    : bell_quad_in_tail,
                'EASE_OUT'   : bell_quad_out_tail,
                'EASE_IN_OUT': bell_quad_in_out_tail,
                },
            'CUBIC': {
                'EASE_IN'    : bell_cubic_in_tail,
                'EASE_OUT'   : bell_cubic_out_tail,
                'EASE_IN_OUT': bell_cubic_in_out_tail,
                },
            'QUART': {
                'EASE_IN'    : bell_quart_in_tail,
                'EASE_OUT'   : bell_quart_out_tail,
                'EASE_IN_OUT': bell_quart_in_out_tail,
                },
            'QUINT': {
                'EASE_IN'    : bell_quint_in_tail,
                'EASE_OUT'   : bell_quint_out_tail,
                'EASE_IN_OUT': bell_quint_in_out_tail,
                },
        },
        'BOTH': {
            'LINEAR': {
                'EASE_IN'    : bell_linear,
                'EASE_OUT'   : bell_linear,
                'EASE_IN_OUT': bell_linear,
                },
            'SINE': {
                'EASE_IN'    : bell_sine_in,
                'EASE_OUT'   : bell_sine_out,
                'EASE_IN_OUT': bell_sine_in_out,
                },
            'QUAD': {
                'EASE_IN'    : bell_quad_in,
                'EASE_OUT'   : bell_quad_out,
                'EASE_IN_OUT': bell_quad_in_out,
                },
            'CUBIC': {
                'EASE_IN'    : bell_cubic_in,
                'EASE_OUT'   : bell_cubic_out,
                'EASE_IN_OUT': bell_cubic_in_out,
                },
            'QUART': {
                'EASE_IN'    : bell_quart_in,
                'EASE_OUT'   : bell_quart_out,
                'EASE_IN_OUT': bell_quart_in_out,
                },
            'QUINT': {
                'EASE_IN'    : bell_quint_in,
                'EASE_OUT'   : bell_quint_out,
                'EASE_IN_OUT': bell_quint_in_out,
                },
        },
    },
    }

#endregion Presets

#region Curve Node Management
###################################################################################################

NODE_TREE_NAME = "Curve Mapping Nodes (API Defined)"
CLIP_MIN_X = 0.0
CLIP_MAX_X = 1.0
CLIP_MIN_Y = 0.0
CLIP_MAX_Y = 1.0
USE_CLIP = True

def nodetree_get(create: typing.Optional[bool]=True) -> bpy.types.ShaderNodeTree:
    tree = bpy.data.node_groups.get(NODE_TREE_NAME)
    if tree is None and create:
        tree = bpy.data.node_groups.new(NODE_TREE_NAME, "ShaderNodeTree")
    return tree

def nodetree_node_exists(name: str) -> bool:
    tree = nodetree_get(create=False)
    return tree is not None and tree.nodes.get(name) is not None


def nodetree_node_update(name: str, data: typing.Union[BLCMAP_CurveDTO, 'BLCMAP_Curve']) -> bpy.types.ShaderNodeVectorCurve:

    tree = nodetree_get(create=True)
    node = tree.nodes.get(name)
    if node is None:
        return nodetree_node_ensure(name, data)

    point_count = max(len(data.points), 2)
    mapping = node.mapping
    mapping.extend = data.extend

    points = mapping.curves[0].points
    while len(points) > point_count: points.remove(points[-2])
    while len(points) < point_count: points.new(0.0, 0.0)

    for point, props in zip(points, data.points):
        point.handle_type = props.handle_type
        point.location = props.location
        point.select = props.select

    mapping.update()
    return node

def nodetree_node_ensure(name: str, data: typing.Optional[typing.Union[BLCMAP_CurveDTO, 'BLCMAP_Curve']]=None) -> typing.Optional[bpy.types.ShaderNodeVectorCurve]:
    tree = nodetree_get(True)
    node = tree.nodes.get(name)

    if node is None and data:
        node = tree.nodes.new("ShaderNodeVectorCurve")
        node.name = name

        mapping = node.mapping
        mapping.clip_min_x = CLIP_MIN_X
        mapping.clip_max_x = CLIP_MAX_X
        mapping.clip_min_y = CLIP_MIN_Y
        mapping.clip_max_y = CLIP_MAX_Y
        mapping.use_clip = USE_CLIP

        node = nodetree_node_update(node.name, data)

    return node

def nodetree_node_remove(name: str) -> None:
    tree = nodetree_get(create=False)
    if tree:
        node = tree.nodes.get(name)
        if node:
            tree.nodes.remove(node)

#endregion Curve Node Management

#region Utilities
###################################################################################################

def _calc_bezier_handles(p2, ht, h1, h2, prev=None, next=None) -> None:
    pt = mathutils.Vector((0.0, 0.0))

    if prev is None:
        p3 = next
        pt[0] = 2.0 * p2[0] - p3[0]
        pt[1] = 2.0 * p2[1] - p3[1]
        p1 = pt
    else:
        p1 = prev

    if next is None:
        p1 = prev
        pt[0] = 2.0 * p2[0] - p1[0]
        pt[1] = 2.0 * p2[1] - p1[1]
        p3 = pt
    else:
        p3 = next

    dvec_a = p2 - p1
    dvec_b = p3 - p2
    len_a = dvec_a.length
    len_b = dvec_b.length

    if len_a == 0.0:
        len_a = 1.0
    if len_b == 0.0:
        len_b = 1.0

    if ht in ('AUTO', 'AUTO_CLAMPED'):
        tvec = mathutils.Vector((
            dvec_b[0] / len_b + dvec_a[0] / len_a,
            dvec_b[1] / len_b + dvec_a[1] / len_a))

        length = tvec.length * 2.5614
        if length != 0.0:
            ln = -(len_a / length)
            h1[0] = p2[0] + tvec[0] * ln
            h1[1] = p2[1] + tvec[1] * ln
            if ht == 'AUTO_CLAMPED' and prev is not None and next is not None:
                ydiff1 = prev[1] - p2[1]
                ydiff2 = next[1] - p2[1]
                if (ydiff1 <= 0.0 and ydiff2 <= 0.0) or (ydiff1 >= 0.0 and ydiff2 >= 0.0):
                    h1[1] = p2[1]
                else:
                    if ydiff1 <= 0.0:
                        if prev[1] > h1[1]:
                            h1[1] = prev[1]
                    else:
                        if prev[1] < h1[1]:
                            h1[1] = prev[1]

            ln = len_b / length
            h2[0] = p2[0] + tvec[0] * ln
            h2[1] = p2[1] + tvec[1] * ln
            if ht == 'AUTO_CLAMPED' and prev is not None and next is not None:
                ydiff1 = prev[1] - p2[1]
                ydiff2 = next[1] - p2[1]
                if (ydiff1 <= 0.0 and ydiff2 <= 0.0) or (ydiff1 >= 0.0 and ydiff2 >= 0.0):
                    h2[1] = p2[1]
                else:
                    if ydiff1 <= 0.0:
                        if next[1] < h2[1]:
                            h2[1] = next[1]
                    else:
                        if next[1] > h2[1]:
                            h2[1] = next[1]

    else: # ht == VECTOR
        h1[0] = p2[0] + dvec_a[0] * (-1.0/3.0)
        h1[1] = p2[1] + dvec_a[1] * (-1.0/3.0)
        h2[0] = p2[0] + dvec_b[0] * (1.0/3.0)
        h2[1] = p2[1] + dvec_b[1] * (1.0/3.0)

def to_bezier(points: typing.Iterable[typing.Union['BLCMAP_CurvePoint', bpy.types.CurveMapPoint]],
              x_range: typing.Optional[typing.Tuple[float, float]]=None,
              y_range: typing.Optional[typing.Tuple[float, float]]=None,
              extrapolate: typing.Optional[bool]=True) -> typing.List[BLCMAP_KeyframePointDTO]:

    data = [(
        p.location.copy(),
        p.handle_type,
        mathutils.Vector((0.0, 0.0)),
        mathutils.Vector((0.0, 0.0))
        ) for p in points]

    if x_range:
        a, b = x_range
        if a > b:
            a, b = b, a
            for item in data:
                item[0][0] = 1.0 - item[0][0]
            data.reverse()
        d = b - a
        for item in data:
            item[0][0] = a + item[0][0] * d

    if y_range:
        a, b = y_range
        d = b - a
        for item in data:
            item[0][1] = a + item[0][1] * d

    n = len(data) - 1
    for i, (pt, ht, h1, h2) in enumerate(data):
        _calc_bezier_handles(pt, ht, h1, h2,
                             data[i-1][0] if i > 0 else None,
                             data[i+1][0] if i < n else None)

    if len(data) > 2:
        ptA, htA, h1A, h2A = data[0]
        ptN, htN, h1N, h2N = data[-1]

        if htA == 'AUTO':
            hlen = (h2A - ptA).length
            hvec = data[1][2].copy()
            if hvec[0] < ptA[0]:
                hvec[0] = ptA[0]

            hvec -= ptA
            nlen = hvec.length
            if nlen > 0.00001:
                hvec *= hlen / nlen
                h2A[0] = hvec[0] + ptA[0]
                h2A[1] = hvec[1] + ptA[1]
                h1A[0] = ptA[0] - hvec[0]
                h1A[1] = ptA[1] - hvec[1]

        if htN == 'AUTO':
            hlen = (h1N - ptN).length
            hvec = data[-2][3].copy()
            if hvec[0] > ptN[0]:
                hvec[0] = ptN[0]

            hvec -= ptN
            nlen = hvec.length
            if nlen > 0.00001:
                hvec *= hlen / nlen
                h1N[0] = hvec[0] + ptN[0]
                h1N[1] = hvec[1] + ptN[1]
                h2N[0] = ptN[0] - hvec[0]
                h2N[1] = ptN[1] - hvec[1]

    if not extrapolate:
        pt = data[0]
        co = pt[0]
        hl = pt[2]
        hl[0] = 0.0
        hl[1] = co[1]

        pt = data[-1]
        co = pt[0]
        hr = pt[3]
        hr[0] = 1.0
        hr[1] = co[1]

    return [BLCMAP_KeyframePointDTO(co=item[0],
                                    handle_left=item[2],
                                    handle_right=item[3]) for item in data]

def keyframe_points_assign(points: bpy.types.FCurveKeyframePoints,
                           frames: typing.Sequence[BLCMAP_KeyframePointDTO]) -> None:

    length = len(points)
    target = len(frames)

    while length > target:
        points.remove(points[-1])
        length -= 1

    for index, frame in enumerate(frames):

        if index < length:
            point = points[index]
        else:
            point = points.insert(frame.co[0], frame.co[1])
            length += 1

        point.interpolation = frame.interpolation
        point.easing = frame.easing
        point.co = frame.co
        point.handle_left_type = frame.handle_left_type
        point.handle_right_type = frame.handle_right_type
        point.handle_left = frame.handle_left
        point.handle_right = frame.handle_right

def points_offset(points: typing.Iterable['BLCMAP_CurvePoint'],
                  offset: float,
                  origin: typing.Optional[float]=0.0) -> None:
    a = (min(max(origin, -0.999), 0.999) - -1.0) * 0.5
    b = (min(max(offset, -0.999), 0.999) - -1.0) * 0.5
    if a != b:
        for p in points:
            x, y = p.location
            if x < b:
                x = (x * b) / a
            else:
                x = ((x-a) * (1.0-b)) / (1.0-a) + b
            p["location"] = (x, y)

def check_match(curve: 'BLCMAP_Curve', mapping: bpy.types.CurveMapping) -> bool:
    if curve.extend != mapping.extend:
        return True
    else:
        cpts = curve.points
        mpts = mapping.curves[0].points
        if len(cpts) != len(mpts):
            return True
        else:
            for cpt, mpt in zip(cpts, mpts):
                aco = cpt.location
                bco = mpt.location
                if aco[0] != bco[0] or aco[1] != bco[1]:
                    return True
        return False

#endregion Utilities

#region Property Groups
###################################################################################################

class BLCMAP_CurvePointProperties(bpy.types.PropertyGroup):

    handle_type: bpy.props.EnumProperty(
        name="Handle Type",
        description="Curve interpolation at this point: Bezier or vector",
        items=[
            ('AUTO'        , "Auto Handle"        , "", 'NONE', 0),
            ('AUTO_CLAMPED', "Auto Clamped Handle", "", 'NONE', 1),
            ('VECTOR'      , "Vector Handle"      , "", 'NONE', 2),
            ],
        get=lambda self: self.get("handle_type", 0),
        options=set(),
        )

    location: bpy.props.FloatVectorProperty(
        name="Location",
        description="X/Y coordinates of the curve point",
        size=2,
        subtype='XYZ',
        get=lambda self: self.get("location", (0.0, 0.0)),
        options=set(),
        )

    select: bpy.props.BoolProperty(
        name="Select",
        description="Selection state of the curve point",
        get=lambda self: self.get("select", False),
        options=set(),
        )

    def __init__(self, data: typing.Union[BLCMAP_CurvePointDTO,
                                          'BLCMAP_CurvePoint',
                                          'BLCMAP_CurvePointProperties',
                                           bpy.types.CurveMapPoint]) -> None:
        self["handle_type"] = ('AUTO', 'AUTO_CLAMPED', 'VECTOR').index(data.handle_type)
        self["location"] = data.location
        self["select"] = data.select

class BLCMAP_CurveProperties(bpy.types.PropertyGroup):
    """Curve in a curve mapping"""

    extend: bpy.props.EnumProperty(
        name="Extend",
        description="Extrapolate the curve or extend it horizontally",
        items=[
            ('HORIZONTAL'  , "Horizontal"  , "", 'NONE', 0),
            ('EXTRAPOLATED', "Extrapolated", "", 'NONE', 1),
            ],
        get=lambda self: self.get("extend", 0),
        options=set(),
        )

    points: bpy.props.CollectionProperty(
        name="Points",
        description="",
        type=BLCMAP_CurvePointProperties,
        options=set()
        )

    def __init__(self, data: typing.Union[BLCMAP_CurveDTO, 'BLCMAP_Curve', 'BLCMAP_CurveProperties']) -> None:
        self["extend"] = ('HORIZONTAL', 'EXTRAPOLATED').index(data.extend)
        points = self.points
        points.clear()
        for item in data:
            points.add().__init__(item)

class BLCMAP_CurvePoint(bpy.types.PropertyGroup):
    """Point of a curve used for a curve mapping"""

    def update(self, context: typing.Optional[bpy.types.Context]=None) -> None:
        try:
            curve = self.id_data.path_resolve(self.path_from_id().rpartition(".points.")[0])
        except ValueError:
            pass
        else:
            if hasattr(curve, "update"):
                curve.update(context)

    handle_type: bpy.props.EnumProperty(
        name="Handle Type",
        description="Curve interpolation at this point: Bezier or vector",
        items=[
            ('AUTO'        , "Auto Handle"        , "", 'NONE', 0),
            ('AUTO_CLAMPED', "Auto Clamped Handle", "", 'NONE', 1),
            ('VECTOR'      , "Vector Handle"      , "", 'NONE', 2),
            ],
        default='AUTO',
        options=set(),
        update=update
        )

    location: bpy.props.FloatVectorProperty(
        name="Location",
        description="X/Y coordinates of the curve point",
        size=2,
        subtype='XYZ',
        default=(0.0, 0.0),
        options=set(),
        update=update
        )

    select: bpy.props.BoolProperty(
        name="Select",
        description="Selection state of the curve point",
        default=False,
        options=set(),
        update=update
        )

    def __init__(self, data: typing.Union[BLCMAP_CurvePointDTO, BLCMAP_CurvePointProperties, 'BLCMAP_CurvePoint', bpy.types.CurveMapPoint]) -> None:
        self["handle_type"] = ('AUTO', 'AUTO_CLAMPED', 'VECTOR').index(data.handle_type)
        self["location"] = data.location
        self["select"] = data.select

    def __eq__(self, other: typing.Any) -> bool:
        for key in ("handle_type", "location", "select"):
            if not getattr(other, key, None) == getattr(self, key):
                return False

class BLCMAP_CurvePoints(bpy.types.PropertyGroup):
    """Collection of curve map points"""

    points__internal__: bpy.props.CollectionProperty(
        type=BLCMAP_CurvePoint,
        options={'HIDDEN'}
        )

    def update(self, context: typing.Optional[bpy.types.Context]=None) -> None:
        try:
            curve = self.id_data.path_resolve(self.path_from_id().rpartition(".")[0])
        except ValueError:
            pass
        else:
            if hasattr(curve, "update"):
                curve.update()

    def __init__(self, data: typing.Sequence[typing.Union[BLCMAP_CurvePointDTO, BLCMAP_CurvePoint, bpy.types.CurveMapPoint]]) -> None:
        points = self.points__internal__
        points.clear()
        for item in data:
            points.add().__init__(item)

    def __iter__(self) -> typing.Iterator[BLCMAP_CurvePoint]:
        return iter(self.points__internal__)

    def __len__(self) -> int:
        return len(self.points__internal__)

    def __getitem__(self, key: typing.Union[int, slice]) -> typing.Union[BLCMAP_CurvePoint, typing.List[BLCMAP_CurvePoint]]:
        if isinstance(key, str):
            raise TypeError((f'{self.__class__.__name__}[key] '
                             f'str key not supported'))

        if isinstance(key, int):
            if 0 > key >= len(self):
                raise IndexError((f'{self.__class__.__name__}[key]: '
                                  f'index {key} out of range 0-{len(self)}'))

            return self.points__internal__[key]

        if isinstance(key, slice):
            return self.points__internal__[key]

        raise TypeError((f'{self.__class__.__name__}[key] '
                         f'expected key to be int or slice, not {key.__class__.__name__}'))

    def new(self, position: float, value: float) -> BLCMAP_CurvePoint:
        """Add a point"""

        if not isinstance(position, float):
            raise TypeError((f'{self.__class__.__name__}.new(position, value): '
                             f'Expected position to be a float, '
                             f'not {position.__class__.__name__}'))

        if not isinstance(value, float):
            raise TypeError((f'{self.__class__.__name__}.new(position, value): '
                             f'Expected value to be a float, '
                             f'not {value.__class__.__name__}'))

        point = self.points__internal__.add()
        point.location = (position, value)

        self.update()
        return point

    def remove(self, point: BLCMAP_CurvePoint) -> None:
        """Remove a point"""

        if not isinstance(point, BLCMAP_CurvePoint):
            raise TypeError((f'{self.__class__.__name__}'
                             f'.remove(point): expected point to be '
                             f'{BLCMAP_CurvePoint.__name__}, not {point.__class__.__name__}'))

        index = next((i for i, p in enumerate(self) if p == point), -1)

        if index == -1:
            raise ValueError((f'{self.__class__.__name__}'
                              f'.remove(point): point not found'))

        if index == 0:
            raise ValueError(f'{self.__class__.__name__}'
                             f'.remove(point): Cannot remove first point')

        if index == len(self) - 1:
            raise ValueError(f'{self.__class__.__name__}'
                             f'.remove(point): Cannot remove last point')

        self.points__internal__.remove(index)
        self.update()

class BLCMAP_Curve(bpy.types.PropertyGroup):
    """Curve in a curve mapping"""

    NODE_NAME_PREFIX = "node"

    def __init__(self,
                 data: typing.Union[BLCMAP_CurveDTO, 'BLCMAP_Curve', 'BLCMAP_CurveProperties', bpy.types.CurveMap],
                 extend: typing.Optional[str]=None) -> None:
        if extend is None:
            extend = 'HORIZONTAL' if isinstance(data, bpy.types.CurveMap) else data.extend
        self["extend"] = ('HORIZONTAL', 'EXTRAPOLATED').index(extend)
        self.points.__init__(data.points)

    def get_node_identifier(self) -> str:
        identifier = self.get("identifier", "")
        if not identifier:
            identifier = f'{self.NODE_NAME_PREFIX}_{uuid.uuid4().hex}'
            self["identifier"] = identifier
        return identifier

    def update(self, _: typing.Optional[bpy.types.Curve]=None) -> None:
        """Ensure points are ordered chronologically"""

        points = list(self.points)
        sorted_points = sorted(points, key=lambda point: point.location[0])

        if points != sorted_points:
            data = [
                (tuple(point.location),
                point.handle_type,
                point.select
                ) for point in sorted_points]

            for point, (location, handle_type, select) in zip(points, data):
                point.location = location
                point.handle_type = handle_type
                point.select = select

        try:
            manager = self.id_data.path_resolve(self.path_from_id().rpartition(".")[0])
        except ValueError:
            nodetree_node_update(self.node_identifier, self)
        else:
            if isinstance(manager, BCLMAP_CurveManager):
                manager.update()
            else:
                nodetree_node_update(self.node_identifier, self)


    extend: bpy.props.EnumProperty(
        name="Extend",
        description="Extrapolate the curve or extend it horizontally",
        items=[
            ('HORIZONTAL'  , "Horizontal"  , "", 'NONE', 0),
            ('EXTRAPOLATED', "Extrapolated", "", 'NONE', 1),
            ],
        default='HORIZONTAL',
        options=set(),
        update=update
        )

    node_identifier: bpy.props.StringProperty(
        name="Identifier",
        description="Unique curve node identifier",
        get=get_node_identifier,
        options=set()
        )

    points: bpy.props.PointerProperty(
        name="Points",
        description="",
        type=BLCMAP_CurvePoints,
        options=set()
        )

class BCLMAP_CurveManager:

    def get_offset(self) -> float:
        return self.get("offset", 0.0)

    def set_offset(self, value: float) -> None:
        cache = self.get_offset()
        self["offset"] = value
        points_offset(self.curve.points, value, cache)
        self.update()

    curve: bpy.props.PointerProperty(
        name="Curve",
        type=BLCMAP_Curve,
        options=set()
        )

    curve_type: bpy.props.EnumProperty(
        name="Type",
        items=[
            ('SIGMOID', "Sigmoid", "", 'NONE', 0),
            ('FALLOFF', "Falloff", "", 'NONE', 1),
            ('BELL'   , "Bell"   , "", 'NONE', 2),
            ],
        default='SIGMOID',
        options=set(),
        update=lambda self, _: self.update()
        )

    easing: bpy.props.EnumProperty(
        name="Easing",
        items=[
            ('EASE_IN'    , "In"      , "Ease in"        , 'IPO_EASE_IN'    , 0),
            ('EASE_OUT'   , "Out"     , "Ease out"       , 'IPO_EASE_OUT'   , 1),
            ('EASE_IN_OUT', "In & Out", "Ease in and out", 'IPO_EASE_IN_OUT', 2),
            ],
        default='EASE_IN_OUT',
        options=set(),
        update=lambda self, _: self.update(),
        )

    interpolation: bpy.props.EnumProperty(
        name="Interpolation",
        items=[
            ('LINEAR', "Linear"    , "Linear"           , 'IPO_LINEAR', 0),
            ('SINE'  , "Sinusoidal", "Sinusoidal"       , 'IPO_SINE'  , 1),
            ('QUAD'  , "Quadratic" , "Quadratic"        , 'IPO_QUAD'  , 2),
            ('CUBIC' , "Cubic"     , "Cubic"            , 'IPO_CUBIC' , 3),
            ('QUART' , "Quartic"   , "Quartic"          , 'IPO_QUART' , 4),
            ('QUINT' , "Quntic"    , "Quintic"          , 'IPO_QUINT' , 5),
            None,
            ('CURVE' , "Curve"     , "Use custom curve" , 'FCURVE'    , 6),
            ],
        default='LINEAR',
        options=set(),
        update=lambda self, _: self.update(),
        )

    offset: bpy.props.FloatProperty(
        name="Offset",
        min=-1.0,
        max=1.0,
        get=get_offset,
        set=set_offset,
        options=set()
        )

    ramp: bpy.props.EnumProperty(
        name="Ramp",
        items=[
            ('HEAD', "Head", "", 'NONE', 0),
            ('TAIL', "Tail", "", 'NONE', 1),
            ('BOTH', "Both", "", 'NONE', 2),
            ],
        default='BOTH',
        options=set(),
        update=lambda self, _: self.update()
        )

    def __init__(self, **options: typing.Dict[str, typing.Any]) -> None:
        curve = options.pop("curve", None)
        if curve:
            options["interpolation"] = 6
            self.curve.__init__(curve)
        for key, value in options.items():
            if key in ("type", "curve_type"):
                self["curve_type"] = ('SIGMOID', 'FALLOFF', 'BELL').index(value)
            elif key == "interpolation":
                self["interpolation"] = ('LINEAR', 'SINE', 'QUAD', 'CUBIC', 'QUART', 'QUINT', 'CURVE').index(value)
            elif key == "easing":
                self["easing"] = ('EASE_IN', 'EASE_OUT', 'EASE_IN_OUT').index(value)
            elif key == "ramp":
                self["ramp"] = ('HEAD', 'TAIL', 'BOTH').index(value)
            else:
                self[key] = value
        BCLMAP_CurveManager.update(self)

    def update(self) -> None:
        ipo = self.interpolation
        curve: BLCMAP_Curve = self.curve
        if ipo != 'CURVE':
            type = self.curve_type
            if type == 'BELL':
                preset = PRESET_LUT[type][self.ramp][ipo][self.easing]
            else:
                preset = PRESET_LUT[type][ipo][self.easing]
            curve.__init__(preset)
            offset = self.get_offset()
            if offset != 0.0:
                points_offset(curve.points, offset)
        nodetree_node_update(curve.node_identifier, curve)

#endregion Property Groups

#region Operators
###################################################################################################

class BLCMAP_OT_curve_copy(bpy.types.Operator):

    bl_idname = "blcmap.curve_copy"
    bl_label = "Copy Curve"
    bl_description = "Copy the curve to the buffer"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return isinstance(getattr(context, "curve", None), BLCMAP_Curve)

    def execute(self, context: bpy.types.Context) -> typing.Set[str]:
        curve = getattr(context, "curve", None)
        if not hasattr(bpy.types.Scene, "blcmap_curve_buffer"):
            bpy.types.Scene.blcmap_curve_buffer = bpy.props.PointerProperty(type=BLCMAP_CurveProperties)
        context.scene.blcmap_curve_buffer.__init__(curve)
        return {'FINISHED'}

class BLCMAP_OT_curve_paste(bpy.types.Operator):

    bl_idname = "blcmap.curve_paste"
    bl_label = "Paste Curve"
    bl_description = "Paste the curve from the buffer"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return (isinstance(getattr(context, "curve", None), BLCMAP_Curve)
                and hasattr(context.scene, "blcmap_curve_buffer")
                and context.scene.is_property_set("blcmap_curve_buffer"))

    def execute(self, context: bpy.types.Context) -> typing.Set[str]:
        curve: BLCMAP_Curve = getattr(context, "curve")
        curve.__init__(context.scene.blcmap_curve_buffer)
        curve.update()
        return {'FINISHED'}

class BLCMAP_OT_node_ensure(bpy.types.Operator):

    bl_idname = "blcmap.node_ensure"
    bl_label = "Ensure Curve"
    bl_description = "Ensure the curve exists"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return isinstance(getattr(context, "curve", None), BLCMAP_Curve)

    def execute(self, context: bpy.types.Context) -> typing.Set[str]:

        curve: typing.Optional[BLCMAP_Curve] = getattr(context, "curve", None)
        if not isinstance(curve, BLCMAP_Curve):
            self.report({'ERROR'}, f'{self.__class__.__name__} Invalid context.curve {curve.__class__.__name__}')
            return {'CANCELLED'}

        nodetree_node_ensure(curve.node_identifier, curve)

        return {'FINISHED'}

class BLCMAP_OT_handle_type_set(bpy.types.Operator):

    bl_idname = "blcmap.handle_type_set"
    bl_label = "Handle Type"
    bl_description = "Set the handle type of selected curve point(s)"
    bl_options = {'INTERNAL'}

    handle_type: bpy.props.EnumProperty(
        name="Handle Type",
        description="Curve interpolation at this point: Bezier or vector",
        items=[
            ('AUTO'        , "Auto Handle"        , "", 'HANDLE_AUTO', 0),
            ('AUTO_CLAMPED', "Auto Clamped Handle", "", 'HANDLE_AUTOCLAMPED', 1),
            ('VECTOR'      , "Vector Handle"      , "", 'HANDLE_VECTOR', 2),
            ],
        default='AUTO',
        options=set(),
        )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return isinstance(getattr(context, "curve", None), BLCMAP_Curve)

    def execute(self, context: bpy.types.Context) -> typing.Set[str]:
        tree = nodetree_get()
        if tree:
            data: BLCMAP_Curve = getattr(context, "curve")
            node = tree.nodes.get(data.node_identifier)
            if node:
                value = self.handle_type
                for point in node.mapping.curves[0].points:
                    if point.select:
                        point.handle_type = value
                node.mapping.update()
        return {'FINISHED'}

#endregion Operators

#region UI Utilities
###################################################################################################

ACTIVE_CURVES: typing.List[BLCMAP_Curve] = []

def check_active_curves():
    curve: BLCMAP_Curve
    for curve in ACTIVE_CURVES:
        tree = nodetree_get()
        if tree is not None:
            node = tree.nodes.get(curve.node_identifier)
            if node is not None and check_match(curve, node.mapping):
                curve.__init__(node.mapping.curves[0])
                curve.update()
    ACTIVE_CURVES.clear()

def draw_curve_manager_ui(layout: bpy.types.UILayout, manager: BCLMAP_CurveManager) -> None:

    row = layout.row()
    row.context_pointer_set("curve", manager.curve)
    row.operator_context = 'INVOKE_DEFAULT'
    
    box = row.column().box()
    ops = row.column(align=True)

    curve: BLCMAP_Curve = manager.curve

    if curve.is_property_set("node_identifier") and nodetree_node_exists(curve.node_identifier):
        row = box.row()
        row.ui_units_y = 0.01

        intrp = manager.interpolation
        split = row.split(factor=0.6)

        if intrp == 'CURVE':
            if not bpy.app.timers.is_registered(check_active_curves):
                ACTIVE_CURVES.append(curve)
                bpy.app.timers.register(check_active_curves, first_interval=1.0)

            split.prop(manager, "interpolation", text="")

            node = nodetree_get().nodes[curve.node_identifier]
            seld = {pt.handle_type for pt in node.mapping.curves[0].points if pt.select}

            row = split.row(align=True)
            row.alignment = 'RIGHT'
            row.enabled = len(seld) > 0

            for htype, icon in (('AUTO', 'HANDLE_AUTO'),
                                ('AUTO_CLAMPED', 'HANDLE_AUTOCLAMPED'),
                                ('VECTOR', 'HANDLE_VECTOR')):
                row.operator(BLCMAP_OT_handle_type_set.bl_idname,
                             text="",
                             icon=icon,
                             depress=(len(seld) == 1 and htype in seld)).handle_type = htype
        
        else:
            ctype = manager.curve_type

            if ctype == 'BELL':
                row = split.row()
                row.prop(manager, 'ramp', text="", icon='NORMALIZE_FCURVES', icon_only=True)
                row.prop(manager, "interpolation", text="")
            else:
                split.prop(manager, "interpolation", text="")

            if intrp != 'LINEAR':
                split.prop(manager, "easing", text="")

        curve = manager.curve

        col = box.column()
        col.scale_x = 0.01
        col.enabled = manager.interpolation == 'CURVE'
        col.template_curve_mapping(nodetree_node_ensure(curve.get_node_identifier(), curve), "mapping")
        col.separator(factor=0.3)

        ops.operator(BLCMAP_OT_curve_copy.bl_idname, icon='COPYDOWN', text="")
        ops.operator(BLCMAP_OT_curve_paste.bl_idname, icon='PASTEDOWN', text="")
    
    else:
        row = box.row()
        row.label(icon='ERROR', text="Missing Curve")
        row.operator(BLCMAP_OT_node_ensure.bl_idname, text="Reload")
        ops.label(icon='BLANK1')

#endregion UI Utilities