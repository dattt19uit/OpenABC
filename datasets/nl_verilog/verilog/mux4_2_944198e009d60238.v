module design_mux4_2_944198e009d60238(d0_0, d0_1, d1_0, d1_1, d2_0, d2_1, d3_0, d3_1, s1, s0, y0, y1);
  input d0_0, d0_1, d1_0, d1_1, d2_0, d2_1, d3_0, d3_1, s1, s0;
  output y0, y1;
  assign y0 = ((d0_0 & ~s1 & ~s0) | (d1_0 & ~s1 & s0) | (d2_0 & s1 & ~s0) | (d3_0 & s1 & s0));
  assign y1 = ((d0_1 & ~s1 & ~s0) | (d1_1 & ~s1 & s0) | (d2_1 & s1 & ~s0) | (d3_1 & s1 & s0));
endmodule
