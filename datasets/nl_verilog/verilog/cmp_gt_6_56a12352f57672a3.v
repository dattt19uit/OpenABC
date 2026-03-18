module design_cmp_gt_6_56a12352f57672a3(a0, a1, a2, a3, a4, a5, b0, b1, b2, b3, b4, b5, y);
  input a0, a1, a2, a3, a4, a5, b0, b1, b2, b3, b4, b5;
  output y;
  assign y = (1 & a5 & ~b5) | (~(a5 ^ b5) & a4 & ~b4) | (~(a4 ^ b4) & ~(a5 ^ b5) & a3 & ~b3) | (~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & a2 & ~b2) | (~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & a1 & ~b1) | (~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & a0 & ~b0);
endmodule
