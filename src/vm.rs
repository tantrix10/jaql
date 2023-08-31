use crate::chunk::Chunk;
use crate::ops;

#[derive(Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum InterpretResult {
    Ok,
    CompileError,
    RuntimeError,
}

pub struct VM{
    pub chunk: Chunk,
    // TODO: in lox this is a pointer straight to the instruction
    // dereffing a pointer is faster than lookup, see how this goes
    // ip: Vec<u8>
}

impl VM {
    pub fn new(chunk: Chunk) -> Self {
        VM{
            chunk: chunk,
            // ip: chunk.code
        }
    }

    pub fn interpret(&mut self) -> InterpretResult{
        return self.run();
    }

    fn run(&mut self,)->InterpretResult{

        for instruction in self.chunk.code.iter(){
            let result: InterpretResult = match instruction {
                &ops::OP_RETURN => {return InterpretResult::Ok},
                &ops::OP_CONSTANT=> InterpretResult::Ok,
                _ => InterpretResult::CompileError
            };
        }

        return InterpretResult::Ok;
    }
}

