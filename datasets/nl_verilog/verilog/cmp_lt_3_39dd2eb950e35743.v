module design_cmp_lt_3_39dd2eb950e35743(a0, a1, a2, b0, b1, b2, y);
  input a0, a1, a2, b0, b1, b2;
  output y;
  assign y = (1 & ~a2 & b2) | (~(a2 ^ b2) & ~a1 & b1) | (~(a1 ^ b1) & ~(a2 ^ b2) & ~a0 & b0);
endmodule
