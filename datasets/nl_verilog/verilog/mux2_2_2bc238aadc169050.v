module design_mux2_2_2bc238aadc169050(d0_0, d0_1, d1_0, d1_1, s, y0, y1);
  input d0_0, d0_1, d1_0, d1_1, s;
  output y0, y1;
  assign y0 = ((d0_0 & ~s) | (d1_0 & s));
  assign y1 = ((d0_1 & ~s) | (d1_1 & s));
endmodule
