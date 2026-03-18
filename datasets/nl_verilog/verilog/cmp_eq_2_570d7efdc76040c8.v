module design_cmp_eq_2_570d7efdc76040c8(a0, a1, b0, b1, y);
  input a0, a1, b0, b1;
  output y;
  assign y = ~(a0 ^ b0) & ~(a1 ^ b1);
endmodule
