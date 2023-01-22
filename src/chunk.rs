#[repr(u8)]
pub enum OpCode {
    OP_RETURN,
}

pub struct Chunk {
    pub code: Vec<u8>,
    count: i64,
    capacity: i64,
}

impl Chunk {
    pub fn new() -> Self {
        Chunk {
            code: Default::default(),
            count: 0,
            capacity: 0,
        }
    }

    pub fn write_chunk(&mut self, byte: u8){
        if self.capacity < self.count + 1 {
            let old_capacity: i64 = self.capacity;
            self.capacity = self.grow_capacity()
        }
    }

    fn grow_capacity(&mut self)->i64{
        0
    }
}
