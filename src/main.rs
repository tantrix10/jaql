mod chunk;
mod disassemble;

use chunk::{Chunk, OpCode};

fn main() {
    println!("Running main.");
    let mut blob = Chunk::new();
    blob.write_chunk(OpCode::OPRETURN);
    blob.write_chunk(OpCode::OPRETURN);
    disassemble::dissasemble_chunk(&blob, "test");
}
