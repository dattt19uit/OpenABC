module design_cmp_eq_7_c91eff622cb101f4(a0, a1, a2, a3, a4, a5, a6, b0, b1, b2, b3, b4, b5, b6, y);
  input a0, a1, a2, a3, a4, a5, a6, b0, b1, b2, b3, b4, b5, b6;
  output y;
  assign y = ~(a0 ^ b0) & ~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6);
endmodule
