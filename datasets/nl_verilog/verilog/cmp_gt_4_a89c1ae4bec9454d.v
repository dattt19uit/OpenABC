module design_cmp_gt_4_a89c1ae4bec9454d(a0, a1, a2, a3, b0, b1, b2, b3, y);
  input a0, a1, a2, a3, b0, b1, b2, b3;
  output y;
  assign y = (1 & a3 & ~b3) | (~(a3 ^ b3) & a2 & ~b2) | (~(a2 ^ b2) & ~(a3 ^ b3) & a1 & ~b1) | (~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & a0 & ~b0);
endmodule
