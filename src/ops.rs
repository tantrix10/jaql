use iota::iota;

// #[derive(PartialEq, Eq, Debug, Clone, Copy)]
// #[repr(u8)]
// pub enum OpCode {
//     OpReturn = 1,
//     OpConstant = 2,
// }

iota! {
    pub const
    OP_RETURN : u8 = iota;,
    OP_CONSTANT,
    OP_NEGATE,
    OP_ADD,
    OP_SUBTRACT,
    OP_MULTIPLY,
    OP_DIVIDE
}
