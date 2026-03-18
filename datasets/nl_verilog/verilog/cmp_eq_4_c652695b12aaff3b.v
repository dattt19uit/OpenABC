module design_cmp_eq_4_c652695b12aaff3b(a0, a1, a2, a3, b0, b1, b2, b3, y);
  input a0, a1, a2, a3, b0, b1, b2, b3;
  output y;
  assign y = ~(a0 ^ b0) & ~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3);
endmodule
