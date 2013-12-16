var x1;
var x2;

minimize z: x2;

s.t. c1 : x1 >= 0;
s.t. c2 : x2 >= 0;
s.t. c3 : x1 + x2 >= 1;

end;