module design_cmp_eq_3_c3642044b7caee4a(a0, a1, a2, b0, b1, b2, y);
  input a0, a1, a2, b0, b1, b2;
  output y;
  assign y = ~(a0 ^ b0) & ~(a1 ^ b1) & ~(a2 ^ b2);
endmodule
