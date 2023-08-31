
pub type Value = f64;

#[derive(Clone)]
pub struct ValueArray {
    pub count: u8,
    pub values: Vec<Value>
}

impl ValueArray {
    pub fn new() -> Self {
        ValueArray {
            count: 0,
            values: vec![]
        }
    }

    pub fn write_value(&mut self, value: Value){
        self.values.push(value);
        self.count += 1;
    }
}
