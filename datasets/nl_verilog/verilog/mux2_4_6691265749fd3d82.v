module design_mux2_4_6691265749fd3d82(d0_0, d0_1, d0_2, d0_3, d1_0, d1_1, d1_2, d1_3, s, y0, y1, y2, y3);
  input d0_0, d0_1, d0_2, d0_3, d1_0, d1_1, d1_2, d1_3, s;
  output y0, y1, y2, y3;
  assign y0 = ((d0_0 & ~s) | (d1_0 & s));
  assign y1 = ((d0_1 & ~s) | (d1_1 & s));
  assign y2 = ((d0_2 & ~s) | (d1_2 & s));
  assign y3 = ((d0_3 & ~s) | (d1_3 & s));
endmodule
