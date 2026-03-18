module design_mux2_7_2bc809e67ffd749b(d0_0, d0_1, d0_2, d0_3, d0_4, d0_5, d0_6, d1_0, d1_1, d1_2, d1_3, d1_4, d1_5, d1_6, s, y0, y1, y2, y3, y4, y5, y6);
  input d0_0, d0_1, d0_2, d0_3, d0_4, d0_5, d0_6, d1_0, d1_1, d1_2, d1_3, d1_4, d1_5, d1_6, s;
  output y0, y1, y2, y3, y4, y5, y6;
  assign y0 = ((d0_0 & ~s) | (d1_0 & s));
  assign y1 = ((d0_1 & ~s) | (d1_1 & s));
  assign y2 = ((d0_2 & ~s) | (d1_2 & s));
  assign y3 = ((d0_3 & ~s) | (d1_3 & s));
  assign y4 = ((d0_4 & ~s) | (d1_4 & s));
  assign y5 = ((d0_5 & ~s) | (d1_5 & s));
  assign y6 = ((d0_6 & ~s) | (d1_6 & s));
endmodule
