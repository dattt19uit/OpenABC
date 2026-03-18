module design_decoder2_2_506cb8dcbeebb5b3(a0, a1, y0, y1, y2, y3);
  input a0, a1;
  output y0, y1, y2, y3;
  assign y0 = ~a0 & ~a1;
  assign y1 = a0 & ~a1;
  assign y2 = ~a0 & a1;
  assign y3 = a0 & a1;
endmodule
