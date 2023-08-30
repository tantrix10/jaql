// using crate::chunk;

use crate::chunk::{Chunk, OpCode};

pub fn dissasemble_chunk(as_chunk: &Chunk, name: &str){
    println!("=== {} ===", name);

    let mut offset: usize = 0;

    let length: usize = as_chunk.code.len();
    
    while offset < length{
        offset = dissasemble_instruction(as_chunk, offset);
    }
}

fn dissasemble_instruction(as_chunk: &Chunk, offset: usize) -> usize{
    print!("{:0width$}", offset, width = 4);
    let instruction: OpCode = as_chunk.code[offset];
    let new_offset: usize = match instruction {
        OpCode::OPRETURN => {
            simple_instruction("OP_RETURN", offset)
        }
    };
    new_offset
}

fn simple_instruction(inst: &str, offset: usize)->usize{
    println!(" {}", inst);
    return offset+1;
}