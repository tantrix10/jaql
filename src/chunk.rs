use crate::value::{ValueArray, Value};


// #[derive(Clone, Copy)]
pub struct Chunk {
    pub code: Vec<u8>,
    count: i64,
    pub constants: ValueArray
}

impl Chunk {
    pub fn new() -> Self {
        Chunk {
            code: vec![],
            count: 0,
            constants: ValueArray::new(),
        }
    }

    pub fn write_chunk(&mut self, byte: u8){
        // TODO: I could template this and cast opcode as u8
        self.code.push(byte);
        self.count += 1;
    }

    pub fn write_constant(&mut self, constant: Value)->u8{
        // TODO: actually check if const already exists
        self.constants.write_value(constant);
        return self.constants.count - 1;
    }



}
