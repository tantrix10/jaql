
use crate::chunk::Chunk;
use crate::ops;

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
    let instruction: u8 = as_chunk.code[offset];
    let new_offset: usize = match instruction {
        ops::OP_RETURN => {
            simple_instruction("OP_RETURN", offset)
        },
        ops::OP_CONSTANT => {
            constant_instruction("OP_CONSTANT", as_chunk, offset)
        }
        _byte => {1}
    };
    new_offset
}

fn simple_instruction(inst: &str, offset: usize)->usize{
    println!(" {}", inst);
    return offset+1;
}

fn constant_instruction(inst: &str, chunk: &Chunk, offset: usize)->usize{
    let constant_index: u8 = chunk.code[offset+1];
    print!(" {}  {:04} ", inst, constant_index);
    let constant: f64 = chunk.constants.values[constant_index as usize];
    println!("{:?}", constant);
    return offset+2;
}