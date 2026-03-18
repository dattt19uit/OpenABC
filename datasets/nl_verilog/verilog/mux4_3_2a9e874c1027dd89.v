module design_mux4_3_2a9e874c1027dd89(d0_0, d0_1, d0_2, d1_0, d1_1, d1_2, d2_0, d2_1, d2_2, d3_0, d3_1, d3_2, s1, s0, y0, y1, y2);
  input d0_0, d0_1, d0_2, d1_0, d1_1, d1_2, d2_0, d2_1, d2_2, d3_0, d3_1, d3_2, s1, s0;
  output y0, y1, y2;
  assign y0 = ((d0_0 & ~s1 & ~s0) | (d1_0 & ~s1 & s0) | (d2_0 & s1 & ~s0) | (d3_0 & s1 & s0));
  assign y1 = ((d0_1 & ~s1 & ~s0) | (d1_1 & ~s1 & s0) | (d2_1 & s1 & ~s0) | (d3_1 & s1 & s0));
  assign y2 = ((d0_2 & ~s1 & ~s0) | (d1_2 & ~s1 & s0) | (d2_2 & s1 & ~s0) | (d3_2 & s1 & s0));
endmodule
