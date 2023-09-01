mod chunk;
mod disassemble;
mod ops;
mod value;
mod vm;

use chunk::Chunk;
use vm::VM;

fn main() {
    println!("Running main.");

    // let vm: VM = VM::new();

    let mut blob = Chunk::new();

    let constant: u8 = blob.write_constant(42.0);
    let constant2: u8 = blob.write_constant(43.0);

    blob.write_chunk(ops::OP_CONSTANT as u8, 123);
    blob.write_chunk(constant, 123);

    blob.write_chunk(ops::OP_CONSTANT as u8, 123);
    blob.write_chunk(constant2, 124);

    blob.write_chunk(ops::OP_SUBTRACT, 124);
    blob.write_chunk(ops::OP_RETURN as u8, 125);

    let mut vm: VM = VM::new(blob);

    vm.interpret();

    // disassemble::dissasemble_chunk(&blob, "test");
}
