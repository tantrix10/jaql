use crate::chunk::Chunk;
use crate::disassemble::dissasemble_instruction;
use crate::ops;
use crate::value::Value;

#[derive(Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum InterpretResult {
    Ok,
    CompileError,
    RuntimeError,
}

pub struct VM {
    pub chunk: Chunk,
    // TODO: in lox this is a pointer straight to the instruction
    // dereffing a pointer is faster than lookup, see how this goes
    // ip: Vec<u8>
}

impl VM {
    pub fn new(chunk: Chunk) -> Self {
        VM {
            chunk: chunk,
            // ip: chunk.code
        }
    }

    pub fn interpret(&mut self) -> InterpretResult {
        return self.run();
    }

    fn run(&mut self) -> InterpretResult {
        let mut offset: usize = 0;
        let length: usize = self.chunk.code.len();
        while offset < length {
            // println!("{:0width$}", offset, width = 4);

            let instruction: u8 = self.chunk.code[offset];
            // TODO: debug flag
            dissasemble_instruction(&self.chunk, offset);
            match instruction {
                ops::OP_RETURN => {
                    println!("Return");
                    return InterpretResult::Ok;
                }
                ops::OP_CONSTANT => {
                    offset = self.read_byte(offset);
                    println!("{:?}", self.read_constant(offset as usize));
                }
                _byte => continue,
            }
            offset += 1;
        }
        return InterpretResult::Ok;
    }

    fn read_byte(&mut self, offset: usize) -> usize {
        let value: usize = offset + 1;
        return value;
    }

    fn read_constant(&mut self, offset: usize) -> f64 {
        return self.chunk.constants.values[self.chunk.code[offset] as usize];
    }
}
