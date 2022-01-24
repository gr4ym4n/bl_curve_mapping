
import typing
import dataclasses
import uuid
import bpy
import mathutils

CURVE_BUFFER: 'BLCMAP_CurveDTO' = None

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
    BLCMAP_CurvePointDTO((0.0, 1.0), 'VECTOR'),
    BLCMAP_CurvePointDTO((1.0, 0.0), 'VECTOR'),
    ])

sine_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.1, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

sine_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

sine_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.1, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.9, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

quad_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.15, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO'),
    ])

quad_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.85, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO'),
    ])

quad_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)   , 'AUTO'),
    BLCMAP_CurvePointDTO((0.15, 0.955), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.85, 0.045), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)   , 'AUTO'),
    ])

cubic_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.2, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

cubic_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.8, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

cubic_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0) , 'AUTO'),
    BLCMAP_CurvePointDTO((0.2, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.8, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0) , 'AUTO'),
    ])

quart_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.25, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO'),
    ])

quart_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.75, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO'),
    ])

quart_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)  , 'AUTO'),
    BLCMAP_CurvePointDTO((0.25, 0.97), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.75, 0.03), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)  , 'AUTO'),
    ])

quint_in = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.275, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO'),
    ])

quint_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.725, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO'),
    ])

quint_in_out = BLCMAP_CurveDTO([
    BLCMAP_CurvePointDTO((0.0, 1.0)    , 'AUTO'),
    BLCMAP_CurvePointDTO((0.275, 0.975), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((0.725, 0.025), 'AUTO_CLAMPED'),
    BLCMAP_CurvePointDTO((1.0, 0.0)    , 'AUTO'),
    ])

PRESET_LUT = {
    'LINEAR'      : linear,
    'SINE_IN'     : sine_in,
    'SINE_OUT'    : sine_out,
    'SINE_IN_OUT' : sine_in_out,
    'QUAD_IN'     : quad_in,
    'QUAD_OUT'    : quad_out,
    'QUAD_IN_OUT' : quad_in_out,
    'CUBIC_IN'    : cubic_in,
    'CUBIC_OUT'   : cubic_out,
    'CUBIC_IN_OUT': cubic_in_out,
    'QUART_IN'    : quart_in,
    'QUART_OUT'   : quart_out,
    'QUART_IN_OUT': quart_in_out,
    'QUINT_IN'    : quint_in,
    'QUINT_OUT'   : quint_out,
    'QUINT_IN_OUT': quint_in_out,
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

#endregion Utilities

#region Property Groups
###################################################################################################

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

    def __init__(self, data: typing.Union[BLCMAP_CurvePointDTO, 'BLCMAP_CurvePoint', bpy.types.CurveMapPoint]) -> None:
        self["handle_type"] = data.handle_type
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
        assert len(data) >= 2
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

    EXTENSION_ITEMS = [
        ('HORIZONTAL', "Horizontal", ""),
        ('EXTRAPOLATED', "Extrapolated", ""),
        ]

    def __init__(self, data: typing.Union[BLCMAP_CurveDTO, 'BLCMAP_Curve', bpy.types.CurveMap]) -> None:
        self["extend"] = data.extend
        self.points.__init__(data.points)

    def get_node_identifier(self) -> str:
        identifier = self.get("identifier", "")
        if not identifier:
            identifier = f'{self.NODE_NAME_PREFIX}_{uuid.uuid4().hex}'
            self["identifier"] = identifier
        return identifier

    def update(self, context: typing.Optional[bpy.types.Curve]=None) -> None:
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
                manager.update(context)
            else:
                nodetree_node_update(self.node_identifier, self)


    extend: bpy.props.EnumProperty(
        name="Extend",
        description="Extrapolate the curve or extend it horizontally",
        items=EXTENSION_ITEMS,
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

    curve: bpy.props.PointerProperty(
        name="Curve",
        type=BLCMAP_Curve,
        options=set()
        )

    easing: bpy.props.EnumProperty(
        name="Easing",
        items=[
            ('EASE_IN'    , "In"      , "Ease in"        , 'NONE', 0),
            ('EASE_IN'    , "Out"     , "Ease out"       , 'NONE', 1),
            ('EASE_IN_OUT', "In & Out", "Ease in and out", 'NONE', 2),
            ],
        default='EASE_IN_OUT',
        options=set(),
        update=lambda self, context: self.update(context),
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
        update=lambda self, context: self.update(context),
        )

    def __init__(self,
                 interpolation: typing.Optional[str]='LINEAR',
                 easing: typing.Optional[str]='EASE_IN_OUT',
                 data: typing.Optional[typing.Union[BLCMAP_CurveDTO, BLCMAP_Curve]]=None) -> None:
        curve: BLCMAP_Curve = self.curve
        if interpolation == 'CURVE':
            self['interpolation'] = 6
            curve.__init__(data or linear)
        else:
            self["interpolation"] = ('LINEAR', 'SINE', 'QUAD', 'CUBIC', 'QUART', 'QUINT').index(interpolation)
            self["easing"] = easing
        self.__class__.update(self)

    def update(self, context: typing.Optional[bpy.types.Context]=None) -> None:
        ipo = self.interpolation
        curve: BLCMAP_Curve = self.curve
        if ipo != 'CURVE':
            preset = PRESET_LUT['LINEAR' if ipo == 'LINEAR' else f'{ipo}{self.easing[4:]}']
            curve.__init__(preset)
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
        global CURVE_BUFFER
        CURVE_BUFFER = BLCMAP_CurveDTO(tuple(BLCMAP_CurvePointDTO(point.location, point.handle_type) for point in curve.points), curve.extend)
        return {'FINISHED'}

class BLCMAP_OT_curve_paste(bpy.types.Operator):

    bl_idname = "blcmap.curve_paste"
    bl_label = "Paste Curve"
    bl_description = "Paste the curve from the buffer"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return CURVE_BUFFER is not None and isinstance(getattr(context, "curve", None), BLCMAP_Curve)

    def execute(self, context: bpy.types.Context) -> typing.Set[str]:
        global CURVE_BUFFER
        curve: BLCMAP_Curve = getattr(context, "curve")
        curve.__init__(CURVE_BUFFER)
        curve.update()
        return {'FINISHED'}

class BLCMAP_OT_curve_edit(bpy.types.Operator):

    bl_idname = "blcmap.curve_edit"
    bl_label = "Edit Curve"
    bl_description = "Edit the curve"
    bl_options = {'INTERNAL', 'UNDO'}

    node = None

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return isinstance(getattr(context, "curve", None), BLCMAP_Curve)

    def __del__(self) -> None:
        BLCMAP_OT_curve_edit.node = None
        BLCMAP_OT_curve_edit.data = None

    def invoke(self, context: bpy.types.Context, event: bpy.types.Event) -> typing.Set[str]:
        curve = getattr(context, "curve", None)

        if not isinstance(curve, BLCMAP_Curve):
            self.report({'ERROR'}, f'{self.__class__.__name__} Invalid context.curve {curve.__class__.__name__}')
            return {'CANCELLED'}

        node = nodetree_node_update(self.id_name, curve)
        BLCMAP_OT_curve_edit.node = node
        return context.window_manager.invoke_popup(self)

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        row = layout.row()
        row.ui_units_y = 0.01
        layout.template_curve_mapping(self.node, "mapping")

    def execute(self, context: bpy.types.Context) -> typing.Set[str]:

        curve: typing.Optional[BLCMAP_Curve] = getattr(context, "curve", None)
        if not isinstance(curve, BLCMAP_Curve):
            self.report({'ERROR'}, f'{self.__class__.__name__} Invalid context.curve {curve.__class__.__name__}')
            return {'CANCELLED'}

        node = BLCMAP_OT_curve_edit.node
        if not isinstance(node, bpy.types.ShaderNodeVectorCurve):
            self.report({'ERROR'}, f'{self.__class__.__name__} Invalid context.node {node.__class__.__name__}')

        curve.__init__(node.mapping.curves[0])
        curve.update()

        return {'FINISHED'}

#endregion Operators

#region UI Utilities
###################################################################################################

def draw_curve_manager_ui(layout: bpy.types.UILayout, manager: BCLMAP_CurveManager) -> None:
    box = layout.box()
    box.separator(factor=0.1)

    row = box.row(align=True)
    row.ui_units_y = 0.01
    row.separator(factor=0.5)
    row.context_pointer_set("curve", manager.curve)
    row.operator_context = 'INVOKE_DEFAULT'

    row.prop(manager, "interpolation", text="")
    
    ipo = manager.interpolation
    if ipo != 'LINEAR':
        subrow = row.row(align=True)
        subrow.ui_units_x = 6.0
        if ipo == 'CURVE':
            subrow.operator(BLCMAP_OT_curve_edit.bl_idname, text="Edit")
        else:
            subrow.prop(manager, "easing", text="")

    row.separator()

    subrow = row.row(align=True)
    subrow.alignment = 'RIGHT'
    subrow.operator(BLCMAP_OT_curve_copy.bl_idname, icon='COPYDOWN', text="")
    subrow.operator(BLCMAP_OT_curve_paste.bl_idname, icon='PASTEDOWN', text="")

    curve = manager.curve

    row.separator(factor=0.5)

    col = box.column()
    col.scale_x = 0.01
    col.enabled = False
    col.template_curve_mapping(nodetree_node_ensure(curve.get_node_identifier(), curve), "mapping")
    col.separator(factor=0.3)

#endregion UI Utilities