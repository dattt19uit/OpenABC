module design_decoder3_3_0c8abd79557eee93(a0, a1, a2, y0, y1, y2, y3, y4, y5, y6, y7);
  input a0, a1, a2;
  output y0, y1, y2, y3, y4, y5, y6, y7;
  assign y0 = ~a0 & ~a1 & ~a2;
  assign y1 = a0 & ~a1 & ~a2;
  assign y2 = ~a0 & a1 & ~a2;
  assign y3 = a0 & a1 & ~a2;
  assign y4 = ~a0 & ~a1 & a2;
  assign y5 = a0 & ~a1 & a2;
  assign y6 = ~a0 & a1 & a2;
  assign y7 = a0 & a1 & a2;
endmodule
