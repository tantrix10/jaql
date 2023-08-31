use crate::chunk::Chunk;
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
        // for instruction in self.chunk.code.iter() {
        //     // let result: InterpretResult =
        //     match instruction {
        //         &ops::OP_RETURN => {
        //             println!("RETURNING NOW");
        //             return InterpretResult::Ok
        //         },
        //         &ops::OP_CONSTANT => {
        //             println!("WE GOT A CONSTANT");
        //             // return InterpretResult::Ok;
        //         },
        //         _ => continue //InterpretResult::CompileError,
        //     };
        let mut offset: usize = 0;
        let length: usize = self.chunk.code.len();
        while offset < length {
            println!("{:0width$}", offset, width = 4);

            let instruction: u8 = self.chunk.code[offset];
            match instruction {
                ops::OP_RETURN => {
                    println!("Returning");
                    return InterpretResult::Ok;
                    offset += 1;
                }
                ops::OP_CONSTANT => {
                    println!("Constants");
                    offset += 2;
                }
                _byte => continue,
            }
        }
        return InterpretResult::Ok;
    }
}
