# tile.capnp
@0x822f5046804da778;

using import "city.capnp".City;
using import "vertex.capnp".Vertex;
using import "geog.capnp".State;
using import "geog.capnp".Country;
using import "geog.capnp".BBoxDeg;
using import "geog.capnp".Road;
using import "geog.capnp".Boundary;

struct Tile {
  id @0 :UInt32;
  name @1 :Text;
  cities @2 :List(Text); # use city idStr
  stateIds @3 :List(Text); # use state abbr
  countryIds @4 :List(Text); # use country abbr

  roads @5 :List(Road);
  boundaries @6 :List(Boundary);
  
  tileBounds @7 :List(Vertex);
  bboxDeg @8 :BBoxDeg;

  neighboringTileIds @9 :List(UInt32);

  # TODO build transform from degrees to tile coords

  # TODO edge waypoints

  # TODO information about waypoint to waypoint or city to city or waypoint to city travel time
}