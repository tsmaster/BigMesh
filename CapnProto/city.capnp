# city.capnp
@0x8d5f7de04dce1a6d;

using import "vertex.capnp".Vertex;
using import "geog.capnp".State;
using import "geog.capnp".Country;
using import "geog.capnp".BBoxDeg;

struct City {
  id @0 :UInt32;
  name @1 :Text;
  state @2 :UInt32; 
  country @3 :UInt32;

  union {
    positionVertex @4: Vertex;
    positionPolygon @5: List(Vertex);
  }

  bboxDeg @6 :BBoxDeg;

  population @7 :UInt32;
  elevation @8 :Float32;

  idStr @9 :Text;  # compressed encoding like STL_WA_USA

  tileIds @10 :List(UInt32);
}          