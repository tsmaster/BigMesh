# geog.capnp
# stores state, countries 

@0xffe89e73cfd2e74e;

struct BBoxDeg {
  minLon @0 :Float32;
  minLat @1 :Float32;
  maxLon @2 :Float32;
  maxLat @3 :Float32;
}

struct State {
  id @0 :UInt32;
  name @1 :Text;
  abbreviation @2: Text;
  population @3 :UInt32;

  bboxDeg @4 :BBoxDeg;

  cityIds @5 :List(UInt32);
  countryId @6 :UInt32;

  tileIds @7 :List(UInt32);
}

struct Country {
  id @0 :UInt32;
  name @1 :Text;
  abbreviation @2: Text;
  population @3 :UInt32;

  bboxDeg @4 :BBoxDeg;

  tileIds @5 :List(UInt32);
}

struct Road {
  name @0 :Text;
  vertIndices @1 :List(UInt32);

  speed @2 :UInt16; # MPH or 0
}

struct Boundary {
  name @0 :Text; # unused?
  vertIndices @1 :List(UInt32);
}