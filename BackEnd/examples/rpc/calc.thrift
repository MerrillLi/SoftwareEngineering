
struct userinfo{
    1:i32 uid;
    2:string name;
    3:string addr;
}

service Calculator {
  i32 add(1:i32 a, 2:i32 b);
  i32 sub(1:i32 a, 2:i32 b);
  i32 mult(1:i32 a, 2:i32 b);
  i32 div(1:i32 a, 2:i32 b);
  list<i32> glist(1:i32 a);
  userinfo guser(1:i32 uid);
}
