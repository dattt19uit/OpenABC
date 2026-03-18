module design_mux4_1_ddffd3ad3bdf78dc(d0_0, d1_0, d2_0, d3_0, s1, s0, y0);
  input d0_0, d1_0, d2_0, d3_0, s1, s0;
  output y0;
  assign y0 = ((d0_0 & ~s1 & ~s0) | (d1_0 & ~s1 & s0) | (d2_0 & s1 & ~s0) | (d3_0 & s1 & s0));
endmodule
