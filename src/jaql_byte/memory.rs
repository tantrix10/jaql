pub fn grow_capacity(i64: capacity)->i64{
    if capacity<8{
        return 8
    }else{
        return capacity * 2
    }
}