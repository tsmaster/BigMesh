// get_cities main.rs

extern crate osmpbfreader;

const MIN_POP:i32 = 50000;

fn main() {
    println!("Hello, verts!");

    let filename = std::env::args_os().nth(1).unwrap();
    let path = std::path::Path::new(&filename);
    let r = std::fs::File::open(&path).unwrap();
    let mut pbf = osmpbfreader::OsmPbfReader::new(r);
    
    for obj in pbf.iter().map(Result::unwrap) {
        match obj {
            osmpbfreader::OsmObj::Node(node) => {
                if (node.tags.contains("place", "city")) ||
                    (node.tags.contains("place", "town")) {
                        let mut population = 0;

                        //println!("tags: {:?}", node.tags);

                        if node.tags.contains_key("population") {
                            //println!("pop {:?}",node);
                            let popstr = node.tags.get("population").unwrap();
                            let popstr = popstr.replace(',', "");
                            population = popstr.parse::<i32>().unwrap_or_default();
                        }
                        
                        // Only collect cities with a population of 50,000 or greater
                        if population >= MIN_POP {
                            let mut name = node.tags.get("name").unwrap();
                            if node.tags.contains_key("name:en") {
                                name = node.tags.get("name:en").unwrap();
                            }
                                
                            println!("Found a city: name={:?} population={} vertexid={}",
                                     name, population, node.id.0);
                            println!("vertex id: {} lon: {} lat: {}", node.id.0, node.lon(), node.lat());
                        }
                    }
            }
            osmpbfreader::OsmObj::Way(_way) => {
            }
            osmpbfreader::OsmObj::Relation(_rel) => {
            }
        }
    }
}
