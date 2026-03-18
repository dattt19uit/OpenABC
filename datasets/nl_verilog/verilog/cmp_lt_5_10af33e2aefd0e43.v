module design_cmp_lt_5_10af33e2aefd0e43(a0, a1, a2, a3, a4, b0, b1, b2, b3, b4, y);
  input a0, a1, a2, a3, a4, b0, b1, b2, b3, b4;
  output y;
  assign y = (1 & ~a4 & b4) | (~(a4 ^ b4) & ~a3 & b3) | (~(a3 ^ b3) & ~(a4 ^ b4) & ~a2 & b2) | (~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~a1 & b1) | (~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~a0 & b0);
endmodule
