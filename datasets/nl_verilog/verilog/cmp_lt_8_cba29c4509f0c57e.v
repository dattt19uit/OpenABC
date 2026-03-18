module design_cmp_lt_8_cba29c4509f0c57e(a0, a1, a2, a3, a4, a5, a6, a7, b0, b1, b2, b3, b4, b5, b6, b7, y);
  input a0, a1, a2, a3, a4, a5, a6, a7, b0, b1, b2, b3, b4, b5, b6, b7;
  output y;
  assign y = (1 & ~a7 & b7) | (~(a7 ^ b7) & ~a6 & b6) | (~(a6 ^ b6) & ~(a7 ^ b7) & ~a5 & b5) | (~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~a4 & b4) | (~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~a3 & b3) | (~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~a2 & b2) | (~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~a1 & b1) | (~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~a0 & b0);
endmodule
