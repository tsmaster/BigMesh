# city.capnp
@0x8d5f7de04dce1a6d;

using import "vertex.capnp".VertDesc;
using import "vertex.capnp".Vertex;
using import "geog.capnp".State;
using import "geog.capnp".Country;
using import "geog.capnp".BBoxDeg;

struct City {
  id @0 :UInt32;
  name @1 :Text;
  idStr @2 :Text;  # compressed encoding like USA_WA_STL

  state @3 :Text; # short str like WA
  country @4 :Text; # short str like USA

  union {
    positionVertex @5: VertDesc;
    positionPolygon @6: List(VertDesc);
  }

  bboxDeg @7 :BBoxDeg;

  population @8 :UInt32;

  tileIds @9 :List(UInt32);
}          