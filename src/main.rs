mod chunk;
mod disassemble;
mod value;
mod ops;

use chunk::{Chunk};

fn main() {
    println!("Running main.");
    let mut blob = Chunk::new();
    let constant: u8 = blob.write_constant(42.0);
    let constant2: u8 = blob.write_constant(43.0);
    blob.write_chunk(ops::OP_CONSTANT as u8);
    blob.write_chunk(constant);
    blob.write_chunk(ops::OP_CONSTANT as u8);
    blob.write_chunk(constant2);
    blob.write_chunk(ops::OP_RETURN as u8);

    disassemble::dissasemble_chunk(&blob, "test");
}
