use crate::chunk::Chunk;
use crate::disassemble::dissasemble_instruction;
use crate::ops;
use crate::value::Value;

static STACK_MAX: u8 = 255;

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
    pub stack: Vec<Value>,
}

impl VM {
    pub fn new(chunk: Chunk) -> Self {
        VM {
            chunk: chunk,
            // ip: chunk.code
            stack: vec![],
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
            // TODO: debug flags properly
            self.debug(offset);
            match instruction {
                ops::OP_RETURN => {
                    println!("{}", self.pop());
                    // println!("Return");
                    return InterpretResult::Ok;
                }
                ops::OP_CONSTANT => {
                    offset = self.read_byte(offset);
                    let constant: Value = self.read_constant(offset as usize);
                    self.push(constant);
                    println!("{:?}", constant);
                }
                ops::OP_NEGATE => {
                    let stack_value: Value = self.pop();
                    self.push(-stack_value);
                }
                // TODO: makes these more generic
                ops::OP_ADD => {
                    let stack_value: Value = self.binary_op(ops::OP_ADD);
                    self.push(stack_value);
                }
                ops::OP_SUBTRACT => {
                    let stack_value: Value = self.binary_op(ops::OP_SUBTRACT);
                    self.push(stack_value)
                }
                ops::OP_MULTIPLY => {
                    let stack_value: Value = self.binary_op(ops::OP_MULTIPLY);
                    self.push(stack_value)
                }
                ops::OP_DIVIDE => {
                    let stack_value: Value = self.binary_op(ops::OP_DIVIDE);
                    self.push(stack_value)
                }
                _byte => continue,
            }
            offset += 1;
        }
        return InterpretResult::Ok;
    }

    fn debug(&mut self, offset: usize) {
        dissasemble_instruction(&self.chunk, offset);
        print!("Stack: ");
        for val in self.stack.iter() {
            print!("[{:?}], ", val)
        }
        print!("\n");
    }

    fn read_byte(&mut self, offset: usize) -> usize {
        let value: usize = offset + 1;
        return value;
    }

    fn read_constant(&mut self, offset: usize) -> f64 {
        return self.chunk.constants.values[self.chunk.code[offset] as usize];
    }

    pub fn push(&mut self, value: Value) {
        self.stack.push(value);
        if self.stack.len() > STACK_MAX as usize {
            panic!("STACK TOO BIG, cannot be greater than: {}", STACK_MAX);
        }
    }

    pub fn pop(&mut self) -> Value {
        let stack_value: Value = match self.stack.pop() {
            Some(x) => x,
            None => panic!("Stack empty"),
        };
        return stack_value;
    }

    pub fn reset_stack(&mut self) {
        self.stack = vec![];
    }

    fn binary_op(&mut self, operation: u8) -> Value {
        let b: Value = self.pop();
        let a: Value = self.pop();
        let c: Value = match operation {
            ops::OP_ADD => a + b,
            ops::OP_DIVIDE => a / b,
            ops::OP_MULTIPLY => a * b,
            ops::OP_SUBTRACT => a - b,
            _byte => panic!("Non binary operations"),
        };
        return c;
    }
}
