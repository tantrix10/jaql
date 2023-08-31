use crate::value::{ValueArray, Value};


#[derive(Clone)]
pub struct Chunk {
    pub code: Vec<u8>,
    count: i64,
    pub constants: ValueArray,
    pub lines: Vec<u64>
}

impl Chunk {
    pub fn new() -> Self {
        Chunk {
            code: vec![],
            count: 0,
            constants: ValueArray::new(),
            lines: vec![],
        }
    }

    pub fn write_chunk(&mut self, byte: u8, line: u64){
        // TODO: I could template this and cast opcode as u8
        self.code.push(byte);
        self.lines.push(line);
        self.count += 1;
    }

    pub fn write_constant(&mut self, constant: Value)->u8{
        // TODO: actually check if const already exists
        self.constants.write_value(constant);
        return self.constants.count - 1;
    }



}
