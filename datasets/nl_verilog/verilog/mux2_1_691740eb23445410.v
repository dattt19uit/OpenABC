module design_mux2_1_691740eb23445410(d0_0, d1_0, s, y0);
  input d0_0, d1_0, s;
  output y0;
  assign y0 = ((d0_0 & ~s) | (d1_0 & s));
endmodule
