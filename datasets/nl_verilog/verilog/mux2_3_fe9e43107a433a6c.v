module design_mux2_3_fe9e43107a433a6c(d0_0, d0_1, d0_2, d1_0, d1_1, d1_2, s, y0, y1, y2);
  input d0_0, d0_1, d0_2, d1_0, d1_1, d1_2, s;
  output y0, y1, y2;
  assign y0 = ((d0_0 & ~s) | (d1_0 & s));
  assign y1 = ((d0_1 & ~s) | (d1_1 & s));
  assign y2 = ((d0_2 & ~s) | (d1_2 & s));
endmodule
