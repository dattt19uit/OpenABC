module design_cmp_gt_2_9637b163c8169379(a0, a1, b0, b1, y);
  input a0, a1, b0, b1;
  output y;
  assign y = (1 & a1 & ~b1) | (~(a1 ^ b1) & a0 & ~b0);
endmodule
