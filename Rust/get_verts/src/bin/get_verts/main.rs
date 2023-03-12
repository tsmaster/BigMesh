// get_verts main.rs


extern crate osmpbfreader;

fn main() {
    println!("Hello, verts!");

    let filename = std::env::args_os().nth(1).unwrap();
    let path = std::path::Path::new(&filename);
    let r = std::fs::File::open(&path).unwrap();
    let mut pbf = osmpbfreader::OsmPbfReader::new(r);
    
    for obj in pbf.iter().map(Result::unwrap) {
        match obj {
            osmpbfreader::OsmObj::Node(node) => {
                println!("id: {:?} lon: {} lat: {}", node.id.0, node.lon(), node.lat());
            }
            osmpbfreader::OsmObj::Way(_way) => {
            }
            osmpbfreader::OsmObj::Relation(_rel) => {
            }
        }
    }
}
