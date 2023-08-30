

#[derive(PartialEq, Eq, Debug, Clone, Copy)]
#[repr(u8)]
pub enum OpCode {
    OPRETURN = 1,
}

// #[derive(Clone, Copy)]
pub struct Chunk {
    pub code: Vec<OpCode>,
    count: i64,
}

impl Chunk {
    pub fn new() -> Self {
        Chunk {
            code: vec![],
            count: 0,
        }
    }

    pub fn write_chunk(&mut self, byte: OpCode){
        self.code.push(byte);
        self.count += 1;
    }

}
